# Enhanced Existing Commands

This module enhances several existing Aider commands by wrapping them with "z" prefix versions that add useful functionality while maintaining compatibility with the original commands.

## Overview

These enhanced commands provide additional features like:
- Retry support for web commands
- File validation for add/drop
- Git status and statistics
- Backup functionality
- Enhanced model comparison
- Voice recognition confidence checks

## Enhanced Commands

### Web Command (`/zweb`)

Enhanced version of `/web` that adds:
- Multiple retries on failure 
- Timing information
- Word count statistics
- Automatic content saving to `.extn_aider/temp/web/`

```bash
# Usage
> /zweb https://example.com

# Features
- Retries failed requests up to 2 times
- Shows fetch timing
- Displays word count
- Saves content to timestamped files
```

### Add Command (`/zadd`) 

Enhanced version of `/add` with:
- Git status display before adding
- File size tracking
- Change summary after adding

```bash
# Usage
> /zadd file1.py file2.py

# Features
- Shows git status before adding
- Tracks file sizes
- Shows what changed after adding
```

### Drop Command (`/zdrop`)

Enhanced version of `/drop` that adds:
- Confirmation prompt
- Automatic file backups
- Status feedback

```bash
# Usage 
> /zdrop file.py

# Features
- Asks for confirmation
- Creates backups in ~/.extn_aider/temp/backups
- Shows backup status
```

### Commit Command (`/zcommit`)

Enhanced version of `/commit` with:
- File statistics
- Enhanced commit messages
- Commit details display

```bash
# Usage
> /zcommit [message]

# Features
- Shows files to be committed with stats
- Adds file statistics to commit message
- Displays commit details after committing
```

### Model Command (`/zmodel`) 

Enhanced version of `/model` adding:
- Model comparison display
- Token and cost differences
- Info about changes

```bash
# Usage
> /zmodel gpt-4

# Features
- Compares old and new models
- Shows token limits
- Shows cost differences
```

### Clear Command (`/zclear`)

Enhanced version of `/clear` that adds:
- Chat history backup
- Markdown formatted backup files
- Timestamped backups

```bash
# Usage
> /zclear

# Features
- Backs up chat history before clearing
- Saves as markdown
- Creates timestamped backup files
```

### Voice Command (`/zvoice`)

Enhanced version of `/voice` with:
- Multiple recording attempts
- Transcription confirmation
- Retry support

```bash
# Usage
> /zvoice

# Features
- Allows multiple recording attempts
- Asks for transcription confirmation
- Retries on poor transcription
```

## Implementation Details

### Directory Structure

The backups and saves are stored in:
```
.extn_aider/
└── temp/
    ├── web/           # Saved web content
    ├── backups/       # File backups
    └── history_backups/ # Chat history backups
```

### File Naming

Files are saved with timestamps and descriptive names:
```
web/20241124_041612__http_example_com.txt
backups/myfile_py_20241124_041612
history_backups/chat_history_20241124_041612.md
```

### Error Handling

All enhanced commands include:
- Proper error messages
- Retries where appropriate
- Fallback behaviors
- Status feedback

## Extension Points

The enhanced commands demonstrate several ways to extend Aider:
1. Adding pre/post processing
2. Including backup functionality
3. Enhanced status reporting
4. File tracking and validation
5. Integration with git
6. Smart retries and confirmation

## Best Practices

When using these enhanced commands:

1. File Operations
   - Use `/zadd` when you want to see git status
   - Use `/zdrop` when you want automatic backups
   - Check `.extn_aider/temp/backups` for backed up files

2. Web Operations
   - Use `/zweb` for reliable web scraping
   - Check `.extn_aider/temp/web` for saved content
   - Look for timing info to diagnose issues

3. Git Operations
   - Use `/zcommit` for better commit messages
   - Check commit details after committing
   - Review file statistics when committing

4. Voice Operations
   - Use `/zvoice` for better transcription
   - Try multiple recordings if needed
   - Confirm transcription accuracy

## Utility Features

Common utilities used across commands:

### File Size Formatting
```python
def format_size(size):
    if size < 1024:
        return f"{size}B"
    elif size < 1024 * 1024:
        return f"{size/1024:.1f}KB"
    return f"{size/1024/1024:.1f}MB"
```

### Time Formatting
```python
def format_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
```

### Safe File Operations
```python
def safe_backup(path, backup_dir):
    try:
        # Create unique backup name
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        backup_path = backup_dir / f"{path.name}_{timestamp}"
        # Copy with metadata
        shutil.copy2(path, backup_path)
        return True
    except Exception:
        return False
```

## Configuration

The enhanced commands respect Aider configuration but add optional settings:

```yaml
# Enhanced command settings
retries: 2          # Number of retries for web/voice
backup: true        # Enable automatic backups
timestamps: true    # Add timestamps to backups
```

## Troubleshooting

Common issues and solutions:

1. Web Command Fails
   - Check internet connection
   - Verify URL is accessible
   - Look for saved content in web directory
   - Check retry count in output

2. Backup Issues
   - Verify directory permissions
   - Check disk space
   - Look for error messages
   - Check backup directory exists

3. Voice Issues
   - Test microphone
   - Try multiple attempts
   - Check transcription output
   - Verify audio settings

## Contributing

When enhancing these commands:

1. Follow the prefix convention (`z` prefix)
2. Maintain compatibility with original commands
3. Add useful features that make sense
4. Include proper error handling
5. Add appropriate feedback
6. Document new features
7. Test thoroughly

## See Also

- Main commands documentation
- Original command implementations
- Aider configuration guide
- Extension system documentation
