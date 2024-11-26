# Custom Chat Command for Aider

This module enhances Aider's chat interface with keyword expansion capabilities. It allows users to define keywords that expand into longer text snippets, making it easier to maintain consistent terminology and requirements across conversations.

## Features

- Keyword expansion using @text- prefix
- JSON-based keyword definitions
- Interactive confirmation of expansions
- Support for multiple editing modes
- Command completion for defined keywords
- Error handling for missing/invalid keywords

## Command Usage

```bash
/customchat <message>
```

The message can contain keywords prefixed with @text- that will be expanded based on definitions in `.extn_aider.keywords.json`.

### Example Usage

```bash
# Define keywords in .extn_aider.keywords.json:
{
    "api": "REST API with JSON responses",
    "tests": "Unit tests using pytest with mocking"
}

# Use in chat:
/customchat Create @text-tests for the login function
# Expands to: Create unit tests using pytest with mocking for the login function

/customchat Add @text-api endpoint for user registration
# Expands to: Add REST API with JSON responses endpoint for user registration
```

## Configuration

### Keyword File Structure
The command looks for `.extn_aider.keywords.json` in the `.extn_aider` directory:

```json
{
    "keyword1": "expansion text 1",
    "keyword2": "expansion text 2",
    ...
}
```

### File Location
```
.extn_aider/
└── .extn_aider.keywords.json
```

## Implementation Details

### Keyword Loading

```python
def load_keywords(io, root="."):
    """Load keywords from the keywords JSON file"""
    try:
        keywords_path = Path(root) / '.extn_aider' / KEYWORDS_FILE
        if not keywords_path.exists():
            io.tool_error(f"Keywords file not found: {KEYWORDS_FILE}")
            return {}
            
        with open(keywords_path) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        io.tool_error(f"Invalid JSON in {KEYWORDS_FILE}: {e}")
        return {}
```

### Keyword Expansion

```python
def expand_keywords(text, keywords, io):
    """Replace @text-keyword patterns with their expansions"""
    pattern = r'@text-(\w+)'
    matches = re.finditer(pattern, text)
    
    replacements = []
    missing_keywords = set()
    
    for match in matches:
        keyword = match.group(1)
        if keyword in keywords:
            replacements.append((match.span(), keywords[keyword]))
        else:
            missing_keywords.add(keyword)
```

### Command Integration

The command integrates with Aider's:
- Edit formats (whole, ask, architect)
- IO system for user interaction
- Command completion system
- Error handling framework

## Features Explained

### 1. Keyword Detection
- Uses regular expressions to find @text- prefixed keywords
- Validates keywords against JSON definitions
- Reports unknown keywords to user

### 2. Interactive Confirmation
- Shows expanded message before sending
- Allows cancellation with Ctrl-C
- Clear feedback about expansions

### 3. Command Completion
- Provides completions for defined keywords
- Auto-completes @text- prefix
- Sorted completion list

### 4. Error Handling
```python
# Examples of handled errors:
- Missing keywords file
- Invalid JSON format
- Unknown keywords
- File access issues
```

## Usage Examples

### 1. Simple Keyword Usage
```bash
/customchat Add @text-api for user authentication
```

### 2. Multiple Keywords
```bash
/customchat Create @text-tests for @text-api endpoints
```

### 3. With Different Edit Formats
```bash
# In ask mode
/customchat Explain how @text-api works

# In architect mode
/customchat Design @text-api structure
```

## Command Completion

The command provides intelligent completion support:

```python
def completions_customchat(self):
    """Provide completions for customchat command"""
    # Load keywords 
    keywords = load_keywords(self.io, root=self.coder.root) 
    if not keywords:
        return []

    # Format completions
    completions = []
    for keyword in keywords:
        completions.append('@text-' + keyword)

    return sorted(completions)
```

## Error Messages

The command provides clear error messages:

1. Missing Keywords File:
```
Error: Keywords file not found: .extn_aider.keywords.json
```

2. Invalid JSON:
```
Error: Invalid JSON in .extn_aider.keywords.json: Expecting property name
```

3. Unknown Keywords:
```
Unknown keywords:
  @text-unknown
```

## Best Practices

### 1. Keyword Organization
- Use descriptive keyword names
- Keep expansions focused and clear
- Group related keywords
- Document keyword purposes

### 2. Keyword File Management
```json
{
    "api": {
        "expansion": "REST API with JSON responses",
        "description": "Standard API format", 
        "category": "architecture"
    }
}
```

### 3. Usage Guidelines
- Use keywords consistently
- Update keywords regularly
- Back up keyword definitions
- Share keywords with team

## Technical Notes

1. **Pattern Matching**
   - Uses Python regex for keyword detection
   - Case-sensitive matching
   - Word boundary aware

2. **Text Processing**
   - Preserves original message structure
   - Handles multiple keywords per message
   - Maintains formatting

3. **Command Integration**
   - Supports all edit formats
   - Preserves chat context
   - Maintains command history

## Troubleshooting

Common issues and solutions:

1. **Keywords Not Expanding**
   - Check keywords file location
   - Verify JSON syntax
   - Confirm keyword spelling

2. **Command Not Found**
   - Verify command registration
   - Check command path
   - Confirm installation

3. **Completion Not Working**
   - Check keywords file
   - Verify file permissions
   - Review completion function

## Contributing

When working with this command:
1. Follow consistent keyword naming
2. Document keyword purposes
3. Test expansions thoroughly
4. Handle errors gracefully
5. Update completions
