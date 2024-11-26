"""Command for saving a backup copy of current chat context in JSON format"""

import json
from datetime import datetime
from pathlib import Path

from ..commands_registry import CommandsRegistry

def cmd_context_backup(self, args):
    """Save a backup copy of current chat context in JSON format
    Usage: /context_backup [filename_prefix]
    
    Saves the current chat context including model info, files, and messages
    as a JSON file in .extn_aider/temp/context_backup/ directory.
    Optional filename prefix can be specified.
    """
    # Create backup directory
    backup_dir = Path.cwd() / '.extn_aider' / 'temp' / 'context_backup'
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Generate timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')

    # Use provided prefix or default
    prefix = args.strip() if args else "aider_context"
    filename = f"{prefix}_{timestamp}.json"
    backup_file = backup_dir / filename

    try:
        # Gather context data
        context_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model": self.coder.main_model.name,
            "files": list(self.coder.get_inchat_relative_files()),
            "messages": self.coder.done_messages + self.coder.cur_messages
        }

        # Save to JSON file
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(context_data, f, indent=2, ensure_ascii=False)

        self.io.tool_output(f"\nSaved context backup to {backup_file}")

    except Exception as e:
        self.io.tool_error(f"Error saving context backup: {e}")

# Register the command
CommandsRegistry.register("context_backup", cmd_context_backup)
