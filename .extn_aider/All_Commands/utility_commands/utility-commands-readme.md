# Utility Commands for Aider

This module provides enhanced file and statistics utilities for better insight into your codebase. It includes commands for listing files with details and showing comprehensive statistics about files in the chat context.

## Commands

### 1. Files Command (`/files`)

Lists all files in chat with detailed information.

```bash
# Usage
/files [pattern]

# Examples
/files              # List all files
/files *.py        # List only Python files
/files src/*       # List files in src directory
```

#### Features:
- File sizes with human-readable formatting (B, KB, MB)
- Last modified timestamps
- Optional pattern filtering
- Sorted output

#### Output Example:
```
Files in chat:
  4.2KB 2024-01-20 14:30 main.py
  2.1MB 2024-01-20 14:25 data.csv
   528B 2024-01-20 14:20 config.yml
```

### 2. Stats Command (`/stats`)

Shows detailed statistics about files in chat.

```bash
# Usage
/stats
```

#### Statistics Provided:

1. **Total Statistics**
   - Total number of files
   - Total lines across all files
   - Total words count
   - Total character count

2. **By File Type**
   - Statistics broken down by file extension
   - Files per type
   - Lines per type
   - Words per type

#### Output Example:
```
Total Statistics:
Files: 10
Lines: 1,234
Words: 5,678
Chars: 23,456

By File Type:
.py:
  Files: 5
  Lines: 850
  Words: 3,200

.md:
  Files: 3
  Lines: 384
  Words: 2,478
```

## Implementation Details

### File Path Handling

Both commands use `pathlib.Path` for cross-platform compatibility:

```python
from pathlib import Path

path = Path(self.coder.abs_root_path(fname))
stats = path.stat()
```

### Size Formatting

Files command formats sizes for readability:
```python
def format_size(size):
    if size < 1024:
        return f"{size}B"
    elif size < 1024 * 1024:
        return f"{size/1024:.1f}KB"
    else:
        return f"{size/1024/1024:.1f}MB"
```

### Statistics Collection

Stats command collects metrics by file type:
```python
stats = {
    'total': {'files': 0, 'lines': 0, 'words': 0, 'chars': 0},
    'by_type': {}
}

# Process each file
for fname in files:
    ext = Path(fname).suffix.lower() or 'no_ext'
    if ext not in stats['by_type']:
        stats['by_type'][ext] = {
            'files': 0, 'lines': 0, 'words': 0, 'chars': 0
        }
```

## Error Handling

Both commands handle various error conditions:

1. **File Access Errors**
   ```python
   try:
       path = Path(self.coder.abs_root_path(fname))
       content = path.read_text()
   except Exception as e:
       self.io.tool_error(f"Error processing {fname}: {e}")
   ```

2. **Pattern Matching**
   ```python
   pattern = args.strip() if args else None
   if pattern:
       files = [f for f in files if pattern in f]
   ```

3. **Empty File Lists**
   ```python
   if not files:
       self.io.tool_output("No files in chat")
       return
   ```

## Integration with Aider

### File Access
- Uses Aider's file path resolution
- Handles relative paths correctly
- Respects git repository boundaries

### Output Formatting
- Uses Aider's IO system
- Consistent error reporting
- Human-readable number formatting

## Technical Details

### Path Resolution
1. Get relative files from Aider:
   ```python
   files = self.coder.get_inchat_relative_files()
   ```

2. Convert to absolute paths:
   ```python
   path = Path(self.coder.abs_root_path(fname))
   ```

### File Statistics
1. Size information:
   ```python
   stats = path.stat()
   size = stats.st_size
   modified = stats.st_mtime
   ```

2. Content analysis:
   ```python
   content = path.read_text()
   lines = len(content.splitlines())
   words = len(content.split())
   chars = len(content)
   ```

## Usage Tips

### Files Command

1. **Pattern Matching**
   - Use `*.ext` for specific file types
   - Use `dir/*` for directory filtering
   - Patterns match anywhere in path

2. **Output Interpretation**
   - Size shown in most appropriate unit
   - Times in local timezone
   - Sorted alphabetically

### Stats Command

1. **Analysis**
   - Check file distributions
   - Identify large files
   - Monitor code growth

2. **By Type Analysis**
   - Compare code vs documentation
   - Track test coverage
   - Identify outliers

## Best Practices

1. **Regular Use**
   - Check file stats regularly
   - Monitor codebase growth
   - Look for outliers

2. **Pattern Usage**
   - Use specific patterns
   - Filter unnecessary files
   - Group related files

3. **Output Review**
   - Check file sizes
   - Monitor line counts
   - Watch growth trends

## Error Messages

Common error messages and causes:

1. **File Errors**
   ```
   Error getting info for file.txt: [Errno 2] No such file or directory
   ```
   - File was deleted/moved
   - Permission issues
   - Path resolution problems

2. **Processing Errors**
   ```
   Error processing file.txt: UnicodeDecodeError
   ```
   - Encoding issues
   - Binary files
   - Corrupt files

## Contributing

When working with these commands:

1. **Code Quality**
   - Handle errors gracefully
   - Keep stats accurate
   - Format output clearly

2. **Performance**
   - Cache file stats when possible
   - Minimize file reads
   - Handle large files well

3. **Compatibility**
   - Use pathlib for paths
   - Handle various file types
   - Support all platforms

## Limitations

1. **Files Command**
   - Basic pattern matching only
   - No regex support
   - Single pattern only

2. **Stats Command**
   - Memory use scales with file size
   - Basic word counting
   - No content analysis

## Future Improvements

Potential enhancements:

1. **Files Command**
   - Advanced pattern matching
   - Multiple patterns
   - Custom sorting

2. **Stats Command**
   - Code complexity metrics
   - Language-specific stats
   - Historical trending