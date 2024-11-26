# Load Templated Command for Aider

This module enhances Aider with the ability to load and execute parameterized command templates. It allows you to create reusable command sequences with customizable parameters.

## Features

- Load command templates from JSON files
- Support for default parameter values
- Interactive parameter collection
- Command completion for template names 
- Error handling and validation
- Support for both aider commands and chat messages

## Installation

1. The command will be available as part of your aider extension system
2. Template files are stored in `.extn_aider/command_templates/load_templated/`
3. Create your first template file (e.g. `new_api.json`) in the templates directory

## Usage

Basic usage:
```bash
/load_templated <template_name>
```

The command will:
1. Load the specified template file
2. Prompt for parameter values (showing defaults if available)
3. Execute the formatted commands

## Template Format

Templates are JSON files with the following structure:

```json
{
    "parameters": [
        "simple_param",                              
        {"name": "param_with_default", "default": "default_value"}  
    ],
    "commands": [
        "/command1 {simple_param}",
        "/command2 {simple_param} {param_with_default}"
    ]
}
```

### Parameters

Parameters can be specified in two ways:

1. Simple string - Required parameter without default:
   ```json
   "simple_param"
   ```

2. Object with default - Optional parameter with default value:
   ```json
   {
       "name": "param_name",
       "default": "default_value"
   }
   ```

### Commands

Commands can be:
- Aider commands (starting with `/`)
- Chat messages (without `/`)

Commands can reference parameters using `{parameter_name}` placeholders.

## Example Templates

### 1. New API Endpoint
```json
{
    "parameters": [
        {"name": "endpoint_name", "default": "users"},
        {"name": "http_method", "default": "GET"},
        {"name": "response_type", "default": "json"}
    ],
    "commands": [
        "/add api/{endpoint_name}.py",
        "/code Create a {http_method} endpoint at /{endpoint_name} that returns {response_type}"
    ]
}
```

Usage:
```
> /load_templated new_api
Enter value for endpoint_name [users]: products  
Enter value for http_method [GET]: POST
Enter value for response_type [json]:
```

### 2. New Test File
```json
{
    "parameters": [
        {"name": "module_name", "default": "users"},
        {"name": "test_type", "default": "unit"}
    ],
    "commands": [
        "/add tests/test_{module_name}.py",
        "/code Create {test_type} tests for the {module_name} module using pytest"
    ]
}
```

Usage:
```
> /load_templated new_test
Enter value for module_name [users]: auth
Enter value for test_type [unit]: integration
```

## Creating Your Own Templates

1. Create a new JSON file in `.extn_aider/command_templates/load_templated/`
2. Follow the template format shown above
3. Test it with the `/load_templated` command

Tips for creating templates:
- Use meaningful default values
- Keep parameters focused and minimal
- Use clear parameter names
- Consider command ordering
- Test templates thoroughly

## Command Help 

You can get help on the command at any time:
```bash
/help load_templated
```

## Error Handling

The command handles various error conditions:
- Missing template files 
- Invalid JSON in templates
- Missing required parameters
- Invalid parameter references
- Unknown aider commands

## Completion Support

The command provides completion support for:
- Template names when using the command
- You can see available templates with just:
  ```bash
  /load_templated
  ```

## Best Practices

1. **Template Organization:**
   - Use descriptive template names
   - Group related templates consistently 
   - Document templates well

2. **Parameter Design:**
   - Provide sensible defaults
   - Use clear parameter names
   - Keep parameter count reasonable

3. **Command Sequences:**
   - Order commands logically
   - Handle dependencies between commands
   - Consider error states

4. **Testing:**
   - Test templates with different inputs
   - Verify parameter expansion
   - Check command execution order

## Contributing

To contribute new templates or improvements:

1. Create useful templates
2. Test thoroughly
3. Share with the community
4. Submit improvements

## Limitations

- Templates must be valid JSON
- Parameter names should be valid Python identifiers
- Commands must be valid aider commands or chat messages

## Support

If you encounter any issues:
1. Check the command help: `/help load_templated` 
2. Review your template JSON syntax
3. Verify parameter names and references
4. Check command validity