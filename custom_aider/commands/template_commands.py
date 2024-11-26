"""Command for loading parameterized command templates with default values"""

import os
import json
from pathlib import Path
from ..commands_registry import CommandsRegistry

class TemplateLoader:
    """Handles loading and parameterizing command templates"""
    
    def __init__(self, io):
        self.io = io
        self.templates_dir = Path.cwd() / '.extn_aider' / 'command_templates' / 'load_templated'
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
    def get_available_templates(self):
        """Return list of available template files"""
        templates = []
        if self.templates_dir.exists():
            templates = [f for f in self.templates_dir.glob('*.json') 
                        if f.is_file()]
        return templates
        
    def load_template(self, template_name):
        """Load a template file by name"""
        template_path = self.templates_dir / f"{template_name}.json"
        if not template_path.exists():
            self.io.tool_error(f"Template {template_name} not found")
            return None
            
        try:
            with open(template_path) as f:
                return json.load(f)
        except json.JSONDecodeError:
            self.io.tool_error(f"Invalid JSON in template {template_name}")
            return None
            
    def get_parameter_values(self, parameters):
        """Interactively collect parameter values from user.
        
        Parameters can be specified in two ways:
        1. Simple string: "param_name"
        2. Dict with default: {"name": "param_name", "default": "default_value"}
        """
        values = {}
        for param in parameters:
            # Handle both string params and dict params with defaults
            if isinstance(param, dict):
                param_name = param["name"]
                default = param.get("default", "")
            else:
                param_name = param
                default = ""
                
            # Build prompt with optional default value
            prompt = f"Enter value for {param_name}"
            if default:
                prompt += f" [{default}]"
            prompt += ": "
            
            value = self.io.prompt_ask(prompt, default=default)
            if value:
                values[param_name] = value
            elif default:
                values[param_name] = default 
            else:
                return None
        return values
        
    def format_commands(self, commands, param_values):
        """Format commands with parameter values"""
        formatted = []
        for cmd in commands:
            try:
                formatted.append(cmd.format(**param_values))
            except KeyError as e:
                self.io.tool_error(f"Missing parameter {e} in template")
                return None
        return formatted

def cmd_load_templated(self, args):
    """Load and execute a parameterized command template
    Usage: /load_templated <template_name>
    
    Load a template file from .extn_aider/command_templates/load_templated/<template_name>.json
    Prompts for parameter values and executes the commands.
    
    Template files should be JSON with this structure:
    {
        "parameters": [
            "simple_param",                              # Simple parameter
            {"name": "param_with_default", "default": "default_value"}  # Parameter with default
        ],
        "commands": [
            "/command1 {simple_param}",
            "/command2 {simple_param} {param_with_default}"
        ]
    }
    
    Example template (new_api.json):
    {
        "parameters": [
            {"name": "endpoint_name", "default": "users"},
            {"name": "http_method", "default": "GET"}
        ],
        "commands": [
            "/add api/{endpoint_name}.py",
            "/code Create a {http_method} endpoint at /{endpoint_name}"
        ]
    }
    
    Usage:
    > /load_templated new_api
    Enter value for endpoint_name [users]: products  
    Enter value for http_method [GET]: POST
    
    This will execute:
    /add api/products.py
    /code Create a POST endpoint at /products
    """
    if not args.strip():
        self.io.tool_error("Please specify a template name")
        return
        
    template_name = args.strip()
    loader = TemplateLoader(self.io)
    
    template = loader.load_template(template_name)
    if not template:
        templates = loader.get_available_templates()
        if templates:
            self.io.tool_output("\nAvailable templates:")
            for t in templates:
                self.io.tool_output(f"  {t.stem}")
        return
        
    param_values = loader.get_parameter_values(template.get('parameters', []))
    if not param_values:
        return
        
    commands = loader.format_commands(template.get('commands', []), param_values)
    if not commands:
        return
        
    # Execute each command
    for cmd in commands:
        if cmd.startswith('/'):
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

def completions_load_templated(self):
    """Completions for load_templated command"""
    loader = TemplateLoader(self.io)
    templates = loader.get_available_templates()
    return [t.stem for t in templates]
    
# Register the command
CommandsRegistry.register(
    "load_templated",
    cmd_load_templated,
    completions_load_templated
)