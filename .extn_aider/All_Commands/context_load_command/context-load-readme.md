# Context Restore Command for Aider

This module provides functionality to restore Aider chat contexts from previously saved backup files. It allows you to load saved chat states, including files and message history, from either backup context files or exported context files.

## Features

- Load chat contexts from backup files
- List available context files
- Support for multiple backup sources
- Automatic file validation
- Smart file handling
- Command completion support

## Command Usage

### List Available Contexts
```bash
/context_load
```
Shows all available context files with their timestamps.

### Load Specific Context
```bash
/context_load filename.json
```
Restores chat state from the specified context file.

## Backup Sources

The command searches for context files in two locations:
```
.extn_aider/temp/
├── context_backup/     # Automatic backups
└── context_create/     # User-created contexts
```

## Context File Format

Expected JSON structure:
```json
{
    "timestamp": "2024-11-26 21:20:01",
    "model": "gemini/gemini-1.5-flash-latest",
    "files": [
        "src/main.py",
        "tests/test_main.py"
    ],
    "messages": [
        {
            "role": "user",
            "content": "Example message"
        },
        {
            "role": "assistant",
            "content": "Response"
        }
    ]
}
```

## Restore Process

1. **Validation**
   - Checks file existence
   - Validates JSON structure
   - Verifies required fields
   - Checks file paths

2. **State Reset**
   - Clears current context
   - Resets file list
   - Cleans message history

3. **File Loading**
   - Adds files to chat
   - Verifies file existence
   - Handles missing files
   - Preserves file order

4. **Message Restoration**
   - Restores chat history
   - Maintains message order
   - Preserves roles
   - Keeps content intact

## Command Completion

The command provides completion support for:
- Available context filenames
- Recent backup files
- Common file patterns

## Usage Examples

### List Available Contexts
```bash
> /context_load
Available context files:
  aider_context_20241126_212001.json (Last modified: 2024-11-26 21:20:01)
  project_backup_20241126_213045.json (Last modified: 2024-11-26 21:30:45)
```

### Load Specific Context
```bash
> /context_load aider_context_20241126_212001.json
Loaded context from aider_context_20241126_212001.json
Model: gemini/gemini-1.5-flash-latest
Timestamp: 2024-11-26 21:20:01
Added 3 files
Added 15 messages
```

## Error Handling

### Common Issues

1. **File Not Found**
   ```bash
   Error: Context file not found: nonexistent.json
   ```

2. **Invalid JSON**
   ```bash
   Error loading context: Invalid JSON structure
   ```

3. **Missing Files**
   ```bash
   Warning: File not found: missing_file.py
   ```

### Recovery Steps

1. **No Context Files**
   ```bash
   No context files found in .extn_aider/temp/context_backup/ or .extn_aider/temp/context_create/
   ```

2. **Partial Restore**
   - Successfully loaded files are added
   - Missing files are reported
   - Chat history is restored
   - Warning messages displayed

## Best Practices

1. **Regular Backups**
   - Create regular context backups
   - Use meaningful filenames
   - Verify backup contents
   - Keep backup history

2. **Restore Workflow**
   - List available contexts first
   - Verify file timestamps
   - Check file contents
   - Test after restore

3. **File Management**
   - Clean up old backups
   - Organize backup files
   - Document backup contents
   - Track file changes

## Integration

Works well with other context commands:
- `/context_backup` - Create backups
- `/context_show` - View current context
- `/context_create` - Create new contexts

## Technical Details

### File Search
```python
def _list_context_files():
    """List all context files in backup and create directories"""
    context_files = []
    for dirname in ['context_backup', 'context_create']:
        context_dir = Path.cwd() / '.extn_aider' / 'temp' / dirname
        if context_dir.exists():
            context_files.extend(context_dir.glob('*.json'))
    return sorted(context_files)
```

### File Loading
```python
def _load_context_file(filepath):
    """Load and validate context file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Validate required fields
    required_fields = ['timestamp', 'model', 'files', 'messages']
    if not all(field in data for field in required_fields):
        raise ValueError("Missing required fields")
    return data
```

## Troubleshooting

### Common Problems

1. **Loading Fails**
   - Check file permissions
   - Verify JSON format
   - Check file encoding
   - Validate content structure

2. **Missing Files**
   - Verify file paths
   - Check file existence
   - Update file locations
   - Review file permissions

3. **Incomplete Restore**
   - Check error messages
   - Verify file contents
   - Review backup integrity
   - Check disk space

### Debug Steps

1. List available contexts:
```bash
/context_load
```

2. Check file contents:
```bash
cat .extn_aider/temp/context_backup/context_file.json
```

3. Verify file structure:
```bash
python -m json.tool context_file.json
```

## Future Improvements

Planned enhancements:
- Partial context restoration
- Context merging capability
- Enhanced validation options
- Progress indicators
- Conflict resolution
- Backup verification

## Contributing

Guidelines for enhancing this command:
1. Maintain backward compatibility
2. Add comprehensive validation
3. Update documentation
4. Include relevant tests
5. Handle edge cases
6. Add error recovery