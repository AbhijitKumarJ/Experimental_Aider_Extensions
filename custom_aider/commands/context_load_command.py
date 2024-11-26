"""Command for restoring chat context from a backup file"""

import json
from datetime import datetime
from pathlib import Path
import os

from ..commands_registry import CommandsRegistry

def _list_context_files():
    """List all context files in backup and create directories"""
    context_files = []
    
    # Check both backup and create directories
    for dirname in ['context_backup', 'context_create']:
        context_dir = Path.cwd() / '.extn_aider' / 'temp' / dirname
        if context_dir.exists():
            context_files.extend(context_dir.glob('*.json'))
            
    return sorted(context_files)

def _load_context_file(filepath):
    """Load and validate context file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Validate required fields
        required_fields = ['timestamp', 'model', 'files', 'messages']
        if not all(field in data for field in required_fields):
            raise ValueError("Missing required fields in context file")
            
        return data
    except Exception as e:
        raise ValueError(f"Error loading context file: {e}")

def cmd_context_load(self, args):
    """Load a context from a backup file
    Usage: /context_load [filename]
    
    If filename is not provided, lists available context files.
    First clears current context, then loads files and messages from the context file.
    Searches in both .extn_aider/temp/context_backup/ and .extn_aider/temp/context_create/ directories.
    """
    # List context files if no argument provided
    if not args.strip():
        context_files = _list_context_files()
        if not context_files:
            self.io.tool_error("No context files found in .extn_aider/temp/context_backup/ or .extn_aider/temp/context_create/")
            return
            
        self.io.tool_output("\nAvailable context files:")
        for file in context_files:
            file_time = datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            self.io.tool_output(f"  {file.name} (Last modified: {file_time})")
        return

    # Find the specified file
    filename = args.strip()
    context_file = None
    
    for dirname in ['context_backup', 'context_create']:
        path = Path.cwd() / '.extn_aider' / 'temp' / dirname / filename
        if path.exists():
            context_file = path
            break
            
    if not context_file:
        self.io.tool_error(f"Context file not found: {filename}")
        return

    try:
        # Load and validate context file
        context_data = _load_context_file(context_file)
        
        # Clear current context and files
        self.cmd_reset("")
        
        # Add files from context
        files_to_add = []
        for file in context_data['files']:
            file_path = Path(self.coder.abs_root_path(file))
            if file_path.exists():
                files_to_add.append(file)
            else:
                self.io.tool_warning(f"File not found: {file}")
                
        if files_to_add:
            self.cmd_add(" ".join(files_to_add))
            
        # Add messages to context
        self.coder.done_messages.extend(context_data['messages'])
        
        # Report success
        self.io.tool_output(f"\nLoaded context from {context_file}")
        self.io.tool_output(f"Model: {context_data['model']}")
        self.io.tool_output(f"Timestamp: {context_data['timestamp']}")
        self.io.tool_output(f"Added {len(files_to_add)} files")
        self.io.tool_output(f"Added {len(context_data['messages'])} messages")
        
    except Exception as e:
        self.io.tool_error(f"Error loading context: {e}")

def completions_context_load(self):
    """Provide completions for context_load command - available context files"""
    try:
        return [f.name for f in _list_context_files()]
    except:
        return []

# Register the command
CommandsRegistry.register("context_load", cmd_context_load, completions_context_load)
