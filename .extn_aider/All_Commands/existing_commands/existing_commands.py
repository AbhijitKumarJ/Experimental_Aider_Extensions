"""
Startup script that adds wrapped versions of existing Aider commands.
Each wrapper starts with 'z' and adds additional functionality.
"""
import time
from pathlib import Path
import re
from ..commands_registry import CommandsRegistry

#convert url to a valid filename
def converturltofilename(url):
    # Replace all non-alphanumeric characters with underscores
    filename = re.sub(r'\W+', '_', url)
    return filename

# Web command wrapper - adds timing and retries
def cmd_zweb(self, args):
    """Enhanced /web command with timing and retry support"""
    if not args.strip():
        self.io.tool_error("Please provide a URL")
        return
        
    start_time = time.time()
    retries = 2
    
    while retries > 0:
        try:
            self.io.tool_output(f"Fetching {args} (retries left: {retries})...")
            content = self.cmd_web(args, return_content=True)
            self.io.tool_output("... added to chat.")

            self.coder.cur_messages += [
                dict(role="user", content=content),
                dict(role="assistant", content="Ok."),
            ]

            if content:
                elapsed = time.time() - start_time
                self.io.tool_output(f"Fetched in {elapsed:.2f} seconds")
                word_count = len(content.split())
                self.io.tool_output(f"Word count: {word_count:,}")
                #save content to a file - .extn_aider/temp/web
                web_dir = Path.cwd() / '.extn_aider' / 'temp' / 'web'
                web_dir.mkdir(parents=True, exist_ok=True)
                saved_file_name = f"{time.strftime('%Y%m%d_%H%M%S')}__{converturltofilename(args)}.txt"
                web_file = web_dir / saved_file_name
                web_file.write_text(content, encoding='utf-8')
                self.io.tool_output(f"Content saved to .extn_aider/temp/web/{saved_file_name}")
                #self.io.tool_output("\n\n"+content)
                retries = 0
                return
                #return content
            else:
                self.io.tool_error("No content found")
                retries -= 1
        except Exception as e:
            self.io.tool_error(f"Error: {e}")
            retries -= 1
            if retries > 0:
                time.sleep(2)  # Wait before retry
                
    self.io.tool_error("Failed to fetch content after multiple retries")



# Add command wrapper - adds file validation and git status
def cmd_zadd(self, args):
    """Enhanced /add command with validation and git status"""
    if not args.strip():
        self.io.tool_error("Please specify files to add")
        return
        
    # Show git status before adding
    if self.coder.repo:
        try:
            status = self.coder.repo.repo.git.status(short=True)
            if status:
                self.io.tool_output("Git status before adding files:")
                self.io.tool_output(status)
        except Exception as e:
            self.io.tool_error(f"Git error: {e}")
            
    # Track sizes of added files
    initial_sizes = {}
    for fname in self.coder.get_inchat_relative_files():
        try:
            size = Path(self.coder.abs_root_path(fname)).stat().st_size
            initial_sizes[fname] = size
        except Exception:
            pass
            
    # Call original add command
    self.cmd_add(args)
    
    # Show what changed
    self.io.tool_output("\nSummary of changes:")
    for fname in self.coder.get_inchat_relative_files():
        try:
            size = Path(self.coder.abs_root_path(fname)).stat().st_size
            if fname in initial_sizes:
                if size != initial_sizes[fname]:
                    self.io.tool_output(f"Modified: {fname} ({size:,} bytes)")
            else:
                self.io.tool_output(f"Added: {fname} ({size:,} bytes)")
        except Exception:
            pass
            

# Drop command wrapper - adds confirmation and backup
def cmd_zdrop(self, args):
    """Enhanced /drop command with confirmation and backup"""
    if not args.strip():
        if not self.io.confirm_ask("Drop all files from chat?", default="n"):
            return
            
    files_to_drop = []
    if args.strip():
        files_to_drop = args.strip().split()
    else:
        files_to_drop = self.coder.get_inchat_relative_files()
        
    # Create backups
    backup_dir = Path.home() / '.extn_aider' / 'temp' / 'backups'
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    backed_up = []
    
    for fname in files_to_drop:
        try:
            full_path = self.coder.abs_root_path(fname)
            if Path(full_path).exists():
                backup_path = backup_dir / f"{fname.replace('/', '_')}_{timestamp}"
                backup_path.write_text(Path(full_path).read_text())
                backed_up.append(fname)
        except Exception as e:
            self.io.tool_error(f"Backup error for {fname}: {e}")
            
    if backed_up:
        self.io.tool_output(f"Backed up {len(backed_up)} files to {backup_dir}")
        
    # Call original drop command
    self.cmd_drop(args)
    

# Commit command wrapper - adds file stats and commit message enhancement
def cmd_zcommit(self, args):
    """Enhanced /commit command with stats and message enhancement"""
    if not self.coder.repo:
        self.io.tool_error("No git repository found")
        return
        
    repo = self.coder.repo.repo
    
    # Get stats before commit
    stats = {}
    for fname in repo.git.diff(None, name_only=True).split():
        try:
            with open(fname) as f:
                lines = f.readlines()
                stats[fname] = {
                    'lines': len(lines),
                    'words': sum(len(line.split()) for line in lines)
                }
        except Exception:
            pass
            
    # Show what's being committed
    if stats:
        self.io.tool_output("Files to be committed:")
        for fname, file_stats in stats.items():
            self.io.tool_output(
                f"  {fname}: {file_stats['lines']:,} lines, "
                f"{file_stats['words']:,} words"
            )
            
    # Add stats to commit message if no message provided
    if not args:
        stats_msg = "\n\nFile statistics:\n"
        for fname, file_stats in stats.items():
            stats_msg += f"- {fname}: {file_stats['lines']} lines modified\n"
        args = stats_msg
        
    # Call original commit command
    result = self.cmd_commit(args)
    
    # Show commit details
    if result:
        commit = repo.head.commit
        self.io.tool_output(f"\nCommit: {commit.hexsha[:7]}")
        self.io.tool_output(f"Author: {commit.author}")
        self.io.tool_output(f"Date: {commit.committed_datetime}")
        
    return result
    

# Model command wrapper - adds model comparison
def cmd_zmodel(self, args):
    """Enhanced /model command with model comparison"""
    if not args.strip():
        self.io.tool_error("Please specify a model")
        return
        
    # Get current model info
    current_model = self.coder.main_model
    current_info = current_model.info
    
    # Call original model command
    self.cmd_model(args)
    
    # Get new model info
    new_model = self.coder.main_model
    new_info = new_model.info
    
    # Compare and show differences
    self.io.tool_output("\nModel comparison:")
    self.io.tool_output(f"Previous: {current_model.name}")
    self.io.tool_output(f"New: {new_model.name}")
    
    if current_info and new_info:
        comparisons = [
            ('Input tokens', 'max_input_tokens'),
            ('Output tokens', 'max_output_tokens'),
            ('Input cost', 'input_cost_per_token'),
            ('Output cost', 'output_cost_per_token')
        ]
        
        for label, key in comparisons:
            old_val = current_info.get(key, 'N/A')
            new_val = new_info.get(key, 'N/A')
            if old_val != new_val:
                self.io.tool_output(f"{label}: {old_val} → {new_val}")
                

# Clear command wrapper - adds backup of chat history
def cmd_zclear(self, args):
    """Enhanced /clear command with history backup"""
    # Backup current chat history
    if self.coder.done_messages:
        backup_dir = Path.cwd() / '.extn_aider' / 'temp' / 'history_backups'
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        backup_file = backup_dir / f"chat_history_{timestamp}.md"
        
        try:
            with open(backup_file, 'w') as f:
                for msg in self.coder.done_messages:
                    f.write(f"## {msg['role'].upper()}\n")
                    f.write(msg['content'])
                    f.write("\n\n")
                    
            self.io.tool_output(f"Chat history backed up to {backup_file}")
        except Exception as e:
            self.io.tool_error(f"Backup error: {e}")
            
    # Call original clear command
    self.cmd_clear(args)
    
# Voice command wrapper - adds transcription confidence and retry
def cmd_zvoice(self, args):
    """Enhanced /voice command with confidence check and retry"""
    max_retries = 3
    min_confidence = 0.8  # minimum confidence threshold
    
    for attempt in range(max_retries):
        self.io.tool_output(f"Recording attempt {attempt + 1}/{max_retries}...")
        
        text = self.cmd_voice(args)
        
        if not text:
            self.io.tool_error("No transcription received")
            continue
            
        # Here we could check transcription confidence if the API provided it
        # For now, we'll ask the user
        if self.io.confirm_ask("Was the transcription accurate? (Y/n)", default="y"):
            return text
            
        if attempt < max_retries - 1:
            self.io.tool_output("Let's try again...")
            
    self.io.tool_error("Max retries reached. Using last transcription.")
    return text
    
# Register commands
CommandsRegistry.register("zadd", cmd_zadd)
CommandsRegistry.register("zdrop", cmd_zdrop)
CommandsRegistry.register("zcommit", cmd_zcommit)
CommandsRegistry.register("zclear", cmd_zclear)
CommandsRegistry.register("zmodel", cmd_zmodel)
CommandsRegistry.register("zvoice", cmd_zvoice)
CommandsRegistry.register("zweb", cmd_zweb)