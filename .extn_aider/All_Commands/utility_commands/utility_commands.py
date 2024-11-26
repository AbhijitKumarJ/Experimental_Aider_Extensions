"""Utility command extensions"""

from pathlib import Path
from ..commands_registry import CommandsRegistry

def cmd_files(self, args):
    """List all files with details
    Usage: /files [pattern]
    
    Shows files in chat with their sizes and last modified times
    Optional pattern to filter files
    """
    files = self.coder.get_inchat_relative_files()
    if not files:
        self.io.tool_output("No files in chat")
        return
        
    pattern = args.strip() if args else None
    if pattern:
        files = [f for f in files if pattern in f]
        
    self.io.tool_output("\nFiles in chat:")
    for fname in sorted(files):
        try:
            path = Path(self.coder.abs_root_path(fname))
            stats = path.stat()
            size = stats.st_size
            modified = stats.st_mtime
            
            # Format size
            if size < 1024:
                size_str = f"{size}B"
            elif size < 1024 * 1024:
                size_str = f"{size/1024:.1f}KB"
            else:
                size_str = f"{size/1024/1024:.1f}MB"
                
            # Format time
            from datetime import datetime
            time_str = datetime.fromtimestamp(modified).strftime("%Y-%m-%d %H:%M")
            
            self.io.tool_output(f"{size_str:>8} {time_str} {fname}")
            
        except Exception as e:
            self.io.tool_error(f"Error getting info for {fname}: {e}")

def cmd_stats(self, args):
    """Show statistics about files in chat
    Usage: /stats
    
    Shows total lines, words, characters for all files in chat
    Breaks down by file type
    """
    files = self.coder.get_inchat_relative_files()
    if not files:
        self.io.tool_output("No files in chat")
        return
        
    stats = {
        'total': {'files': 0, 'lines': 0, 'words': 0, 'chars': 0},
        'by_type': {}
    }
    
    for fname in files:
        try:
            path = Path(self.coder.abs_root_path(fname))
            content = path.read_text()
            
            # Get extension
            ext = path.suffix.lower() or 'no_ext'
            if ext not in stats['by_type']:
                stats['by_type'][ext] = {
                    'files': 0, 'lines': 0, 'words': 0, 'chars': 0
                }
                
            # Calculate stats
            lines = len(content.splitlines())
            words = len(content.split())
            chars = len(content)
            
            # Update totals
            stats['total']['files'] += 1
            stats['total']['lines'] += lines
            stats['total']['words'] += words
            stats['total']['chars'] += chars
            
            # Update by type
            stats['by_type'][ext]['files'] += 1
            stats['by_type'][ext]['lines'] += lines
            stats['by_type'][ext]['words'] += words
            stats['by_type'][ext]['chars'] += chars
            
        except Exception as e:
            self.io.tool_error(f"Error processing {fname}: {e}")
            
    # Show results
    self.io.tool_output("\nTotal Statistics:")
    self.io.tool_output(f"Files: {stats['total']['files']}")
    self.io.tool_output(f"Lines: {stats['total']['lines']:,}")
    self.io.tool_output(f"Words: {stats['total']['words']:,}")
    self.io.tool_output(f"Chars: {stats['total']['chars']:,}")
    
    self.io.tool_output("\nBy File Type:")
    for ext, type_stats in sorted(stats['by_type'].items()):
        self.io.tool_output(f"\n{ext}:")
        self.io.tool_output(f"  Files: {type_stats['files']}")
        self.io.tool_output(f"  Lines: {type_stats['lines']:,}")
        self.io.tool_output(f"  Words: {type_stats['words']:,}")

# Register commands
CommandsRegistry.register("files", cmd_files)
CommandsRegistry.register("stats", cmd_stats)