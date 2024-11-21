import sys
from pathlib import Path
from aider.main import main as aider_main
from .commands_registry import CommandsRegistry
import importlib

def load_command_modules():
    """Dynamically load all command modules"""
    print("Loading command modules...")  # Debug output
    commands_dir = Path(__file__).parent / "commands"
    if not commands_dir.exists():
        print(f"Commands directory not found: {commands_dir}")  # Debug output
        return
        
    # Exclude __init__.py and files starting with _
    command_files = [
        f for f in commands_dir.glob("*.py")
        if not f.name.startswith("_") and f.name != "__init__.py"
    ]
    
    for command_file in command_files:
        module_name = f"custom_aider.commands.{command_file.stem}"
        try:
            importlib.import_module(module_name)
            print(f"Loaded command module: {module_name}")
        except Exception as e:
            print(f"Error loading command module {module_name}: {e}")

def initialize_custom_aider():
    """Initialize the custom aider environment"""
    # First override the Coder class
    import aider.coders as coders
    from .custom_coder import CustomCoder
    coders.Coder = CustomCoder
    
    # Then load command modules to register commands
    load_command_modules()
    
    # Log loaded commands
    commands = CommandsRegistry.list_commands()
    print(f"Loaded custom commands: {', '.join(commands)}")

def custom_main():
    """Run custom aider with extensions"""
    try:
        initialize_custom_aider()
        return aider_main()
    except Exception as e:
        print(f"Error in custom aider: {e}")
        raise

if __name__ == "__main__":
    custom_main()