"""Git-related command extensions"""

import subprocess
from datetime import datetime
from pathlib import Path

from ..commands_registry import CommandsRegistry

def cmd_glog(self, args):
    """Show pretty git log with branch graph and stats
    Usage: /glog [options]
    
    Options:
        -n N     Show last N commits (default: 10)
        --all    Show all branches
        --stat   Show changed files statistics
    """
    if not self.coder.repo:
        self.io.tool_error("No git repository found")
        return
        
    # Parse arguments
    num_commits = "10"
    show_all = False
    show_stats = False
    
    if args:
        parts = args.split()
        for i, part in enumerate(parts):
            if part == "-n" and i + 1 < len(parts):
                num_commits = parts[i + 1]
            elif part == "--all":
                show_all = True
            elif part == "--stat":
                show_stats = True
                
    cmd = [
        "git", "log",
        f"-n{num_commits}",
        "--graph",
        "--date=format:%Y-%m-%d %H:%M",
        "--pretty=format:%C(yellow)%h%C(reset) - %C(green)%ad%C(reset) %C(bold blue)%an%C(reset)%C(red)%d%C(reset)%n%s%n"
    ]
    
    if show_all:
        cmd.append("--all")
    if show_stats:
        cmd.append("--stat")
        
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            self.io.tool_output(result.stdout)
        else:
            self.io.tool_error(f"Git error: {result.stderr}")
    except Exception as e:
        self.io.tool_error(f"Error running git command: {e}")

def completions_glog(self):
    """Provide completions for glog command"""
    return ["--all", "--stat", "-n"]

# Register commands
CommandsRegistry.register("glog", cmd_glog, completions_glog)