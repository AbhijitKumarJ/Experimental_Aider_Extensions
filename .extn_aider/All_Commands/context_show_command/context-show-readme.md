# Context Commands for Aider

This module provides functionality to visualize and analyze your Aider chat context in an interactive HTML format. It generates a comprehensive view of your chat session, including files, messages, model information, and Git status.

## Features

- Interactive HTML visualization of chat context
- File content preview and statistics
- Chat history with syntax highlighting
- Model and Git information display
- Message filtering and organization
- Export capabilities for selected content

## Command Usage

### Show Context
```bash
/context_show
```
Generates and displays an HTML report of the current chat context in your default browser.

## Generated HTML Report Features

### 1. Header Section
- Timestamp of report generation
- Model information (name, edit format)
- Quick actions buttons

### 2. Statistics Section
- Total files in chat
- Line counts and sizes
- Message statistics
- Git repository information

### 3. Files Section
- List of all files in chat
- File content previews
- Size and line count information
- Syntax-highlighted code display

### 4. Chat History Section
- Complete message history
- Role-based message coloring
- Collapsible message content
- Search/filter capabilities

### 5. Interactive Elements
- Collapsible sections
- Search functionality
- Select/Deselect All buttons
- Export selected content

## Storage Location

HTML reports are stored in the project's `.extn_aider` directory:
```
.extn_aider/
└── temp/
    └── context/
        └── context_view_20241126_212001.html
```

## HTML Report Structure

### CSS Classes and Styling
```css
.container   - Main container
.header      - Report header
.section     - Content sections
.file-item   - File display
.message     - Chat message
.user        - User message styling
.assistant   - Assistant message styling
.system      - System message styling
```

### JavaScript Features
- Dynamic content loading
- Interactive filtering
- Export functionality
- Clipboard integration

## Technical Implementation

### HTML Generation
- Uses Jinja2 templates
- Cross-browser compatible
- Responsive design
- Syntax highlighting support

### Content Processing
- File content sanitization
- HTML escaping
- Message formatting
- Git information extraction

## Usage Examples

### Basic Usage
```bash
# Generate and view context
/context_show

# Export selected content
# Use the "Export Selected" button in the HTML interface
```

### Integration with Git
```bash
# View context with Git history
/context_show
# Git information appears in the metadata section
```

### File Analysis
```bash
# View file statistics
/context_show
# Check the Statistics section
```

## Best Practices

1. **Regular Context Reviews**
   - Review context periodically
   - Check for unnecessary files
   - Monitor chat history size

2. **Content Organization**
   - Keep related files together
   - Use clear message structure
   - Maintain clean chat history

3. **Resource Management**
   - Clean up old HTML reports
   - Monitor storage usage
   - Export important contexts

## Template System

### Base Template
```html
<!DOCTYPE html>
<html>
<head>
    <title>Aider Chat Context - {{timestamp}}</title>
    <!-- Styles and Scripts -->
</head>
<body>
    <div class="container">
        <!-- Content Sections -->
    </div>
</body>
</html>
```

### Customizable Elements
- Color schemes
- Layout options
- Section organization
- Display preferences

## Troubleshooting

### Common Issues

1. **Report Generation Fails**
   - Check directory permissions
   - Verify template files
   - Check disk space

2. **Browser Display Issues**
   - Try different browsers
   - Clear browser cache
   - Check file permissions

3. **Missing Content**
   - Verify chat state
   - Check file access
   - Review Git connectivity

### Debug Steps

1. Check HTML file:
```bash
ls -l .extn_aider/temp/context/
```

2. Verify browser compatibility:
```bash
# Try alternative browsers
firefox context_view.html
chrome context_view.html
```

## Future Enhancements

Planned improvements:
- Additional visualization options
- Enhanced search capabilities
- Custom styling support
- PDF export option
- Real-time updates
- Collaborative features

## Integration Points

Works well with:
- `/context_backup` - For saving context state
- `/context_load` - For restoring contexts
- `/stats` - For detailed file analysis
- `/glog` - For Git history integration

## Security Notes

### Data Protection
- Local storage only
- No external requests
- Sanitized content display
- Safe file handling

### Browser Integration
- Local file protocol
- No remote resources
- Sandboxed execution
- Safe content rendering

## Performance Considerations

### Optimization Tips
1. Limit file sizes in context
2. Clean up old reports
3. Use efficient search patterns
4. Monitor resource usage

### Resource Management
- Disk space monitoring
- Memory efficient processing
- Browser resource usage
- Template caching

## Contributing

Guidelines for enhancing this command:
1. Follow template structure
2. Maintain cross-browser compatibility
3. Update documentation
4. Add relevant tests
5. Consider accessibility
6. Follow security best practices

## References

Related Documentation:
- Template System Guide
- HTML Report Structure
- Styling Guidelines
- JavaScript Features
- Browser Compatibility