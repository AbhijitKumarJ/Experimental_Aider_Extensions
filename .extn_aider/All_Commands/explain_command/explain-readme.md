# Explain Command for Aider

This module provides interactive code explanation functionality with HTML visualization. It analyzes Python code using AST (Abstract Syntax Tree) and generates navigable HTML reports with control flow diagrams.

## Features

- Interactive HTML visualization of code components
- Analysis of functions and classes
- Control flow diagrams using Mermaid
- Multiple visualization levels (basic/deep/eli5)
- Syntax highlighted source code
- Statistics and metrics
- Cross-platform path handling

## Command Usage

```bash
/explain <function/class> [--level basic/deep/eli5]

# Examples
/explain MyClass
/explain process_data --level=deep
/explain calculate_stats --level=eli5
```

## Implementation Components

### 1. CodeAnalyzer Class

Analyzes Python code using AST:

- Function/class detection
- Control flow analysis
- Argument analysis
- Call graph creation
- Statistics collection

```python
class CodeAnalyzer:
    def __init__(self, code_text):
        self.code_text = code_text
        self.tree = ast.parse(code_text)
```

Key methods:
- `find_target()` - Locates specific function/class
- `analyze_node()` - Deep analysis of AST node  
- `_analyze_function()` - Function-specific analysis
- `_analyze_class()` - Class-specific analysis

### 2. HTMLExplanationGenerator Class

Generates interactive HTML visualization:

- Tab-based interface
- Control flow diagrams
- Statistics display
- Source code highlighting

```python
class HTMLExplanationGenerator:
    @staticmethod 
    def generate_html(analysis, level='basic'):
        # Generate complete HTML document
```

Key methods:
- `generate_control_flow()` - Creates Mermaid diagrams
- `generate_html()` - Produces final HTML report

### 3. Template System

Uses Jinja2 templates for HTML generation:

```
cmd_explain_tmpl/
├── base_template.html  - Main HTML template
├── style.css          - CSS styling
└── script.js          - JavaScript functionality 
```

Template features:
- Tab navigation
- Code highlighting
- Collapsible sections
- Interactive diagrams

## HTML Report Structure

### 1. Overview Tab
- Basic information
- Purpose description
- Function signature
- Statistics overview

### 2. Details Tab  
- Implementation details
- Control structures
- Function calls
- Line counts

### 3. Source Tab
- Complete source code
- Syntax highlighting
- Code navigation

### 4. Flow Tab
- Mermaid control flow diagram
- Visual code structure
- Execution paths

## Technical Details

### AST Analysis 

The command analyzes Python code using these AST elements:
- Functions (FunctionDef, AsyncFunctionDef)
- Classes (ClassDef)
- Control flow (If, For, While)
- Function calls (Call)

### Code Storage

Reports are stored in:
```
.extn_aider/
└── temp/
    └── explain/
        └── explanation_<name>_<timestamp>.html
```

### Dependencies

Required packages:
- `ast` - Python standard library
- `jinja2` - Template system
- `webbrowser` - Report display 
- `pygments` - Code highlighting

## Usage Examples

### 1. Basic Function Analysis

```bash
/explain calculate_total

# Analyzes:
# - Function signature
# - Parameters
# - Control flow
# - Return values
```

### 2. Deep Class Analysis

```bash
/explain DataProcessor --level=deep

# Analyzes:
# - Class structure
# - Methods
# - Inheritance
# - Dependencies
```

### 3. Simple Explanation

```bash
/explain validate_input --level=eli5

# Provides:
# - Simple explanation
# - Basic flow
# - Key concepts
```

## Integration Points

The command integrates with:

1. **File System**
   - Reads Python source files
   - Saves HTML reports
   - Handles paths cross-platform

2. **Web Browser**
   - Opens reports automatically
   - Falls back to manual opening

3. **Aider Core**
   - Accesses in-chat files
   - Uses IO system
   - Provides completions

## Command Completion

Provides intelligent completions:
- Python functions/classes in chat
- Level options (basic/deep/eli5)
- Skips private definitions (_*)

```python
def completions_explain(self):
    """Provide completions for explain command"""
    for fname in self.coder.get_inchat_relative_files():
        if fname.endswith('.py'):
            # Find Python symbols
```

## Error Handling

The command handles various errors:

1. **File Errors**
   - File not found
   - Read permission denied
   - Unicode decode errors

2. **Parse Errors**
   - Invalid Python syntax
   - AST parse failures
   - Symbol not found

3. **Render Errors**
   - Template errors
   - Browser launch failures
   - File write errors

## Best Practices

When using this command:

1. **Code Organization**
   - Keep functions/classes focused
   - Use meaningful names
   - Add docstrings

2. **File Management**
   - Clean old reports
   - Use appropriate paths
   - Handle temp files

3. **Error Recovery**
   - Check error messages
   - Verify file paths
   - Review browser settings

## Troubleshooting

Common issues and solutions:

1. **Symbol Not Found**
   - Check file is in chat
   - Verify symbol name
   - Check symbol is public

2. **Report Not Generated**
   - Check file permissions
   - Verify Python version
   - Check disk space

3. **Browser Issues**
   - Check default browser
   - Try manual file open
   - Verify file path

## Contributing

When working with this command:
1. Follow AST patterns
2. Maintain template structure
3. Handle errors gracefully
4. Document changes
5. Test with various code styles

## Important Notes

1. The command only analyzes Python files
2. The report uses local browser resources
3. Large files may take longer to analyze
4. Private symbols are skipped by default
5. Reports are temporary unless saved