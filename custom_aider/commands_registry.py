from typing import Callable, Dict, Optional, List
import inspect

class CommandsRegistry:
    """A registry for custom aider commands"""
    _commands: Dict[str, Callable] = {}
    _completions: Dict[str, Callable] = {}
    _descriptions: Dict[str, str] = {}
    
    @classmethod
    def register(cls, name: str, handler: Callable, completions: Optional[Callable] = None) -> None:
        """Register a command handler and optional completions"""
        print(f"Registering command: {name}")  # Debug print
        
        if not callable(handler):
            raise TypeError("Command handler must be callable")
            
        # Store command docstring as description
        if handler.__doc__:
            cls._descriptions[name] = inspect.cleandoc(handler.__doc__)
            
        cmd_name = f"cmd_{name}"
        cls._commands[cmd_name] = handler
        print(f"Registered command {cmd_name}")  # Debug print
        
        if completions:
            if not callable(completions):
                raise TypeError("Completions must be callable")
            cls._completions[f"completions_{name}"] = completions
            print(f"Registered completions for {name}")  # Debug print

    @classmethod
    def install_commands(cls, commands_instance) -> None:
        """Install all registered commands on a Commands instance"""
        print(f"Installing {len(cls._commands)} commands...")  # Debug print
        
        for name, func in cls._commands.items():
            if hasattr(commands_instance.__class__, name):
                print(f"Warning: Command {name} already exists")
                continue
                
            try:
                setattr(commands_instance.__class__, name, func)
                print(f"Installed command: {name}")  # Debug print
            except Exception as e:
                print(f"Error installing command {name}: {e}")
                
        for name, func in cls._completions.items():
            if not hasattr(commands_instance.__class__, name):
                setattr(commands_instance.__class__, name, func)
                print(f"Installed completions: {name}")  # Debug print

        print("Finished installing commands")  # Debug print

        
    @classmethod
    def list_commands(cls) -> List[str]:
        """List all registered command names"""
        return [name[4:] for name in cls._commands.keys()]  # Strip cmd_ prefix
        
    @classmethod
    def get_command(cls, name: str) -> Optional[Callable]:
        """Get a command by name"""
        return cls._commands.get(f"cmd_{name}")
        
    @classmethod
    def get_description(cls, name: str) -> str:
        """Get command description"""
        return cls._descriptions.get(name, "No description available")
        
    @classmethod
    def remove_command(cls, name: str) -> None:
        """Remove a registered command"""
        cls._commands.pop(f"cmd_{name}", None)
        cls._completions.pop(f"completions_{name}", None)
        cls._descriptions.pop(name, None)

    @classmethod
    def clear(cls) -> None:
        """Clear all registered commands"""
        cls._commands.clear()
        cls._completions.clear()
        cls._descriptions.clear()