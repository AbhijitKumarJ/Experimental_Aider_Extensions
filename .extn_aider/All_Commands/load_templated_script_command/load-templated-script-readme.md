# Load Templated Script Command for Aider

A powerful extension for loading and executing Python-based command templates. This module allows you to create complex, dynamic command sequences using Python scripts, with a focus on proper cross-platform path handling.

## Features

- Execute command templates defined in Python scripts
- Cross-platform path handling using pathlib
- Interactive parameter collection
- Rich template examples included
- Boolean and string parameter support
- Comprehensive error handling
- Command completion for script names

## Installation

1. Templates are stored in `.extn_aider/command_templates/load_templated_script/` 
2. Several example templates are included:
   - `crud_api_script.py`
   - `new_api_script.py` 
   - `project_structure_script.py`
   - `test_suite_script.py`
   - `microservices_script.py`

## Usage

Basic command usage:
```bash
/load_templated_script <template_name>
```

Example:
```bash
> /load_templated_script project_structure
Enter value for project_name [myapp]: myservice
Enter enable use_auth? [y/N]: y
```

## Script Template Structure

Each template script should define:

1. `PARAMS` - Dictionary of parameter names and default values
2. `generate_commands()` - Function that returns list of commands

Basic template structure:
```python
from pathlib import Path
import os

PARAMS = {
    "param1": "default1",
    "param2": True  # Boolean parameter
}

def generate_commands(params):
    commands = []
    # Add commands here
    return commands
```

## Path Handling Best Practices

All templates should use proper cross-platform path handling:

1. Use pathlib.Path for paths:
```python
project_dir = Path(params["project_name"])
src_dir = project_dir / "src"
config_file = src_dir / "config.yaml"
```

2. Convert paths to strings when needed:
```python
commands.append(f"/add {str(config_file)}")
```

3. Create directories safely:
```python 
os.makedirs(src_dir, exist_ok=True)
```

4. Use .resolve() for absolute paths:
```python
abs_path = config_file.resolve()
```

5. Check path existence:
```python
if not path.exists():
    return f"Error: Path not found: {path}"
```

## Example Templates

### 1. Project Structure Generator
```python
from pathlib import Path
import os

PARAMS = {
    "project_name": "myapp",
    "components": ["web", "api"],
    "use_docker": True
}

def generate_commands(params):
    commands = []
    # Use Path for cross-platform paths
    project_root = Path(params["project_name"])
    
    # Create component directories
    for component in params["components"]:
        component_dir = project_root / component
        
        # Add component files
        commands.extend([
            f"/add {str(component_dir / '__init__.py')}",
            f"/add {str(component_dir / 'main.py')}"
        ])
    
    if params["use_docker"]:
        commands.extend([
            f"/add {str(project_root / 'Dockerfile')}",
            "/code Create Dockerfile for the project"
        ])
        
    return commands
```

### 2. Test Suite Generator
```python
from pathlib import Path
import glob

PARAMS = {
    "source_dir": "src",
    "exclude_patterns": [".*", "__pycache__"]
}

def find_python_files(source_dir, exclude_patterns):
    """Find Python files respecting excludes"""
    source_path = Path(source_dir)
    py_files = []
    
    for py_file in source_path.rglob("*.py"):
        if not any(py_file.match(pat) for pat in exclude_patterns):
            py_files.append(py_file)
    
    return py_files

def generate_commands(params):
    commands = []
    source_files = find_python_files(
        params["source_dir"],
        params["exclude_patterns"]
    )
    
    # Create test files with parallel structure 
    for source_file in source_files:
        test_file = Path("tests") / source_file.relative_to(params["source_dir"])
        test_file = test_file.parent / f"test_{test_file.name}"
        
        commands.extend([
            f"/add {str(test_file)}", 
            f"/code Create tests for {source_file}"
        ])
    
    return commands
```

## Path Handling Guidelines

1. **Cross-platform Compatibility**
   - Always use Path instead of string concatenation
   - Use / operator to join paths
   - Convert to string only when needed
   - Use .resolve() for absolute paths
   - Use .relative_to() for relative paths

2. **Safe Directory Creation**
   - Always use os.makedirs with exist_ok=True
   - Create parent directories before adding files
   - Check directory existence when needed

3. **Path Manipulation**
   - Use path.name for filenames
   - Use path.parent for parent directories
   - Use path.suffix for extensions
   - Use path.stem for names without extension

4. **File Operations**
   - Handle file read/write exceptions
   - Use proper encoding (usually utf-8)
   - Clean up temporary files

## Error Handling

The command handles these error conditions:
- Missing template files
- Invalid Python syntax
- Missing required attributes 
- Module import errors
- Command execution failures
- File operation errors

## Best Practices

1. **Template Organization**
   - Keep templates focused and modular
   - Document parameters clearly
   - Follow consistent naming
   - Test cross-platform behavior

2. **Parameter Design** 
   - Use descriptive names
   - Provide sensible defaults
   - Validate parameter values
   - Handle missing parameters

3. **Command Generation**
   - Order commands logically 
   - Handle dependencies
   - Validate file paths
   - Clean up on failure

4. **Testing**
   - Test on multiple platforms
   - Test with different parameters
   - Verify file operations
   - Check error handling

## Contributing

To contribute templates:

1. Use proper path handling
2. Test thoroughly on all platforms
3. Document clearly
4. Follow examples
5. Submit improvements

## Debugging Tips

1. Enable verbose output:
```python
if self.coder.verbose:
    print(f"Debug info: {value}")
```

2. Test path handling:
```python
# Print resolved paths
print(f"Absolute path: {path.resolve()}")
```

3. Check command generation:
```python
# Print commands before execution
for cmd in commands:
    print(f"Generated command: {cmd}")
```

## Support

If you encounter issues:

1. Check path handling
2. Verify parameters
3. Test commands individually
4. Check error messages
5. Verify template exists

## See Also

- [pathlib documentation](https://docs.python.org/3/library/pathlib.html)
- [os.path documentation](https://docs.python.org/3/library/os.path.html)
- Built-in templates in `.extn_aider/command_templates/load_templated_script/`
