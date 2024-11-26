"""Commands for showing and saving context information"""

import time
import webbrowser
from datetime import datetime
from pathlib import Path

from ..commands_registry import CommandsRegistry

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html>
<head>
<title>Aider Chat Context - {timestamp}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; color: #333; }}
.container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); }}
.header {{ border-bottom: 2px solid #eee; margin-bottom: 20px; padding-bottom: 10px; }}
.section {{ margin-bottom: 30px; }}
.file-content {{ background: #f8f8f8; padding: 15px; border-radius: 5px; overflow-x: auto; font-family: "Consolas", "Monaco", monospace; }}
.chat-message {{ margin: 10px 0; padding: 10px; border-radius: 5px; }}
.user-message {{ background: #e3f2fd; border-left: 4px solid #2196f3; }}
.assistant-message {{ background: #f5f5f5; border-left: 4px solid #9e9e9e; }}
.system-message {{ background: #fff3e0; border-left: 4px solid #ff9800; }}
.repo-map {{ background: #f1f8e9; border-left: 4px solid #8bc34a; }}
pre {{ margin: 0; padding: 10px; overflow-x: auto; }}
.metadata {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 20px; }}
.metadata-item {{ background: #fff; padding: 15px; border-radius: 5px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); }}
.file-list {{ list-style: none; padding: 0; }}
.file-list li {{ padding: 5px 0; }}
.stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }}
</style>
</head>
<body>
<div class="container">
{content}
</div>
</body>
</html>
"""

def escape_html(text):
    """Escape HTML special characters to their HTML entities"""
    return (str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;"))

def format_messages(messages):
    """Format chat messages into HTML with proper escaping"""
    html = ""
    for msg in messages:
        role = msg.get('role', '')
        content = msg.get('content', '')
        
        # Skip empty messages
        if not content:
            continue
            
        css_class = f"{role}-message chat-message"
        
        # Special handling for system messages that look like part of the repo map
        if role == "user" and "Here are summaries of some files present in my git repo" in content:
            css_class = "repo-map chat-message"
        
        html += f'<div class="{escape_html(css_class)}">\n'
        html += f'<strong>{escape_html(role.upper())}</strong>\n'
        html += f'<pre>{escape_html(content)}</pre>\n'
        html += '</div>\n'
        
    return html

def get_file_stats(coder):
    """Get statistics about files in chat"""
    stats = {'total_files': 0, 'total_lines': 0, 'total_chars': 0}
    file_details = []
    
    for fname in coder.get_inchat_relative_files():
        try:
            path = Path(coder.abs_root_path(fname))
            if path.exists():
                content = path.read_text()
                lines = len(content.splitlines())
                chars = len(content)
                
                stats['total_files'] += 1
                stats['total_lines'] += lines
                stats['total_chars'] += chars
                
                file_details.append({
                    'name': fname,
                    'size': path.stat().st_size,
                    'lines': lines,
                    'chars': chars
                })
        except Exception:
            continue
            
    return stats, file_details

def cmd_showcontext(self, args):
    """Save and display current chat context as HTML
    Usage: /showcontext
    
    Saves the current chat context including files, messages, and metadata 
    as a formatted HTML file and opens it in the default browser.
    Files are saved in .extn_aider/context/ with timestamps.
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create context directory
    context_dir = Path.cwd() / '.extn_aider' / 'temp' /'context'
    context_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate content
    content = []
    
    # Header
    content.append('<div class="header">')
    content.append(f'<h1>Aider Chat Context - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</h1>')
    content.append('</div>')
    
    # Metadata section
    content.append('<div class="metadata section">')
    
    # Model info
    content.append('<div class="metadata-item">')
    content.append('<h3>Model Information</h3>')
    content.append(f'<p>Main Model: {escape_html(self.coder.main_model.name)}</p>')
    content.append(f'<p>Edit Format: {escape_html(self.coder.edit_format)}</p>')
    if self.coder.main_model.weak_model and self.coder.main_model.weak_model != self.coder.main_model:
        content.append(f'<p>Weak Model: {escape_html(self.coder.main_model.weak_model.name)}</p>')
    content.append('</div>')
    
    # Files in chat
    content.append('<div class="metadata-item">')
    content.append('<h3>Files in Chat</h3>')
    stats, file_details = get_file_stats(self.coder)
    content.append('<div class="stats">')
    content.append(f'<div>Total Files: {stats["total_files"]}</div>')
    content.append(f'<div>Total Lines: {stats["total_lines"]:,}</div>')
    content.append(f'<div>Total Chars: {stats["total_chars"]:,}</div>')
    content.append('</div>')
    content.append('<ul class="file-list">')
    for file in sorted(file_details, key=lambda x: x['name']):
        size_kb = file['size'] / 1024
        content.append(
            f'<li>{file["name"]} ({size_kb:.1f}KB, {file["lines"]:,} lines)</li>'
        )
    content.append('</ul>')
    content.append('</div>')
    
    # Git info if available
    if self.coder.repo:
        content.append('<div class="metadata-item">')
        content.append('<h3>Git Information</h3>')
        try:
            repo = self.coder.repo.repo
            branch = repo.active_branch.name
            commit = repo.head.commit
            content.append(f'<p>Branch: {escape_html(branch)}</p>')
            content.append(f'<p>Last Commit: {escape_html(commit.hexsha[:7])}</p>')
            content.append(f'<p>Author: {escape_html(str(commit.author))}</p>')
            content.append(f'<p>Date: {escape_html(str(commit.committed_datetime))}</p>')
        except Exception as e:
            content.append(f'<p>Error getting git info: {escape_html(str(e))}</p>')
        content.append('</div>')
    
    content.append('</div>')  # End metadata section
    
    # Chat history
    content.append('<div class="section">')
    content.append('<h2>Chat History</h2>')
    messages = (self.coder.done_messages + self.coder.cur_messages)
    content.append(format_messages(messages))
    content.append('</div>')
    
    # Files content
    content.append('<div class="section">')
    content.append('<h2>File Contents</h2>')
    for fname in sorted(self.coder.get_inchat_relative_files()):
        content.append(f'<h3>{escape_html(fname)}</h3>')
        try:
            path = Path(self.coder.abs_root_path(fname))
            file_content = path.read_text()
            content.append('<div class="file-content">')
            content.append(f'<pre>{escape_html(file_content)}</pre>')
            content.append('</div>')
        except Exception as e:
            content.append(f'<p>Error reading file: {escape_html(str(e))}</p>')
    content.append('</div>')
    
    # Generate full HTML
    html = HTML_TEMPLATE.format(
        timestamp=timestamp,
        content='\n'.join(content)
    )
    
    # Save the file
    output_file_name = f'context_{timestamp}_AiderContext.html'
    output_file = context_dir / output_file_name
    output_file.write_text(html, encoding="utf-8")
    
    self.io.tool_output(f"\nSaved context to {output_file}")
    
    # Open in browser
    try:
        webbrowser.open(output_file.as_uri())
        self.io.tool_output("Opened in default browser")
    except Exception as e:
        self.io.tool_error(f"Error opening browser: {e}")
        self.io.tool_output(f"You can manually open: {output_file}")

# Register commands
CommandsRegistry.register("showcontext", cmd_showcontext)