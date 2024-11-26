"""Generate test suite with proper path handling"""
from pathlib import Path
import os
import glob

PARAMS = {
    "test_type": "unit",           # unit, integration, or e2e
    "source_dir": "src",           # Source code directory
    "exclude_patterns": [".*"],    # Glob patterns to exclude
    "test_lib": "pytest",          # Testing library
    "add_coverage": True           # Add coverage configuration
}

def find_python_files(source_dir, exclude_patterns):
    """Find Python files while respecting gitignore and exclude patterns"""
    source_path = Path(source_dir)
    py_files = []
    
    # Convert exclude patterns to absolute paths
    exclude_paths = set()
    for pattern in exclude_patterns:
        for path in source_path.rglob(pattern):
            exclude_paths.add(path.absolute())
    
    # Find all Python files
    for py_file in source_path.rglob("*.py"):
        # Skip files matching exclude patterns
        if not any(py_file.absolute() == ex_path for ex_path in exclude_paths):
            if not any(part.startswith('.') for part in py_file.parts):
                py_files.append(py_file.relative_to(source_path))
    
    return py_files

def generate_commands(params):
    """Generate test files and configuration"""
    commands = []
    
    # Create test directory structure
    test_base = Path("tests")
    test_type = params["test_type"]
    
    # Create test directory if it doesn't exist
    os.makedirs(test_base, exist_ok=True)

    # Define test directories based on type
    test_dirs = {
        "unit": [test_base / "unit"],
        "integration": [test_base / "integration", test_base / "fixtures"],
        "e2e": [
            test_base / "e2e",
            test_base / "e2e" / "pages",
            test_base / "e2e" / "fixtures"
        ]
    }
    
    # Create test directories
    for test_dir in test_dirs.get(test_type, []):
        os.makedirs(test_dir, exist_ok=True)
        commands.append(f"/add {str(test_dir / '__init__.py')}")
    
    # Create test configuration
    if params["test_lib"] == "pytest":
        config_files = [
            (test_base / "conftest.py", "Create pytest fixtures"),
            (Path("pytest.ini"), "Configure pytest options"),
        ]
        if params["add_coverage"]:
            config_files.append((
                Path(".coveragerc"),
                "Configure coverage settings with source and excludes"
            ))
    else:
        config_files = [
            (Path("unittest.cfg"), "Configure unittest settings")
        ]
    
    for config_file, desc in config_files:
        commands.extend([
            f"/add {str(config_file)}",
            f"/code {desc}"
        ])
    
    # Find source files and create corresponding tests
    source_files = find_python_files(params["source_dir"], params["exclude_patterns"])
    
    for source_file in source_files:
        # Create test file with same structure as source
        if test_type == "unit":
            test_file = test_base / "unit" / f"test_{source_file}"
        else:
            # For integration/e2e, group by module
            module_name = source_file.parts[0] if len(source_file.parts) > 1 else source_file.stem
            test_file = test_base / test_type / f"test_{module_name}.py"
        
        # Ensure parent directories exist
        commands.append(f"/add {str(test_file)}")
        
        # Add test content
        rel_path = os.path.relpath(source_file, params["source_dir"])
        if test_type == "unit":
            commands.append(
                f"/code Create unit tests for {rel_path} using {params['test_lib']}"
            )
        elif test_type == "integration":
            commands.append(
                f"/code Create integration tests for {module_name} module"
            )
        else:  # e2e
            commands.append(
                f"/code Create end-to-end tests for {module_name} functionality"
            )
    
    # Add test helpers
    helper_files = {
        "unit": [("helpers.py", "Create test helpers")],
        "integration": [
            ("docker_utils.py", "Create Docker test utilities"),
            ("db_utils.py", "Create database test utilities")
        ],
        "e2e": [
            ("selenium_utils.py", "Create Selenium test utilities"),
            ("page_objects.py", "Create page object base classes")
        ]
    }
    
    for helper_file, desc in helper_files.get(test_type, []):
        helper_path = test_base / "utils" / helper_file
        commands.extend([
            f"/add {str(helper_path)}",
            f"/code {desc}"
        ])
    
    return commands
