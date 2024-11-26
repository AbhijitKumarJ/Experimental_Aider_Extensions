"""Generate microservice structure with cross-platform path handling"""
from pathlib import Path
import os

PARAMS = {
    "service_name": "user-service",
    "components": ["api", "worker", "scheduler"],
    "message_queue": "rabbitmq",
    "monitoring": False,
    "base_dir": "services",           # Base directory for all services
    "config_format": "yaml",          # yaml or env
    "add_docker": True               # Add Docker support
}

def create_component_structure(base_path, component, config_format):
    """Helper to create component directory structure"""
    commands = []
    component_dir = base_path / component    
    # Create directories if they don't exist
    os.makedirs(component_dir, exist_ok=True)

    # Common files for all components
    common_files = [
        component_dir / "__init__.py",
        component_dir / "main.py",
        component_dir / "utils.py"
    ]
    
    # Add configuration file
    if config_format == "yaml":
        common_files.append(component_dir / "config.yaml")
    else:
        common_files.append(component_dir / ".env.example")
    
    # Add all files
    for file_path in common_files:
        commands.append(f"/add {str(file_path)}")
    
    return commands

def generate_commands(params):
    """Generate commands with proper path handling"""
    commands = []
    
    # Set up base service path
    service_path = Path(params["base_dir"]) / params["service_name"]
    
    # Create base service directory
    os.makedirs(service_path, exist_ok=True)
    
    # Create service level structure
    service_files = [
        service_path / "__init__.py",
        service_path / "README.md",
        service_path / "requirements.txt"
    ]
    
    # Add service level files
    for file_path in service_files:
        commands.append(f"/add {str(file_path)}")
        
    # Process each component
    for component in params["components"]:
        # Add component structure
        commands.extend(
            create_component_structure(service_path, component, params["config_format"])
        )
        
        # Add component-specific files
        if component == "api":
            api_paths = [
                service_path / "api" / "routes",
                service_path / "api" / "models",
                service_path / "api" / "schemas",
            ]
            for api_path in api_paths:
                commands.append(f"/add {str(api_path / '__init__.py')}")
                
        elif component == "worker":
            worker_paths = [
                service_path / "worker" / "tasks",
                service_path / "worker" / "processors"
            ]
            for worker_path in worker_paths:
                commands.append(f"/add {str(worker_path / '__init__.py')}")
                
        elif component == "scheduler":
            scheduler_paths = [
                service_path / "scheduler" / "jobs",
                service_path / "scheduler" / "triggers"
            ]
            for scheduler_path in scheduler_paths:
                commands.append(f"/add {str(scheduler_path / '__init__.py')}")
    
    # Add message queue configuration if multiple components
    if len(params["components"]) > 1:
        queue_config = service_path / "queue"
        os.makedirs(queue_config, exist_ok=True)

        commands.extend([
            f"/add {str(queue_config / '__init__.py')}",
            f"/add {str(queue_config / 'connection.py')}",
            f"/code Set up {params['message_queue']} connection handling"
        ])
    
    # Add monitoring if requested
    if params["monitoring"]:
        monitoring_dir = service_path / "monitoring"
        os.makedirs(monitoring_dir, exist_ok=True)

        monitoring_files = [
            monitoring_dir / "metrics.py",
            monitoring_dir / "prometheus.yml",
            monitoring_dir / "grafana" / "dashboards" / "service.json"
        ]
        for monitor_path in monitoring_files:
            commands.extend([
                f"/add {str(monitor_path)}",
                f"/code Add {monitor_path.name} for {params['service_name']} monitoring"
            ])
    
    # Add Docker support
    if params["add_docker"]:
        docker_files = [
            service_path / "Dockerfile",
            service_path / "docker-compose.yml",
            service_path / ".dockerignore"
        ]
        for docker_path in docker_files:
            commands.extend([
                f"/add {str(docker_path)}",
                f"/code Create {docker_path.name} for {params['service_name']}"
            ])
    
    # Add tests
    test_dir = service_path / "tests"
    test_types = ["unit", "integration"]
    
    for test_type in test_types:
        type_dir = test_dir / test_type
        os.makedirs(type_dir, exist_ok=True)

        commands.extend([
            f"/add {str(type_dir / '__init__.py')}",
            f"/add {str(type_dir / 'conftest.py')}"
        ])
        
        # Add component-specific tests
        for component in params["components"]:
            test_file = type_dir / f"test_{component}.py"
            commands.extend([
                f"/add {str(test_file)}",
                f"/code Create {test_type} tests for {component}"
            ])
    
    # Add CI/CD configuration
    github_dir = service_path / ".github" / "workflows"
    os.makedirs(github_dir, exist_ok=True)
    
    commands.extend([
        f"/add {str(github_dir / 'test.yml')}",
        f"/add {str(github_dir / 'deploy.yml')}",
        "/code Create GitHub Actions workflows for testing and deployment"
    ])
    
    return commands
