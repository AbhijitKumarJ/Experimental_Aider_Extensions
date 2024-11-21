"""Custom coder implementation with command registry support"""
import logging
from typing import Optional, ClassVar
from aider.coders.base_coder import Coder as BaseCoder
from .commands_registry import CommandsRegistry

logger = logging.getLogger(__name__)

class CustomCoder(BaseCoder):
    """Enhanced Coder with custom command support"""
    
    _current_coder: ClassVar[Optional['CustomCoder']] = None
    
    def __init__(self, *args, **kwargs):
        print("CustomCoder.__init__ called")  # Debug print
        super().__init__(*args, **kwargs)
    
    @classmethod
    def create(cls, *args, **kwargs):
        """Create a coder instance with custom commands"""
        print("CustomCoder.create called")  # Debug print
        
        # Create coder instance
        coder = super().create(*args, **kwargs)
        print(f"Created coder: {coder.__class__}")  # Debug print
        
        # Install custom commands
        if hasattr(coder, 'commands'):
            print(f"Found commands on coder") # Debug print
            registered_commands = CommandsRegistry.list_commands()
            print(f"Installing commands: {registered_commands}")  # Debug print
            CommandsRegistry.install_commands(coder.commands)
            print("Finished installing commands")  # Debug print
        else:
            print("No commands attribute found on coder")  # Debug print
            
        # Store reference
        cls._current_coder = coder
        return coder