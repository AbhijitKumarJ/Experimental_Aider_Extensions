# Unofficial and experimental Aider Extension

Experimental Custom extensions for the Aider AI coding assistant.
The purpose of this repository is to experiment with possible new features and suggest to aider contributor to add based on their judgement.
Do not consider this in any way related to official distribution of aider.

## Important Notice

This is just for experimentation and not for serious use. If you want to use these files, 
please verify the code yourself and experiment with it before using it to any work.

## Project Layout
```
./
├── main.py           # New simple runner
└── custom_aider/
    ├── __init__.py
    ├── monkey_patch.py
    ├── custom_aider_main.py
    ├── custom_coder.py
    ├── commands_registry.py
    └── commands/     # Custom command implementations
        ├── __init__.py
        ├── clipboard_edits_command.py
        ├── context_commands.py
        ├── docrag_commands.py
        ├── existing_commands.py
        ├── explain_command.py
        ├── git_commands.py
        ├── keywords_command.py
        ├── tkinter_command.py
        └── utility_commands.py
```

## Usage

Run the extended version of aider: 

```bash
python main.py
```

## Available Extended Commands

### Document Analysis and RAG Commands

- `/createragfromdoc` - Create a RAG from a text/markdown document
  ```
  Usage: /createragfromdoc <nickname> <document_path>
  Creates a Retrieval Augmented Generation (RAG) index for enhanced document querying.
  Example: /createragfromdoc docs_rag /path/to/document.md
  requirements: same as help command advanced
  ```

- `/queryragfromdoc` - Query an existing RAG
  ```
  Usage: /queryragfromdoc <nickname> <query>
  Search through indexed documents for relevant content.
  Example: /queryragfromdoc docs_rag "How do I use the git commands?"
  requirements: same as help command advanced
  ```

- `/listrag` - List all available RAGs
  ```
  Usage: /listrag
  Shows details about all RAGs including source documents and creation dates.
  ```

- `/deleterag` - Delete a RAG
  ```
  Usage: /deleterag <nickname>
  Permanently removes a RAG and frees up disk space.
  ```

### Enhanced Chat Commands

- `/customchat` - Enhanced chat with keyword substitution
  ```
  Usage: /customchat <message>
  Supports @text-keyword references defined in .aider.keywords.json
  Example: /customchat Create @text-tests for the login function
  ```

### Editor Commands

- `/clip-edit` - Apply clipboard edits
  ```
  Usage: /clip-edit <filename>
  Applies code edits from clipboard (copied from ChatGPT/Claude) to specified files.
  ```

- `/tkinter_editor` - Launch enhanced Tkinter editor
  ```
  Usage: /tkinter_editor [initial_text]
  Opens a desktop GUI editor with syntax highlighting and keyword suggestions.
  ```

### Git Integration Commands

- `/glog` - Enhanced git log
  ```
  Usage: /glog [options]
  Options:
    -n N     Show last N commits (default: 10)
    --all    Show all branches
    --stat   Show changed files statistics
  ```

- `/zadd` - Enhanced add command
  ```
  Usage: /zadd <files>
  Adds files with validation and git status display.
  ```

- `/zcommit` - Enhanced commit command
  ```
  Usage: /zcommit [message]
  Commits changes with enhanced messages and file statistics.
  ```

### Context and Analysis Commands

- `/showcontext` - Save and display chat context
  ```
  Usage: /showcontext
  Creates an HTML report of current chat context including files and messages.
  ```

- `/explain` - Interactive code explanation
  ```
  Usage: /explain <function/class> [--level basic/deep/eli5]
  Creates interactive HTML documentation with diagrams and analysis.
  requirements: pip install jinja2
  ```

- `/files` - List files with details
  ```
  Usage: /files [pattern]
  Shows files in chat with sizes and modification times.
  ```

- `/stats` - Show file statistics
  ```
  Usage: /stats
  Displays lines, words, and character counts by file type.
  ```

### Enhanced Base Commands

- `/zclear` - Enhanced clear with history backup
- `/zdrop` - Enhanced drop with confirmation
- `/zmodel` - Enhanced model selection with comparison
- `/zvoice` - Enhanced voice command with confidence check and retry
- `/zweb` - Enhanced web command with saving scraped data in .aider/web folder and timing and retry support

## Configuration

### Keywords Configuration

Create a `.aider.keywords.json` file in your project root:

```json
{
    "api": "REST API with JSON responses",
    "mvc": "Model-View-Controller architecture pattern",
    "tests": "Unit tests using pytest with mocking",
    "docs": "Docstrings following Google style guide"
}
```

### Model Configuration

Create a `sample.aider.conf.yml` file:

```yaml
model: gemini/gemini-1.5-flash-latest
map-tokens: 1024
subtree-only: true
```

## Directory Structure

The extension creates several directories for storing data:

- `.aider/rags/` - Stores RAG indexes and metadata
- `.aider/context/` - Stores context HTML reports
- `.aider/web/` - Stores scraped web content
- `.aider/backups/` - Stores file backups
- `.aider/explanations/` - Stores code explanation reports

## Contributing

Feel free to experiment with these extensions and suggest improvements. This is an experimental project meant to explore potential new features for the Aider project.

## License

This project is licensed under the Apache License - see the LICENSE file for details.