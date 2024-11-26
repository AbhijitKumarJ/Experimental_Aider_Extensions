"""Command for interactive context viewing and export"""

import os
import json
import webbrowser
from datetime import datetime
from pathlib import Path
from jinja2 import Template

from ..commands_registry import CommandsRegistry

# Get template directory
TEMPLATE_DIR = Path(__file__).parent.parent / 'gui' / 'templates' / 'cmd_context_create_tmpl'

def get_context_data(coder):
    """Gather all context data"""
    context_data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'model_info': {
            'name': coder.main_model.name,
            'edit_format': coder.edit_format
        },
        'files': [],
        'messages': [],
        'git_info': None
    }
    
    # Get file information
    for fname in coder.get_inchat_relative_files():
        try:
            path = Path(coder.abs_root_path(fname))
            if path.exists():
                content = path.read_text()
                context_data['files'].append({
                    'name': fname,
                    'size': path.stat().st_size,
                    'lines': len(content.splitlines()),
                    'content': content
                })
        except Exception:
            continue
            
    # Get chat messages
    messages = (coder.done_messages + coder.cur_messages)
    for msg in messages:
        context_data['messages'].append({
            'role': msg.get('role', ''),
            'content': msg.get('content', '')
        })
        
    # Get git info if available
    if coder.repo:
        try:
            repo = coder.repo.repo
            branch = repo.active_branch.name
            commit = repo.head.commit
            context_data['git_info'] = {
                'branch': branch,
                'commit_hash': commit.hexsha[:7],
                'author': str(commit.author),
                'date': str(commit.committed_datetime)
            }
        except Exception:
            pass
            
    return context_data

def cmd_context_create(self, args):
    """Create interactive context view with export capabilities
    Usage: /context_create
    
    Generates an HTML page showing all context elements:
    - Files in chat
    - Chat messages
    - Model information
    - Git status
    
    Features:
    - Checkbox to select/unselect items
    - Export selected items as JSON
    - Interactive expanding/collapsing sections
    """
    try:
        # Get context data
        context_data = get_context_data(self.coder)
        
        # Load template files
        with open(TEMPLATE_DIR / 'base_template.html') as f:
            template = Template(f.read())
            
        with open(TEMPLATE_DIR / 'style.css') as f:
            styles = f.read()
            
        with open(TEMPLATE_DIR / 'script.js') as f:
            scripts = f.read()
            
        # Generate HTML
        html = template.render(
            context=context_data,
            styles=styles,
            scripts=scripts
        )
        
        # Save the file
        output_dir = Path.cwd() / '.extn_aider' / 'context'
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = output_dir / f'context_view_{timestamp}.html'
        output_file.write_text(html, encoding='utf-8')
        
        self.io.tool_output(f"\nSaved context view to {output_file}")
        
        # Open in browser
        try:
            webbrowser.open(output_file.as_uri())
            self.io.tool_output("Opened in default browser")
        except Exception as e:
            self.io.tool_error(f"Error opening browser: {e}")
            self.io.tool_output(f"You can manually open: {output_file}")
            
    except Exception as e:
        self.io.tool_error(f"Error creating context view: {e}")

# Register the command
CommandsRegistry.register("context_create", cmd_context_create)