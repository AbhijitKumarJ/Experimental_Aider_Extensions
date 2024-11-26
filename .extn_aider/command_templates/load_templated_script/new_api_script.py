"""Generate API endpoints with cross-platform path handling"""
from pathlib import Path
import os

PARAMS = {
    "endpoint_name": "users",
    "http_method": "GET",
    "response_type": "json",
    "extra_validation": False,
    "api_version": "v1",          # API version for URL prefix
    "base_dir": "api"         # Base directory for API files
}

def generate_commands(params):
    """Generate commands with proper path handling"""
    commands = []
    
    # Set up paths using Path for cross-platform compatibility
    base_path = Path(params["base_dir"])
    version_path = base_path / params["api_version"]
    endpoint_dir = version_path / params["endpoint_name"]

    # Create directory structure
    os.makedirs(version_path, exist_ok=True)
    os.makedirs(endpoint_dir, exist_ok=True)
    
    # Create endpoint structure
    files_to_create = [
        endpoint_dir / "__init__.py",
        endpoint_dir / "routes.py",
        endpoint_dir / "models.py",
        endpoint_dir / "schemas.py"
    ]

    if params["extra_validation"]:
        files_to_create.append(endpoint_dir / "validators.py")

    # Add all required files
    for file_path in files_to_create:
        commands.append(f"/add {str(file_path)}")
    
    # Generate route code
    route_cmd = (
        f"Create a {params['http_method']} endpoint at "
        f"/{params['api_version']}/{params['endpoint_name']} "
        f"that returns {params['response_type']}"
    )
    commands.append(f"/code {route_cmd}")
    
    # Add schema and model
    commands.extend([
        f"/code Create Pydantic schema for {params['endpoint_name']} endpoint",
        f"/code Create SQLAlchemy model for {params['endpoint_name']}"
    ])
    
    # Add validation if requested
    if params["extra_validation"]:
        commands.append(
            f"/code Add input validation for {params['endpoint_name']} endpoint"
        )
    
    # Add tests
    test_dir = Path("tests") / "api" / params["api_version"]
    test_file = test_dir / f"test_{params['endpoint_name']}.py"

    # Create test directory if it doesn't exist
    os.makedirs(test_dir, exist_ok=True)
    
    commands.extend([
        f"/add {str(test_file)}",
        f"/code Create tests for {params['endpoint_name']} endpoint"
    ])
    
    # Add route registration in API init
    api_init = version_path / "__init__.py"
    commands.extend([
        f"/add {str(api_init)}",
        f"/code Register {params['endpoint_name']} routes in API"
    ])
    
    # Update OpenAPI/Swagger documentation
    docs_dir = Path("docs") / "api"
    os.makedirs(docs_dir, exist_ok=True)
    
    swagger_file = docs_dir / f"{params['api_version']}.yaml"
    commands.extend([
        f"/add {str(swagger_file)}",
        f"/code Update OpenAPI documentation for {params['endpoint_name']} endpoint"
    ])
    
    return commands
