# Context Backup Command for Aider

This module provides functionality to create backup copies of Aider chat contexts in JSON format. It allows you to save the current state of your chat, including model information, files in context, and conversation history.

## Overview

The context backup command creates point-in-time snapshots of your Aider chat session, storing them as JSON files for later reference or restoration.

## Features

- Creates timestamped backups of chat context
- Stores model information, files, and messages
- Customizable backup filenames
- JSON format for easy parsing and portability
- Organized storage in project-specific directory

## Command Usage

### Basic Command
```bash
/context_backup
```
Creates a backup with default filename prefix "aider_context"

### Custom Filename Prefix
```bash
/context_backup myproject
```
Creates a backup with custom prefix "myproject"

## Backup Contents

The backup JSON file includes:
- Timestamp of backup
- Current model name
- List of files in chat
- Complete message history (both done and current messages)

Example backup JSON structure:
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
      "content": "Response message"
    }
  ]
}
```

## Storage Location

Backups are stored in the project's `.extn_aider` directory:
```
.extn_aider/
└── temp/
    └── context_backup/
        ├── aider_context_20241126_212001.json
        └── myproject_20241126_213045.json
```

## Implementation Details

### Filename Format
- Prefix: User-provided or "aider_context"
- Timestamp: YYYY-MM-DD_HH_MM_SS
- Extension: .json
- Example: `myproject_20241126_212001.json`

### Error Handling
The command handles various error conditions:
- Directory creation failures
- File writing errors
- JSON serialization issues
- Encoding problems

## Usage Tips

1. Create regular backups during long sessions
2. Use meaningful prefix names for easier identification
3. Verify backups after creation
4. Clean up old backups periodically

## Example Workflow

```bash
# Start of project session
/context_backup project_start

# After major changes
/context_backup after_refactor

# Before ending session
/context_backup project_end
```

## Best Practices

1. **Regular Backups**
   - Create backups before major changes
   - Backup after significant progress
   - Backup before ending sessions

2. **Organization**
   - Use descriptive prefix names
   - Maintain a backup naming convention
   - Document backup contents externally if needed

3. **Maintenance**
   - Review backups periodically
   - Remove unnecessary backups
   - Verify backup integrity

## Technical Notes

### Path Handling
- Uses `pathlib.Path` for cross-platform compatibility
- Creates directories recursively as needed
- Uses UTF-8 encoding for file writing

### JSON Serialization
- Uses `json.dump` with indentation
- Handles circular references
- Preserves Unicode characters

## Troubleshooting

### Common Issues

1. **Backup Creation Fails**
   - Check directory permissions
   - Verify disk space
   - Ensure valid filename prefix

2. **Missing Content**
   - Verify chat state before backup
   - Check file encodings
   - Ensure all messages are included

3. **File Size Issues**
   - Monitor backup sizes
   - Check for large messages
   - Consider cleaning chat history

### Debug Steps

1. Verify backup directory exists:
   ```bash
   ls -l .extn_aider/temp/context_backup/
   ```

2. Check backup file contents:
   ```bash
   cat .extn_aider/temp/context_backup/latest_backup.json
   ```

3. Verify file permissions:
   ```bash
   ls -l .extn_aider/temp/context_backup/*.json
   ```

## Integration with Other Commands

The context backup command works well with:
- `/context_show` - For viewing current context
- `/context_load` - For restoring from backups
- `/context_create` - For creating new contexts

## Future Improvements

Planned enhancements:
- Compression options for large backups
- Backup rotation policies
- Backup verification tools
- Cloud storage integration
- Backup diffing capabilities

## Contributing

When working on this command:
1. Maintain backwards compatibility
2. Add comprehensive error handling
3. Update documentation for changes
4. Include relevant tests
5. Handle all edge cases