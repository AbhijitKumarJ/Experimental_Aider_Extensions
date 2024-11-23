"""Command for interactive code explanation with HTML output"""
import os
import re
import ast
import webbrowser
from pathlib import Path
from datetime import datetime
from jinja2 import Template

from ..commands_registry import CommandsRegistry

# Get template directory
TEMPLATE_DIR = Path(__file__).parent.parent / 'gui' / 'templates' / 'cmd_explain_tmpl'

class CodeAnalyzer:
    """Analyzes Python code using AST"""
    
    def __init__(self, code_text):
        self.code_text = code_text
        self.tree = ast.parse(code_text)
        
    def find_target(self, target_name):
        """Find a specific function or class definition"""
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if node.name == target_name:
                    return self.analyze_node(node)
        return None
        
    def analyze_node(self, node):
        """Analyze a specific AST node"""
        analysis = {
            'name': node.name,
            'type': self._get_node_type(node),
            'docstring': ast.get_docstring(node) or '',
            'source': self._get_node_source(node),
            'lineno': node.lineno
        }
        
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            analysis.update(self._analyze_function(node))
        elif isinstance(node, ast.ClassDef):
            analysis.update(self._analyze_class(node))
            
        return analysis
        
    def _get_node_type(self, node):
        if isinstance(node, ast.AsyncFunctionDef):
            return 'async function'
        elif isinstance(node, ast.FunctionDef):
            return 'function'
        elif isinstance(node, ast.ClassDef):
            return 'class'
        return 'unknown'
        
    def _get_node_source(self, node):
        """Get source code for a node"""
        return ast.unparse(node)
        
    def _analyze_function(self, node):
        """Analyze a function definition"""
        args = []
        defaults = []
        
        for arg in node.args.args:
            args.append(arg.arg)
            
        if node.args.defaults:
            defaults = [ast.unparse(default) for default in node.args.defaults]
            
        return {
            'args': args,
            'defaults': defaults,
            'body_info': self._analyze_body(node)
        }
        
    def _analyze_class(self, node):
        """Analyze a class definition"""
        methods = []
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.append(self.analyze_node(item))
                
        return {
            'methods': methods,
            'bases': [ast.unparse(base) for base in node.bases],
            'body_info': self._analyze_body(node)
        }
        
    def _analyze_body(self, node):
        """Analyze function/class body"""
        info = {
            'has_loops': False,
            'has_conditionals': False,
            'calls': [],
            'line_count': len(node.body)
        }
        
        for item in ast.walk(node):
            if isinstance(item, (ast.For, ast.While)):
                info['has_loops'] = True
            elif isinstance(item, ast.If):
                info['has_conditionals'] = True
            elif isinstance(item, ast.Call) and hasattr(item.func, 'id'):
                info['calls'].append(item.func.id)
                
        return info

class HTMLExplanationGenerator:
    """Generates HTML explanation for code analysis"""
    
    @staticmethod
    def generate_control_flow(analysis):
        """Generate Mermaid diagram showing control flow"""
        mermaid = ["graph TD"]
        
        if analysis['type'] in ('function', 'async function'):
            # Function flow
            mermaid.append(f"    Start[Start] --> Args[Process Arguments]")
            
            if analysis['body_info']['has_conditionals']:
                mermaid.append("    Args --> Conditions{Conditions}")
                mermaid.append("    Conditions -->|True| Process[Process]")
                mermaid.append("    Conditions -->|False| Alt[Alternative]")
                mermaid.append("    Process --> End[Return]")
                mermaid.append("    Alt --> End")
            else:
                mermaid.append("    Args --> Process[Process]")
                mermaid.append("    Process --> End[Return]")
                
        elif analysis['type'] == 'class':
            # Class structure
            mermaid.append(f"    C[{analysis['name']}]")
            for method in analysis.get('methods', []):
                mermaid.append(f"    C --> {method['name']}[{method['name']}()]")
                
        return "\n".join(mermaid)

    @staticmethod
    def generate_html(analysis, level='basic'):
        """Generate complete HTML document"""
        # Load template files
        with open(TEMPLATE_DIR / 'base_template.html') as f:
            template = Template(f.read())
            
        with open(TEMPLATE_DIR / 'style.css') as f:
            styles = f.read()
            
        with open(TEMPLATE_DIR / 'script.js') as f:
            scripts = f.read()
        
        # Prepare template context
        context = {
            'name': analysis['name'],
            'type': analysis['type'],
            'docstring': analysis['docstring'],
            'source': analysis['source'],
            'lineno': analysis['lineno'],
            'styles': styles,
            'scripts': scripts,
            'flow_diagram': HTMLExplanationGenerator.generate_control_flow(analysis),
            'line_count': analysis['body_info']['line_count'],
            'has_loops': analysis['body_info']['has_loops'],
            'has_conditionals': analysis['body_info']['has_conditionals'],
            'calls': analysis['body_info'].get('calls', [])
        }
        
        # Add function-specific context
        if analysis['type'] in ('function', 'async function'):
            args = analysis.get('args', [])
            defaults = analysis.get('defaults', [])
            
            # Add default values to args
            sig_parts = []
            default_offset = len(args) - len(defaults)
            for i, arg in enumerate(args):
                if i >= default_offset and defaults:
                    sig_parts.append(f"{arg}={defaults[i - default_offset]}")
                else:
                    sig_parts.append(arg)
                    
            context['signature'] = f"def {analysis['name']}({', '.join(sig_parts)}):"
            context['args'] = args
            
        # Generate HTML using template
        return template.render(**context)

def cmd_explain(self, args):
    """Interactive code explanation
    Usage: /explain <function/class> [--level basic/deep/eli5]
    
    Creates an interactive HTML view that lets you:
    - Click to expand/collapse explanation sections
    - Toggle between abstraction levels
    - See animated control flow diagrams
    - Get real examples from the codebase
    """
    if not args.strip():
        self.io.tool_error("Please specify what to explain")
        return
        
    # Parse arguments
    parts = args.strip().split()
    target = parts[0]
    level = "basic"  # default level
    
    if len(parts) > 1 and parts[1].startswith('--level='):
        level = parts[1].split('=')[1]
        if level not in ('basic', 'deep', 'eli5'):
            self.io.tool_error("Invalid level. Use: basic, deep, or eli5")
            return
            
    # Look for the target in files
    found = False
    for fname in self.coder.get_inchat_relative_files():
        try:
            if not fname.endswith('.py'):
                continue
                
            path = Path(self.coder.abs_root_path(fname))
            content = path.read_text()
            
            analyzer = CodeAnalyzer(content)
            analysis = analyzer.find_target(target)
            
            if analysis:
                found = True
                self.io.tool_output(f"\nAnalyzing {target} from {fname}...")
                
                # Generate HTML
                html = HTMLExplanationGenerator.generate_html(analysis, level)
                
                # Save HTML file
                output_dir = Path.cwd() / '.aider' / 'explanations'
                output_dir.mkdir(parents=True, exist_ok=True)
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_file = output_dir / f"explanation_{target}_{timestamp}.html"
                
                output_file.write_text(html, encoding='utf-8')
                self.io.tool_output(f"\nSaved explanation to {output_file}")
                
                # Open in browser
                try:
                    webbrowser.open(output_file.as_uri())
                    self.io.tool_output("Opened in default browser")
                except Exception as e:
                    self.io.tool_error(f"Error opening browser: {e}")
                    self.io.tool_output(f"You can manually open: {output_file}")
                break
                
        except Exception as e:
            self.io.tool_error(f"Error processing {fname}: {e}")
            continue
            
    if not found:
        self.io.tool_error(f"Could not find {target} in any Python files")

def completions_explain(self):
    """Provide completions for explain command"""
    completions = []
    
    # Scan files for function and class definitions
    for fname in self.coder.get_inchat_relative_files():
        try:
            if not fname.endswith('.py'):
                continue
                
            path = Path(self.coder.abs_root_path(fname))
            content = path.read_text()
            
            # Use AST to find all functions and classes
            try:
                analyzer = CodeAnalyzer(content)
                for node in ast.walk(analyzer.tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        name = node.name
                        if not name.startswith('_'):  # Skip private definitions
                            completions.append(name)
                            # Add --level options
                            completions.extend([
                                f"{name} --level=basic",
                                f"{name} --level=deep",
                                f"{name} --level=eli5"
                            ])
            except SyntaxError:
                # Fall back to regex for files with syntax errors
                for match in re.finditer(r'(?:def|class)\s+([a-zA-Z_]\w*)', content):
                    name = match.group(1)
                    if not name.startswith('_'):
                        completions.append(name)
                        # Add --level options
                        completions.extend([
                            f"{name} --level=basic",
                            f"{name} --level=deep",
                            f"{name} --level=eli5"
                        ])
                        
        except Exception as e:
            if self.coder.verbose:
                self.io.tool_error(f"Error getting completions from {fname}: {e}")
            continue
            
    return sorted(set(completions))  # Remove duplicates

# Register the command with completions
CommandsRegistry.register("explain", cmd_explain, completions_explain)