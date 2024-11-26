"""Generate project structure with cross-platform path handling"""
from pathlib import Path
import os

PARAMS = {
    "project_name": "myapp",
    "components": ["web", "api", "worker"],  # Project components
    "config_format": "yaml",                # yaml or env
    "add_docker": True,                     # Add Docker support
    "python_version": "3.9"                 # Python version to use
}

def create_dir_structure(base_path, dirs):
    """Helper to create directory commands"""
    commands = []
    for dir_name in dirs:
        dir_path = base_path / dir_name
        
        # Create directory
        os.makedirs(dir_path, exist_ok=True)
        # Create __init__.py in each Python package directory
        if not any(part.startswith('.') for part in dir_path.parts):
            commands.append(f"/add {str(dir_path / '__init__.py')}")
    return commands

def generate_commands(params):
    """Generate commands with proper path handling"""
    commands = []
    
    # Use Path for proper cross-platform path handling
    project_root = Path(params["project_name"])
    
    # Create project directory
    os.makedirs(project_root, exist_ok=True)
    
    # Define standard directories every project needs
    standard_dirs = [
        "docs",
        "tests",
        "scripts"
    ]
    
    # Add component-specific directories
    for component in params["components"]:
        standard_dirs.append(str(project_root / component))
        
    # Create directory structure
    commands.extend(create_dir_structure(project_root, standard_dirs))
    
    # Add configuration based on format
    if params["config_format"] == "yaml":
        config_path = project_root / "config.yaml"
        commands.extend([
            f"/add {str(config_path)}",
            "/code Create YAML configuration template"
        ])
    else:
        env_path = project_root / ".env.example"
        commands.extend([
            f"/add {str(env_path)}",
            "/code Create environment variables template"
        ])
    
    # Add Docker support if requested
    if params["add_docker"]:
        docker_files = [
            project_root / "Dockerfile",
            project_root / ".dockerignore",
            project_root / "docker-compose.yml"
        ]
        for docker_file in docker_files:
            commands.extend([
                f"/add {str(docker_file)}",
                f"/code Setup {docker_file.name} for Python {params['python_version']}"
            ])
    
    # Add CI configuration
    github_dir = project_root / ".github" / "workflows"
    os.makedirs(github_dir, exist_ok=True)
    
    commands.extend([
        f"/add {str(github_dir / 'tests.yml')}",
        "/code Create GitHub Actions workflow for testing"
    ])
    
    # Add common project files
    common_files = [
        ("README.md", "Create project README with setup instructions"),
        ("requirements.txt", "Add project dependencies"),
        (".gitignore", "Add Python .gitignore"),
        ("setup.py", "Create setup.py for package installation")
    ]
    
    for filename, desc in common_files:
        file_path = project_root / filename
        commands.extend([
            f"/add {str(file_path)}",
            f"/code {desc}"
        ])
    
    return commands
