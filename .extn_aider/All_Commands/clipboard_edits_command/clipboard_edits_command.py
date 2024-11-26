"""Startup script that adds clipboard edit command"""
import pyperclip
from pathlib import Path

from ..commands_registry import CommandsRegistry

"""Add clipboard edit command to Aider"""
def cmd_clip_edit(self, args):
    """Apply clipboard contents as edits to specified files
    Usage: /clip-edit <filename>
    
    Gets code edits from clipboard (copied from ChatGPT/Claude) and applies them to the specified file.
    The clipboard content should contain code changes in a supported format (diff, whole file, etc).
    """
    if not args.strip():
        self.io.tool_error("Please specify a file to edit")
        return
        
    # Get clipboard content
    try:
        content = pyperclip.paste()
        if not content:
            self.io.tool_error("No content found in clipboard")
            return
    except Exception as e:
        self.io.tool_error(f"Error accessing clipboard: {e}")
        return
        
    target_file = args.strip()
    
    # Add file to chat if not already present
    if target_file not in self.coder.get_inchat_relative_files():
        self.cmd_add(target_file)
        if target_file not in self.coder.get_inchat_relative_files():
            return # Add failed
            
    # Set up for applying edits
    self.coder.partial_response_content = content
    
    try:
        # Try applying the edits
        edited = self.coder.apply_updates()
        
        if edited:
            self.io.tool_output(f"Applied clipboard edits to {', '.join(edited)}")
            
            # Auto-commit if enabled
            if self.coder.auto_commits and self.coder.repo:
                commit_msg = f"Applied clipboard edits to {', '.join(edited)}"
                self.coder.repo.commit(
                    fnames=edited,
                    message=commit_msg,
                    aider_edits=True
                )
        else:
            self.io.tool_error("No edits were applied. Check that the clipboard contains valid code changes.")
            
    except ValueError as e:
        # Handle format errors
        self.io.tool_error(f"Error applying edits: {e}")
        self.io.tool_output(
            "Make sure the clipboard contains code changes in a supported format "
            "(diff, whole file, etc)"
        )
        

# Add command completion
def completions_clip_edit(self):
    """Provide file completion for clip-edit command"""
    return self.completions_add()
    
CommandsRegistry.register("clip_edit", cmd_clip_edit, completions_clip_edit)