# Aider Extension User Guide

A comprehensive guide to using the extended Aider command-line interface with all its enhanced features.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Working with Documents](#working-with-documents)
4. [Enhanced Git Integration](#enhanced-git-integration)
5. [Custom Chat Features](#custom-chat-features)
6. [Code Analysis Tools](#code-analysis-tools)
7. [Editor Integration](#editor-integration)
8. [Web and Voice Features](#web-and-voice-features)
9. [Configuration](#configuration)
10. [Tips and Tricks](#tips-and-tricks)

## Getting Started

### Installation

1. Clone the repository:
```bash
git clone https://github.com/AbhijitKumarJ/Experimental_Aider_Extensions.git
cd Experimental_Aider_Extensions
```

2. Install required dependencies:
```bash
pip install aider-chat
pip install jinja2
pip install llama-index-core
pip install llama-index-embeddings-huggingface
pip install pygments
pip install pyperclip
pip install streamlit
```

Optional dependencies for specific features:
```bash
# For voice commands
pip install SpeechRecognition

# For help system
pip install 'aider-chat[help]' --extra-index-url https://download.pytorch.org/whl/cpu

# For enhanced editor features
pip install tkinter  # Usually comes with Python
```

3. Start the extended Aider:
```bash
python main.py
```

### Initial Configuration

1. Create a configuration file `.aider.conf.yml`:
```yaml
model: gemini/gemini-1.5-flash-latest
map-tokens: 1024
subtree-only: true
```

2. Set up keywords file `.aider.keywords.json`:
```json
{
    "api": "REST API with JSON responses",
    "tests": "Unit tests using pytest with mocking"
}
```

## Basic Usage

### Starting a Session

```bash
# Start with default settings
python main.py

# Start with specific model
python main.py --model gemini/gemini-1.5-flash-latest

# Start with specific directory
python main.py /path/to/project
```

### Getting Help

```bash
# Show all available commands
> /help

# Get help for specific command
> /help createragfromdoc
```

## Working with Documents

### RAG (Retrieval Augmented Generation)

Creating and querying document-based RAGs:

```bash
# Create a RAG from a document
> /createragfromdoc docs_rag ./documentation.md

# List all available RAGs
> /listrag

# Query a RAG
> /queryragfromdoc docs_rag "How do I configure logging?"

# Delete a RAG when no longer needed
> /deleterag docs_rag
```

### File Management

Enhanced file operations:

```bash
# Show files in chat with details
> /files
> /files *.py  # Filter by pattern

# Show file statistics
> /stats

# Enhanced add command with validation
> /zadd file1.py file2.py

# Enhanced drop with confirmation
> /zdrop file1.py
```

## Enhanced Git Integration

### Git Log and Status

```bash
# Show pretty git log with graphs
> /glog
> /glog -n 5  # Show last 5 commits
> /glog --all  # Show all branches
> /glog --stat  # Show file statistics

# Enhanced commit with statistics
> /zcommit "Added new feature"
```

### Common Git Workflows

```bash
# Add files with status check
> /zadd *.py

# Commit with automatic statistics
> /zcommit

# Review changes
> /glog --stat
```

## Custom Chat Features

### Using Keyword Substitution

1. Define keywords in `.aider.keywords.json`:
```json
{
    "api": "REST API with JSON responses",
    "tests": "Unit tests using pytest with mocking"
}
```

2. Use in chat:
```bash
# Use keywords in messages
> /customchat Create @text-tests for the login function

# Keywords will be expanded automatically
> /customchat Add @text-api endpoint for user registration
```

### Context Management

```bash
# Save and view current chat context
> /showcontext

# Clear chat with history backup
> /zclear
```

## Code Analysis Tools

### Code Explanation

```bash
# Get interactive explanation of code
> /explain MyClass
> /explain my_function --level=deep
> /explain process_data --level=eli5
```

### Code Statistics

```bash
# Get detailed file statistics
> /stats

# Show specific file details
> /files mymodule.py
```

## Editor Integration

### Clipboard Integration

```bash
# Apply clipboard content as edits
> /clip-edit myfile.py
```

### GUI Editors

```bash
# Launch Streamlit editor
> /streamlit_editor

# Launch Tkinter editor
> /tkinter_editor
```

## Web and Voice Features

### Web Integration

```bash
# Enhanced web command with retry
> /zweb https://example.com/docs

# Content is automatically saved to .aider/web/
```

### Voice Integration

```bash
# Enhanced voice command
> /zvoice
# Speak your command
# Confirm accuracy when prompted
```

## Configuration

### Directory Structure

The extension creates these directories:
```
.aider/
├── rags/        # RAG indexes
├── context/     # Context reports
├── web/         # Scraped content
├── backups/     # File backups
└── explanations/# Code explanations
```

### Configuration Files

1. `.aider.conf.yml` - Main configuration:
```yaml
model: gemini/gemini-1.5-flash-latest
map-tokens: 1024
subtree-only: true
```

2. `.aider.keywords.json` - Custom keywords:
```json
{
    "api": "REST API with JSON responses",
    "tests": "Unit tests using pytest with mocking"
}
```

## Tips and Tricks

### Keyboard Shortcuts

- `Ctrl+C` - Cancel current operation
- `Ctrl+D` - Exit Aider
- `Ctrl+S` - Save in editors
- `Esc` - Cancel in editors

### Efficiency Tips

1. Use command completion:
   ```bash
   # Press Tab to complete commands
   > /cr<Tab>  # Completes to /createragfromdoc
   ```

2. Use patterns in file commands:
   ```bash
   > /files *.py  # Show only Python files
   ```

3. Quick context check:
   ```bash
   > /stats  # Quick overview of files
   ```

### Common Workflows

1. Document Analysis:
   ```bash
   > /createragfromdoc docs docs.md
   > /queryragfromdoc docs "How to configure?"
   ```

2. Code Review:
   ```bash
   > /zadd *.py
   > /stats
   > /explain MainClass
   ```

3. Git Operations:
   ```bash
   > /zadd modified_files.py
   > /glog --stat
   > /zcommit "Updates"
   ```

### Troubleshooting

1. Command not working:
   - Check if model is supported
   - Verify file paths are correct
   - Check for required dependencies

2. RAG issues:
   - Ensure document is text/markdown
   - Check document size is reasonable
   - Verify unique RAG nicknames

3. Editor issues:
   - Check for required packages
   - Verify clipboard content format
   - Check file permissions

### Best Practices

1. Regular backups:
   ```bash
   > /showcontext  # Saves context regularly
   ```

2. Organized RAGs:
   ```bash
   > /listrag  # Review existing RAGs
   > /deleterag unused_rag  # Clean up
   ```

3. Efficient keyword use:
   - Keep keywords focused and clear
   - Update keywords as needed
   - Use descriptive expansions

4. Version control:
   ```bash
   > /glog  # Regular status checks
   > /zcommit  # Frequent small commits
   ```

