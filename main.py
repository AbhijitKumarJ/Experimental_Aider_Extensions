#!/usr/bin/env python3
"""Direct runner for custom aider without installation"""
import os
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Apply patches before any aider imports
from custom_aider.monkey_patch import monkey_patch_aider
monkey_patch_aider()

# Now import and run custom main
from custom_aider.custom_aider_main import custom_main

if __name__ == "__main__":
    sys.exit(custom_main())