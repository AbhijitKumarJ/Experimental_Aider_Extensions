"""Command for loading and executing script-based command templates"""

import os
import sys
import importlib.util
from pathlib import Path
from ..commands_registry import CommandsRegistry

def load_script_template(template_name):
    """Load a script template by name and return module"""
    try:
        # Find template directory
        templates_dir = Path.cwd() / '.extn_aider' / 'command_templates' / 'load_templated_script'
        script_path = templates_dir / f"{template_name}.py"

        if not script_path.exists():
            return None, f"Template {template_name} not found"

        # Load module from file
        spec = importlib.util.spec_from_file_location(template_name, script_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[template_name] = module
        spec.loader.exec_module(module)

        return module, None

    except Exception as e:
        return None, f"Error loading template: {str(e)}"

def get_parameter_values(io, params):
    """Collect parameter values interactively"""
    values = {}
    for name, default in params.items():
        if isinstance(default, bool):
            # Handle boolean parameters
            response = io.confirm_ask(
                f"Enable {name}?",
                default="y" if default else "n"
            )
            values[name] = response
        else:
            # Handle string parameters
            value = io.prompt_ask(
                f"Enter value for {name} [{default}]: ",
                default=str(default)
            )
            values[name] = value

    return values

def cmd_load_templated_script(self, args):
    """Load and execute a script-based command template
    Usage: /load_templated_script <template_name>
    
    Load a Python script template from .extn_aider/command_templates/load_templated_script/<template_name>.py.
    The script should define:
    1. PARAMS: dict of parameter names and default values
    2. generate_commands(params): function that returns list of commands
    
    Complex examples showing proper path handling:

    1. Basic Project Structure:
    ```python
    from pathlib import Path
    import os

    PARAMS = {
        "project_name": "myapp",
        "source_dir": "src"
    }
    
    def generate_commands(params):
        commands = []
        # Use Path for cross-platform paths
        project_root = Path(params["project_name"])
        src_dir = project_root / params["source_dir"]
        
        # Create directory structure
        for dir_name in ["models", "views", "controllers"]:
            dir_path = src_dir / dir_name
            commands.append(f"/add {str(dir_path / '__init__.py')}")
            
        # Add common files
        readme_path = project_root / "README.md"
        commands.extend([
            f"/add {str(readme_path)}",
            "/code Create project documentation"
        ])
        
        return commands
    ```

    2. Test File Generator:
    ```python
    from pathlib import Path
    import glob

    PARAMS = {
        "source_dir": "src",
        "exclude_patterns": [".*", "__pycache__"]
    }
    
    def find_python_files(source_dir, exclude_patterns):
        " ""Find Python files respecting excludes"" "
        source_path = Path(source_dir)
        py_files = []
        
        for py_file in source_path.rglob("*.py"):
            if not any(py_file.match(pat) for pat in exclude_patterns):
                py_files.append(py_file)
        
        return py_files
    
    def generate_commands(params):
        commands = []
        # Find source files
        source_files = find_python_files(
            params["source_dir"],
            params["exclude_patterns"]
        )
        
        # Create test files
        for source_file in source_files:
            # Generate parallel test structure
            test_file = Path("tests") / source_file.relative_to(params["source_dir"])
            test_file = test_file.parent / f"test_{test_file.name}"
            
            commands.extend([
                f"/add {str(test_file)}",
                f"/code Create tests for {source_file}"
            ])
            
        return commands
    ```

    3. Multi-component Application:
    ```python
    from pathlib import Path
    import os

    PARAMS = {
        "components": ["web", "api"],
        "config_type": "yaml"
    }
    
    def generate_commands(params):
        commands = []
        
        # Create component directories
        for component in params["components"]:
            component_dir = Path(component)
            
            # Add component files
            commands.extend([
                f"/add {str(component_dir / '__init__.py')}",
                f"/add {str(component_dir / 'main.py')}"
            ])
            
            # Add component config
            if params["config_type"] == "yaml":
                config_file = component_dir / "config.yaml"
            else:
                config_file = component_dir / ".env"
                
            commands.append(f"/add {str(config_file)}")
        
        return commands
    ```

    Key path handling tips:
    1. Use pathlib.Path for cross-platform compatibility
    2. Join paths with / operator: Path("base") / "subdir" / "file.py"
    3. Convert Path to string when needed: str(path)
    4. Use .resolve() for absolute paths
    5. Use .relative_to() for relative paths
    6. Check parts with path.parts or path.name
    7. Use .rglob() for recursive file finding
    8. Use .match() for pattern matching
    9. Handle parent directories: path.parent
    10. Create parallel directory structures
    """
    if not args.strip():
        self.io.tool_error("Please specify a template name")
        return

    template_name = args.strip()

    # Load the template module
    module, error = load_script_template(template_name)
    if error:
        self.io.tool_error(error)
        available = Path.cwd() / '.extn_aider' / 'command_templates' / 'load_templated_script'
        if available.exists():
            self.io.tool_output("\nAvailable templates:")
            for f in available.glob("*.py"):
                if not f.name.startswith("_"):
                    self.io.tool_output(f"  {f.stem}")
        return

    # Verify required attributes
    if not hasattr(module, 'PARAMS') or not hasattr(module, 'generate_commands'):
        self.io.tool_error(
            f"Template {template_name} must define PARAMS dict and generate_commands function"
        )
        return

    # Get parameter values
    params = get_parameter_values(self.io, module.PARAMS)
    if not params:
        return

    try:
        # Generate commands
        commands = module.generate_commands(params)
        if not commands:
            self.io.tool_error("Template generated no commands")
            return

        # Show commands that will be executed
        self.io.tool_output("\nCommands to execute:")
        for cmd in commands:
            self.io.tool_output(f"  {cmd}")

        if not self.io.confirm_ask("\nProceed with execution?", default="y"):
            return

        # Execute each command
        for cmd in commands:
            if cmd.startswith('/code '):
                # Strip the leading /code and dispatch code command
                cmd_args = cmd[5:].strip()
                # Treat as a message to send
                self.coder.send_message(cmd_args)
            elif cmd.startswith('/'):
                # Strip the leading / and dispatch command
                cmd_name, *cmd_args = cmd[1:].split(maxsplit=1)
                cmd_args = cmd_args[0] if cmd_args else ''

                handler_name = f"cmd_{cmd_name}"
                handler = getattr(self, handler_name, None)

                if handler:
                    handler(cmd_args)
                else:
                    self.io.tool_error(f"Unknown command: {cmd_name}")
            else:
                # Treat as a message to send
                self.coder.send_message(cmd)

    except Exception as e:
        self.io.tool_error(f"Error executing template: {str(e)}")

def completions_load_templated_script(self):
    """Provide completions for script templates"""
    templates_dir = Path.cwd() / '.extn_aider' / 'command_templates' / 'load_templated_script'
    if templates_dir.exists():
        return [f.stem for f in templates_dir.glob("*.py") 
                if not f.name.startswith("_")]
    return []

# Register the command
CommandsRegistry.register(
    "load_templated_script",
    cmd_load_templated_script,
    completions_load_templated_script
)