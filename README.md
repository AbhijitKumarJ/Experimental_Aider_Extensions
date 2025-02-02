# Unofficial and experimental Aider Extension

Experimental Custom extensions for the Aider AI coding assistant.  This repository is for experimenting with potential new features and suggesting them to Aider contributors.  This is **not** an officially supported Aider distribution.

## Important Notice

This is purely experimental and not intended for production use.  Before using any code from this repository, please thoroughly review and test it.  Use at your own risk.

## Features

- **RAG (Retrieval Augmented Generation):**  Query documents using RAG.
- **Advanced Chat Customization:** Keyword substitution for enhanced chat interactions.
- **Enhanced Git Integration:** Improved visualizations and streamlined workflows.
- **Code Analysis and Explanation Tools:**  Interactive code analysis and explanation features.
- **Interactive Context Management:**  View, save, and load chat context.
- **GUI Editors:** Enhanced Tkinter editor with syntax highlighting and features.
- **Web and Voice Command Enhancements:** Improved web scraping and voice command processing.
- **Command Templating:** Create reusable command sequences using templates.


## Installation

1. **Install Aider:**
   ```bash
   pip install aider-chat
   ```

2. **Clone this repository:**
   ```bash
   git clone https://github.com/YourUsername/aider-extension.git
   cd aider-extension
   ```

3. **Install dependencies:**
   ```bash
   pip install jinja2 llama-index-core llama-index-embeddings-huggingface pygments pyperclip streamlit requests
   pip install 'aider-chat[help]' --extra-index-url https://download.pytorch.org/whl/cpu
   ```

## Project Structure

```
./
├── main.py               # Main script to run the extension
├── .extn_aider/           # Directory for extension data
│   ├── command_templates/ # Directory for command templates
│   │   ├── load_templated/
│   │   └── load_templated_script/
│   └── ...
└── custom_aider/         # Core extension code
    ├── __init__.py
    ├── monkey_patch.py   # Early patching of Aider classes
    ├── custom_aider_main.py # Main entry point for the extension
    ├── custom_coder.py    # Custom Coder class
    ├── commands_registry.py # Command registry
    ├── commands/         # Custom command implementations
    │   ├── docrag_commands.py
    │   ├── git_commands.py
    │   └── ...
    ├── gui/             # GUI components (Tkinter editor)
    └── docs/            # Documentation
```

## Basic Usage

1. **Start the extension:**
   ```bash
   python main.py
   ```

2. **Use commands in the Aider chat:**
   ```
   > /help  # List available commands
   > /createragfromdoc docs ./documentation.md  # Create a RAG index
   > /glog -n 5  # Show the last 5 git commits
   ```

## Available Commands

(See detailed documentation in the `custom_aider/docs` directory and individual command files.)

### Document Processing
- `/createragfromdoc <nickname> <path>`: Create a RAG index from a document.
- `/queryragfromdoc <nickname> <query>`: Query an existing RAG index.
- `/listrag`: List available RAG indexes.
- `/deleterag <nickname>`: Delete a RAG index.

### Enhanced Chat
- `/customchat <message>`: Send a message with keyword substitution.
- `/clip-edit <filename>`: Apply code edits from the clipboard.
- `/editor_tkinter`: Open the enhanced Tkinter editor.

### Git Integration
- `/glog [options]`: Show a Git log with graph and statistics.
- `/zadd <files>`: Add files to Git staging area with status check.
- `/zcommit <message>`: Commit changes with statistics in the message.
- `/zdrop <files>`: Remove files from the chat with backup.

### Context Management
- `/context_show`: Display the current chat context as HTML.
- `/context_backup [prefix]`: Save a backup of the chat context.
- `/context_load [filename]`: Load a chat context from a backup file.
- `/explain <target> [--level <level>]`: Get an interactive explanation of code.
- `/files [pattern]`: List files in the chat with details.
- `/stats`: Show statistics about files in the chat.
- `/zclear`: Clear the chat history with backup.

### Web and Voice
- `/zweb <url>`: Fetch content from a URL with retry mechanism.
- `/zvoice`: Use voice input with transcription confidence check.

### Template Loading
- `/load_templated <template_name>`: Load and execute a parameterized command template.
- `/load_templated_script <template_name>`: Load and execute a script-based command template.

### AIChat API
- `/aichat_rag_query <rag_name> <query>`: Query a RAG using the AIChat API.


## Configuration

1. **`.aider.conf.yml`:**  Main configuration file (see example below).
2. **`.extn_aider.keywords.json`:**  Keywords for chat substitution (see example below).

**Example `.aider.conf.yml`:**

```yaml
model: gemini/gemini-1.5-flash-latest
map-tokens: 1024
subtree_only: true
```

**Example `.extn_aider.keywords.json`:**

```json
{
  "api": "REST API with JSON responses",
  "tests": "Unit tests using pytest"
}
```

## Extension System Architecture

The extension system uses several key components:

1. **Command Registry** (`commands_registry.py`)
   - Central registration of commands
   - Manages completion handlers
   - Handles command help text

2. **Custom Coder** (`custom_coder.py`) 
   - Extends Aider's base Coder
   - Installs custom commands
   - Provides extension hooks

3. **Monkey Patching** (`monkey_patch.py`)
   - Early class patching
   - Safe core modifications
   - Path management

4. **Template Systems**
   - Command templates
   - Script templates 
   - Project scaffolding

For more technical details, see `custom_aider/docs/extension-docs.md`.

## Repository Organization 

- `.extn_aider/All_Commands/` contains reference implementations and documentation for each command type
- Active command implementations go in `custom_aider/commands/`
- GUI components in `custom_aider/gui/`
- Documentation in `custom_aider/docs/`

## Contributing

Feel free to experiment with these extensions and suggest improvements. This is an experimental project meant to explore potential new features for the Aider project.

## License

This project is licensed under the Apache License - see the LICENSE file for details.
