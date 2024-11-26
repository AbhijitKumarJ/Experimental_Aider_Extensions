"""Generate CRUD API endpoints with cross-platform path handling"""
from pathlib import Path
import os

PARAMS = {
    "resource_name": "users",     # Name of the resource (eg: users, products)
    "operations": "crud",         # Which operations to include (c=create, r=read, etc)
    "use_auth": False,           # Add authentication
    "add_tests": False,          # Generate test files
    "base_dir": "src"           # Base directory for generated files
}

def generate_commands(params):
    """Generate commands with proper path handling"""
    commands = []
    resource = params["resource_name"]
    base = Path(params["base_dir"])
    
    # Create directory structure using platform-safe paths
    model_path = base / "models" / f"{resource}.py"
    route_path = base / "routes" / f"{resource}.py"
    
    # Create directories if they don't exist
    os.makedirs(base / "models", exist_ok=True)
    os.makedirs(base / "routes", exist_ok=True)

    # Convert paths to strings with proper separators
    commands.extend([
        f"/add {str(model_path)}",
        f"/add {str(route_path)}"
    ])
    
    # Create model class
    commands.append(
        f"/code Create a {resource} model class with SQLAlchemy"
    )
    
    # Add requested CRUD operations
    ops = params["operations"].lower()
    for op in ops:
        if op == 'c':
            create_cmd = f"Add POST endpoint for creating {resource}"
            if params["use_auth"]:
                create_cmd += " with @require_auth decorator"
            commands.append(f"/code {create_cmd}")
            
        elif op == 'r':
            commands.append(f"/code Add GET endpoints for listing and retrieving {resource}")
            
        elif op == 'u':
            update_cmd = f"Add PUT endpoint for updating {resource}"
            if params["use_auth"]:
                update_cmd += " with ownership verification"
            commands.append(f"/code {update_cmd}")
            
        elif op == 'd':
            commands.append(f"/code Add DELETE endpoint for {resource}")
    
    # Add tests if requested
    if params["add_tests"]:
        # Set up test infrastructure

        # Create test directory
        test_dir = Path("tests")
        os.makedirs(test_dir, exist_ok=True)
        
        # Create test files
        test_path = test_dir / f"test_{resource}.py"
        fixture_path = test_dir / "conftest.py"
        
        commands.extend([
            f"/add {str(test_path)}",
            f"/add {str(fixture_path)}",
            f"/code Create pytest fixtures and test cases for {resource} endpoints"
        ])
    
    # Add route registration
    init_path = base / "routes" / "__init__.py"
    commands.extend([
        f"/add {str(init_path)}",
        f"/code Register {resource} routes in Flask blueprint"
    ])
        
    return commands
