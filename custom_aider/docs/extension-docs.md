# Aider Extension System Technical Documentation

This document explains how the Aider extension system works internally, providing technical details for developers who want to understand or extend the system.

## Overview

The extension system is built around several key components that work together to add new functionality to Aider:

1. Command Registry - Central registration and management of commands
2. Custom Coder - Enhanced coder class with extension support
3. Monkey Patching - System for safely extending Aider's core functionality
4. Dynamic Command Loading - Automatic discovery and loading of command modules

## Core Components

### 1. Commands Registry (`commands_registry.py`)

The `CommandsRegistry` is a central class that manages all custom commands:

```python
class CommandsRegistry:
    _commands: Dict[str, Callable] = {}
    _completions: Dict[str, Callable] = {}
    _descriptions: Dict[str, str] = {}

    @classmethod
    def register(cls, name: str, handler: Callable, completions: Optional[Callable] = None):
        # Registers a new command and its optional completions
        cmd_name = f"cmd_{name}"
        cls._commands[cmd_name] = handler
        if completions:
            cls._completions[f"completions_{name}"] = completions
```

Key features:
- Centralized command registration
- Support for command completions
- Automatic docstring extraction for help text
- Safe command installation checking

### 2. Custom Coder (`custom_coder.py`)

The `CustomCoder` extends Aider's base `Coder` class to support extensions:

```python
class CustomCoder(BaseCoder):
    _current_coder: ClassVar[Optional['CustomCoder']] = None
    
    @classmethod
    def create(cls, *args, **kwargs):
        coder = super().create(*args, **kwargs)
        if hasattr(coder, 'commands'):
            CommandsRegistry.install_commands(coder.commands)
        cls._current_coder = coder
        return coder
```

Features:
- Maintains compatibility with base Aider functionality
- Installs custom commands on creation
- Provides extension points for new features

### 3. Monkey Patching (`monkey_patch.py`)

The monkey patching system allows safe modification of Aider's core classes:

```python
def monkey_patch_aider():
    # Add custom_aider directory to Python path
    custom_aider_dir = Path(__file__).parent
    if str(custom_aider_dir) not in sys.path:
        sys.path.insert(0, str(custom_aider_dir))
    
    # Patch Aider's coder classes
    from custom_aider.custom_coder import CustomCoder
    import aider.coders as coders
    coders.Coder = CustomCoder
```

Purpose:
- Ensures extensions are loaded before Aider's core
- Maintains consistent state across the application
- Provides clean integration points

## Command Implementation

### Command Structure

Each command module should follow this structure:

```python
from ..commands_registry import CommandsRegistry

def cmd_commandname(self, args):
    """Command documentation
    Usage: /commandname <args>
    
    Detailed description of the command.
    """
    # Command implementation
    pass

def completions_commandname(self):
    """Return list of possible completions"""
    return ["completion1", "completion2"]

# Register the command
CommandsRegistry.register("commandname", cmd_commandname, completions_commandname)
```

### Command Types

1. **Simple Commands**
   ```python
   def cmd_simple(self, args):
       self.io.tool_output("Simple command output")
   ```

2. **Interactive Commands**
   ```python
   def cmd_interactive(self, args):
       if self.io.confirm_ask("Continue?", default="y"):
           # Perform action
           pass
   ```

3. **File-handling Commands**
   ```python
   def cmd_filehandler(self, args):
       for fname in self.coder.get_inchat_relative_files():
           path = Path(self.coder.abs_root_path(fname))
           # Process file
   ```

## Extension Initialization Flow

1. **Early Initialization**
   ```python
   # main.py
   from custom_aider.monkey_patch import monkey_patch_aider
   monkey_patch_aider()
   ```

2. **Command Loading**
   ```python
   def load_command_modules():
       commands_dir = Path(__file__).parent / "commands"
       for command_file in commands_dir.glob("*.py"):
           if not command_file.name.startswith("_"):
               importlib.import_module(f"custom_aider.commands.{command_file.stem}")
   ```

3. **Command Installation**
   ```python
   def initialize_custom_aider():
       # Override Coder class
       import aider.coders as coders
       from .custom_coder import CustomCoder
       coders.Coder = CustomCoder
       
       # Load command modules
       load_command_modules()
   ```

## Adding New Commands

### 1. Create Command Module

Create a new Python file in the `commands` directory:

```python
# commands/my_command.py
from ..commands_registry import CommandsRegistry

def cmd_mycommand(self, args):
    """My new command description
    Usage: /mycommand <args>
    """
    # Implementation
    pass

CommandsRegistry.register("mycommand", cmd_mycommand)
```

### 2. Command Features

Commands can access:
- `self.coder` - The `CustomCoder` instance
- `self.io` - Input/output interface
- `self.coder.repo` - Git repository (if available)
- `self.coder.main_model` - Current language model

### 3. Best Practices

1. **Error Handling**
   ```python
   try:
       # Command logic
   except Exception as e:
       self.io.tool_error(f"Error: {e}")
       return
   ```

2. **Input Validation**
   ```python
   if not args.strip():
       self.io.tool_error("Please provide required arguments")
       return
   ```

3. **Progress Feedback**
   ```python
   self.io.tool_output("Processing...")
   # Long operation
   self.io.tool_output("Done!")
   ```

## GUI Integration

The extension system supports multiple GUI frameworks:

### 1. Tkinter Integration
```python
class TkinterEditor:
    def __init__(self, initial_text=""):
        self.root = tk.Tk()
        # Setup GUI
```

### 2. Streamlit Integration
```python
def create_streamlit_app():
    import streamlit as st
    # Define Streamlit interface
```

## Data Storage

The extension uses the following directories for data storage:

- **`.extn_aider/rags/`**: Stores RAG (Retrieval Augmented Generation) indexes.  Each RAG is stored in its own subdirectory within this folder, named after the RAG's nickname.
- **`.extn_aider/temp/context_backup/`**: Stores backups of the chat context.  Backups are saved as JSON files with timestamps in the filename.
- **`.extn_aider/temp/context/`**: Stores HTML files generated by the `/context_create` command.
- **`.extn_aider/temp/web/`**: Stores content scraped from URLs using the `/zweb` command.
- **`.extn_aider/temp/backups/`**: Stores backups of files dropped from the chat using the `/zdrop` command.
- **`.extn_aider/explanations/`**: Stores code explanations generated by the `/explain` command.
- **`.extn_aider/command_templates/load_templated/`**: Stores JSON-based command templates for the `/load_templated` command.
- **`.extn_aider/command_templates/load_templated_script/`**: Stores Python script-based command templates for the `/load_templated_script` command.


Best practices for storage:
1. Use appropriate paths for global vs project data
2. Create directories as needed
3. Clean up temporary files
4. Handle storage errors gracefully

## Testing Extensions

### 1. Unit Testing Commands

```python
def test_command():
    coder = CustomCoder.create()
    result = coder.commands.cmd_mycommand("test args")
    assert result == expected_output
```

### 2. Integration Testing

```python
def test_extension_flow():
    initialize_custom_aider()
    # Test complete flow
```

## Debugging Tips

1. Enable debug output:
   ```python
   self.coder.verbose = True
   ```

2. Use logging:
   ```python
   import logging
   logger = logging.getLogger(__name__)
   logger.debug("Debug info")
   ```

3. Check command registration:
   ```python
   print(CommandsRegistry.list_commands())
   ```

## Common Issues and Solutions

1. **Command Not Found**
   - Check if command module is in the correct directory
   - Verify command registration syntax
   - Check for import errors in the module

2. **Completion Not Working**
   - Verify completion function is registered
   - Check completion function return value
   - Debug completion function logic

3. **GUI Issues**
   - Check required packages are installed
   - Verify GUI framework compatibility
   - Handle GUI events properly

## Best Practices Summary

1. Follow consistent command naming
2. Provide clear documentation
3. Handle errors gracefully
4. Give user feedback for long operations
5. Clean up resources properly
6. Test thoroughly
7. Log appropriately
8. Use appropriate storage locations
9. Validate inputs
10. Support command completion where appropriate

## Available Commands

This section provides a summary of the available commands within the extension.  For detailed usage instructions and examples, refer to the individual command files within the `custom_aider/commands` directory.

### Document Processing Commands
- `/createragfromdoc`: Create a RAG index from a document.
- `/queryragfromdoc`: Query an existing RAG index.
- `/listrag`: List available RAG indexes.
- `/deleterag`: Delete a RAG index.

### Enhanced Chat Commands
- `/customchat`: Send a message with keyword substitution.
- `/clip-edit`: Apply code edits from the clipboard.
- `/editor_tkinter`: Open the enhanced Tkinter editor.

### Git Integration Commands
- `/glog`: Show a Git log with graph and statistics.
- `/zadd`: Add files to Git staging area with status check.
- `/zcommit`: Commit changes with statistics in the message.
- `/zdrop`: Remove files from the chat with backup.

### Context Management Commands
- `/context_show`: Display the current chat context as HTML.
- `/context_backup`: Save a backup of the chat context.
- `/context_load`: Load a chat context from a backup file.
- `/context_create`: Create an interactive context view with export capabilities.

### Web and Voice Commands
- `/zweb`: Fetch content from a URL with retry mechanism.
- `/zvoice`: Use voice input with transcription confidence check.

### Template Loading Commands
- `/load_templated`: Load and execute a parameterized command template.
- `/load_templated_script`: Load and execute a script-based command template.

### AIChat API Commands
- `/aichat_rag_query`: Query a RAG using the AIChat API.

### Time Machine Command
- `/timemachine`: Explore code history intelligently.

### Utility Commands
- `/files`: List files with details.
- `/stats`: Show file statistics.

