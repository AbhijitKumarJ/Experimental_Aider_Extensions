# Unofficial and experimental Aider Extension

Experimental Custom extensions for the Aider AI coding assistant.
The purpose of this repository is to experiment with possible new features and suggest to aider contributor to add based on their judgement.
Do not consider this in any way related to official distribution of aider.

## Important Notice

This is just for experimentation and not for serious use. If you want to use these files, 
please verify the code yourself and experiment with it before using it to any work.



Project Layout:
```
./
├── main.py           # New simple runner
└── custom_aider/
    ├── __init__.py
    ├── monkey_patch.py
    ├── custom_aider_main.py
    ├── custom_coder.py
    ├── commands_registry.py
    └── commands/
        ├── __init__.py
        ├── git_commands.py
        └── utility_commands.py
```


## Usage

Run the extended version of aider: 

```bash
python main.py
```

## New Commands

- `/glog`: Enhanced git log with branch graph and file stats
- `/files`: List files in chat with details
- `/stats`: Show statistics about files in chat

## Development

To add new commands:

1. Create a new module in `custom_aider/commands/`
2. Define command functions with docstrings
3. Register commands using `CommandsRegistry.register()`
```

To use this extension:

1. Clone/create the directory structure as shown above
2. Install the package in development mode:
```bash
pip install -e .
```

3. Run aider with the extensions:
```bash
aider-custom
```

This provides a clean, maintainable structure for extending aider with new commands. The CommandsRegistry manages registration and installation of commands, while the custom coder ensures proper initialization. Each command is well-documented and properly integrated with aider's existing functionality.

You can easily add more commands by creating new modules in the commands directory and registering them with the CommandsRegistry. The extension system is modular and type-safe, making it easy to maintain and extend further.