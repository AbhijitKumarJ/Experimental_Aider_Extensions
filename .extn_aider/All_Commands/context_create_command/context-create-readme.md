# Context Create Command for Aider

This module provides functionality to create interactive HTML views of your Aider chat context. It generates a comprehensive snapshot of your current chat session, including files, messages, model information, and Git status.

## Features

- Interactive HTML visualization of chat context
- Content organization by type (files, messages)
- Metadata display (model info, Git status)
- Proper file path handling using pathlib
- Cross-platform compatibility
- Error handling for file operations
- Browser integration for viewing

## Command Usage

```bash
/context_create
```

This command generates an HTML report and automatically opens it in your default browser.

## Generated Report Features

### 1. Metadata Section
- Timestamp of generation
- Model information (name, edit format)
- Statistics about files in chat
- Git repository status (if available)

### 2. Files Section
Lists all files in the chat with:
- File names
- Sizes and line counts
- File content previews
- Syntax highlighting for code

### 3. Chat History Section
Shows all chat messages with:
- Role-based formatting (user/assistant/system)
- Chronological ordering
- Full message content
- Special handling for repository map messages

## Implementation Details

### File Structure
The command creates this directory structure:
```
.extn_aider/
└── temp/
    └── context/
        └── context_view_YYYYMMDD_HHMMSS.html
```

### HTML Report Structure
```html
<!DOCTYPE html>
<html>
<head>
    <title>Aider Chat Context - {timestamp}</title>
    <!-- Styles -->
</head>
<body>
    <div class="container">
        <!-- Metadata section -->
        <!-- Files section -->
        <!-- Chat history section -->
    </div>
</body>
</html>
```

### Data Collection Functions

1. **File Information**
   ```python
   def get_file_stats(coder):
       stats = {'total_files': 0, 'total_lines': 0, 'total_chars': 0}
       file_details = []
       for fname in coder.get_inchat_relative_files():
           # Collect file statistics
       return stats, file_details
   ```

2. **Message Formatting**
   ```python
   def format_messages(messages):
       # Format chat messages with proper escaping
       # Add role-specific styling
   ```

3. **Git Information**
   ```python
   # Collected if git repository is available:
   git_info = {
       'branch': branch_name,
       'commit_hash': commit.hexsha[:7],
       'author': str(commit.author),
       'date': str(commit.committed_datetime)
   }
   ```

## CSS Styling

The command uses a custom CSS framework that provides:
- Clean, modern design
- Role-based message styling
- Proper code formatting
- Responsive layout
- Dark/light theme compatible

## Error Handling

The command handles various error conditions:
1. Missing directories
2. File access errors
3. Git repository issues
4. Browser launch failures

## Best Practices

When using this command:
1. Regularly create context snapshots
2. Keep generated reports organized
3. Clean up old reports periodically
4. Check report contents for sensitive information

## Example Generated Report

```html
<!-- Snapshot of a context report -->
<div class="metadata section">
    <div class="metadata-item">
        <h3>Model Information</h3>
        <p>Main Model: gemini/gemini-1.5-flash-latest</p>
        <p>Edit Format: whole</p>
    </div>
    
    <div class="metadata-item">
        <h3>Files in Chat</h3>
        <div class="stats">
            <div>Total Files: 3</div>
            <div>Total Lines: 150</div>
            <div>Total Chars: 4,500</div>
        </div>
    </div>
</div>
```

## Integration with Aider

The command integrates with Aider's:
- File management system
- Git functionality
- IO system
- Model information

## Technical Notes

1. **Path Handling**
   - Uses `pathlib.Path` for cross-platform compatibility
   - Handles relative paths properly
   - Validates file existence

2. **HTML Generation**
   - Uses template-based approach
   - Proper HTML escaping
   - Clean CSS organization

3. **Browser Integration**
   - Uses `webbrowser` module
   - Handles browser launch errors
   - Provides fallback file path

## Troubleshooting

Common issues and solutions:

1. **Report Not Generated**
   - Check directory permissions
   - Verify file paths
   - Check disk space

2. **Browser Not Opening**
   - Check default browser settings
   - Try manual file opening
   - Verify file permissions

3. **Missing Content**
   - Verify files in chat
   - Check file access permissions
   - Confirm message history

## Contributing

When working on this command:
1. Follow HTML best practices
2. Maintain CSS organization
3. Handle errors gracefully
4. Test cross-platform compatibility
5. Document changes