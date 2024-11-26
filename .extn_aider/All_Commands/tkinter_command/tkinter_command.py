"""Command for launching the enhanced tkinter editor"""

import os
import subprocess
import sys
from pathlib import Path
import pkg_resources

from ..commands_registry import CommandsRegistry

def ensure_dependencies():
    """Ensure required packages are installed"""
    required = {'pygments'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    
    if missing:
        # Install missing packages
        python = sys.executable
        subprocess.check_call([
            python, '-m', 'pip', 'install', *missing,
            '--quiet', '--disable-pip-version-check'
        ])
        return True
    return False

def cmd_tkinter_editor(self, initial_content=""):
    """Open the enhanced tkinter editor for writing prompts
    Usage: /tkinter_editor [initial_text]
    
    Opens a graphical editor window with:
    - Syntax highlighting for multiple formats
    - Keyword suggestions (type @keyword)
    - Status bar with document statistics
    - Control+S to save and close
    - Escape to cancel
    
    The tkinter editor uses keywords from .extn_aider.keywords.json for suggestions.
    """
    # Ensure dependencies are installed
    try:
        if ensure_dependencies():
            self.io.tool_output("Installing required packages...")
    except Exception as e:
        self.io.tool_error(f"Error installing dependencies: {e}")
        return None
        
    # Get package directory
    package_dir = Path(__file__).parent.parent
    
    # Import the editor directly
    try:
        from ..gui.editors.tkinter_editor.tkinter_editor import SimpleEditor
        
        # Create and run editor
        editor = SimpleEditor(initial_content)
        result = editor.run()
        
        if result is not None:
            return result
            
    except Exception as e:
        self.io.tool_error(f"Error running tkinter editor: {e}")
        return None

# Register the editor command
CommandsRegistry.register("tkinter_editor", cmd_tkinter_editor)