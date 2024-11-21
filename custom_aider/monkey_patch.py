"""Early monkey-patching of aider classes"""
import os
import sys
from pathlib import Path

def monkey_patch_aider():
    """Monkey patch aider classes before any aider imports"""
    # Add our custom_aider directory to the Python path
    custom_aider_dir = Path(__file__).parent
    if str(custom_aider_dir) not in sys.path:
        sys.path.insert(0, str(custom_aider_dir))
    
    # First import our custom coder
    from custom_aider.custom_coder import CustomCoder
    
    # Then patch aider's coders
    import aider.coders as coders
    coders.Coder = CustomCoder
    
    # Also patch the base coder module
    import aider.coders.base_coder
    aider.coders.base_coder.Coder = CustomCoder
    
    # Ensure commands directory is in path
    commands_dir = custom_aider_dir / "commands"
    os.makedirs(commands_dir, exist_ok=True)
    
    print("Custom aider classes loaded and patched")