# Unofficial and experimental Aider Extension

Experimental Custom extensions for the Aider AI coding assistant.
The purpose of this repository is to experiment with possible new features and suggest to aider contributor to add based on their judgement.
Do not consider this in any way related to official distribution of aider.

## Important Notice

This is just for experimentation and not for serious use. If you want to use these files, 
please verify the code yourself and experiment with it before using it to any work.

## Features

- RAG (Retrieval Augmented Generation) support for document querying
- Advanced chat customization with keyword substitution
- Enhanced Git integration with better visualizations
- Code analysis and explanation tools
- Interactive context management and visualization
- GUI editors with syntax highlighting
- Web and voice command enhancements
- Template support for common development tasks

## Installation

```bash
# First install aider
pip install aider-chat

# Clone this repository
git clone https://github.com/YourUsername/aider-extension.git
cd aider-extension

# Install additional dependencies
pip install jinja2
pip install llama-index-core  
pip install llama-index-embeddings-huggingface
pip install pygments
pip install pyperclip
pip install streamlit
```

## Project Structure

```
./
├── main.py               # New simple runner
├── .extn_aider/           
│   ├── command_templates/ # Command templates
│   │   ├── load_templated/
│   │   └── load_templated_script/
│   └── All_Commands/     # Reference implementations (not used directly)
│       ├── docrag_commands/
│       ├── git_commands/
│       ├── context_commands/
│       └── ...
└── custom_aider/         # Core extension implementation
    ├── __init__.py
    ├── monkey_patch.py   # Early patching system
    ├── custom_aider_main.py
    ├── custom_coder.py
    ├── commands_registry.py
    ├── commands/         # Active command implementations
    │   ├── docrag_commands.py
    │   ├── git_commands.py
    │   └── ...
    ├── gui/             # GUI components
    └── docs/            # Documentation
```

## Basic Usage

1. Start the extended version:
```bash
python main.py
```

2. Use new commands in chat:
```
> /help  # See available commands
> /createragfromdoc docs ./documentation.md  # Create a RAG
> /glog -n 5  # Show git history
```

## Available Commands

Note: For detailed documentation on each command, see the README.md files in `.extn_aider/All_Commands/*/`

### Document Processing
- `/createragfromdoc` - Create a RAG from document
- `/queryragfromdoc` - Query existing RAGs
- `/listrag` - List available RAGs
- `/deleterag` - Remove a RAG

### Enhanced Chat
- `/customchat` - Chat with keyword substitution
- `/clip-edit` - Apply clipboard edits
- `/tkinter_editor` - Launch desktop editor

### Git Integration
- `/glog` - Enhanced git log
- `/zadd` - Smart git add
- `/zcommit` - Enhanced commit with stats

### Context Management
- `/showcontext` - Save/display chat context
- `/explain` - Interactive code explanation
- `/files` - List files with details
- `/stats` - Show file statistics

### Other Commands
- `/zvoice` - Enhanced voice command
- `/zweb` - Enhanced web scraping
- `/load_templated` - Load command templates
- `/load_templated_script` - Load script templates

## Configuration

1. Create `.aider.conf.yml`:
```yaml
model: gemini/gemini-1.5-flash-latest
map-tokens: 1024
subtree-only: true
```

2. Create `.extn_aider.keywords.json` for chat substitutions:
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