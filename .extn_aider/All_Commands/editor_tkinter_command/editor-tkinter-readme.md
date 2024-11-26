# Editor Tkinter Command for Aider

This module provides a feature-rich graphical editor based on Tkinter for writing and editing content in Aider. It includes syntax highlighting, keyword suggestions, and a clean modern interface.

## Features

- Syntax highlighting for multiple formats
- Keyword suggestions with @keyword triggers
- Format selection (plain, markdown, xml)
- Status bar with document statistics
- Modern UI with proper font rendering
- Cross-platform compatibility
- Auto-complete support
- Keyboard shortcuts
- Real-time updates

## Command Usage

```bash
/editor_tkinter [initial_text]
```

Opens a graphical Tkinter editor window with optional initial text content.

## Editor Interface

### Main Components

1. **Toolbar**
   - Format selector dropdown
   - Status updates

2. **Editor Area**
   - Syntax-highlighted text area
   - Line wrapping
   - Auto-indentation

3. **Status Bar**
   - Line count
   - Word count
   - Character count
   - Current format

4. **Control Buttons**
   - Save & Close
   - Cancel
   - Help text

## Implementation Details

### Editor Class Structure

```python
class SimpleEditor:
    def __init__(self, initial_text=""):
        self.root = tk.Tk()
        self.root.title("Simple Editor")
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Set up components
        self._setup_toolbar()
        self._setup_editor()
        self._setup_statusbar()
        self._setup_buttons()
        
        # Initialize state
        self.result = None
```

### Syntax Highlighting

Based on Pygments for multiple languages:
```python
SUPPORTED_FORMATS = {
    'plain': TextLexer(),
    'markdown': MarkdownLexer(),
    'xml': XmlLexer(),
    # More formats can be added
}
```

### Keyword Suggestions

```python
def _show_suggestions(self, word):
    """Show suggestion window with matching keywords"""
    if not word or not word.startswith('@'):
        return self._hide_suggestions()
        
    # Get matching keywords
    prefix = word[1:]  # Remove @ symbol
    matches = []
    for key, value in self.keywords.items():
        if key.startswith(prefix):
            matches.append((f"@{key}", value))
```

## Features Explained

### 1. Format Handling
- Multiple format support
- Real-time syntax updates
- Format-specific highlighting

### 2. Keyword Support
- Loads from `.extn_aider.keywords.json`
- Real-time suggestions
- Easy insertion with Tab/Enter

### 3. Text Statistics
- Line counting
- Word counting
- Character counting
- Format indication

### 4. File Operations
- Clean save handling
- Cancellation support
- State preservation

## Keyboard Shortcuts

| Shortcut | Action |
|----------|---------|
| Ctrl+S | Save & Close |
| Escape | Cancel |
| Tab/Enter | Insert suggestion |
| Up/Down | Navigate suggestions |

## Configuration

### Appearance Settings
```python
EDITOR_CONFIG = {
    'font': ('Courier', 12),
    'wrap': tk.WORD,
    'undo': True,
    'padx': 5,
    'pady': 5
}
```

### Color Schemes
```python
TAG_COLORS = {
    'keyword': '#0000FF',
    'string': '#008000',
    'comment': '#808080',
    'function': '#800080'
}
```

## Integration with Aider

The editor integrates with:
- Keyword system
- File handling
- Command framework
- Error reporting

## Command Registration

```python
def cmd_editor_tkinter(self, initial_content=""):
    """Open the enhanced tkinter editor for writing prompts
    Usage: /editor_tkinter [initial_text]
    
    Opens a graphical editor window with:
    - Syntax highlighting for multiple formats
    - Keyword suggestions (type @keyword)
    - Status bar with document statistics
    - Control+S to save and close
    - Escape to cancel
    """
    # Ensure dependencies
    try:
        if ensure_dependencies():
            self.io.tool_output("Installing required packages...")
    except Exception as e:
        self.io.tool_error(f"Error installing dependencies: {e}")
        return None
```

## Error Handling

The editor handles various error conditions:

1. **Dependency Issues**
```python
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
```

2. **Runtime Errors**
- Package installation failures
- Window creation issues
- File access problems
- Syntax highlighting errors

## Usage Examples

### 1. Basic Usage
```bash
/editor_tkinter
# Opens empty editor
```

### 2. With Initial Content
```bash
/editor_tkinter "Initial text"
# Opens editor with content
```

### 3. With Format Selection
```bash
# Select format from dropdown:
- plain
- markdown
- xml
```

## Technical Details

### Window Management

1. **Size and Position**
```python
window_width = 800
window_height = 600
center_x = int((screen_width - window_width) / 2)
center_y = int((screen_height - window_height) / 2)
```

2. **Component Layout**
```
+------------------+
| Format Selector  |
+------------------+
|                  |
|   Editor Area    |
|                  |
+------------------+
|   Status Bar     |
+------------------+
| Save   | Cancel  |
+------------------+
```

### Event Handling

1. **Key Events**
```python
self.root.bind('<Control-s>', self.save_and_close)
self.root.bind('<Escape>', self.cancel)
self.text_widget.bind('<KeyRelease>', self._on_key_release)
```

2. **Window Events**
```python
self.root.protocol("WM_DELETE_WINDOW", self.cancel)
```

## Best Practices

When using the editor:

1. **Content Management**
   - Use appropriate formats
   - Save regularly
   - Use keyword suggestions

2. **Performance**
   - Keep content size reasonable
   - Close editor when done
   - Use appropriate format

3. **Error Recovery**
   - Check error messages
   - Save important content
   - Use cancel carefully

## Troubleshooting

Common issues and solutions:

1. **Editor Won't Open**
   - Check Tkinter installation
   - Verify Python environment
   - Check system resources

2. **Syntax Highlighting Issues**
   - Verify format selection
   - Check Pygments installation
   - Review content format

3. **Suggestion Problems**
   - Check keywords file
   - Verify file permissions
   - Review trigger characters

## Contributing

When working with this command:
1. Test cross-platform compatibility
2. Maintain consistent UI
3. Handle errors gracefully
4. Document changes
5. Test all formats
