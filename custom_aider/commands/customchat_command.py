"""Custom chat command with keyword expansion support"""

import json
from pathlib import Path

from ..commands_registry import CommandsRegistry

KEYWORDS_FILE = ".extn_aider.keywords.json"

def load_keywords(io, root="."):
    """Load keywords from the keywords JSON file"""
    try:
        keywords_path = Path(root) / '.extn_aider' / KEYWORDS_FILE
        if not keywords_path.exists():
            io.tool_error(f"Keywords file not found: {KEYWORDS_FILE}")
            return {}
            
        with open(keywords_path) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        io.tool_error(f"Invalid JSON in {KEYWORDS_FILE}: {e}")
        return {}
    except Exception as e:
        io.tool_error(f"Error reading {KEYWORDS_FILE}: {e}")
        return {}

def expand_keywords(text, keywords, io):
    """Replace @text-keyword patterns with their expansions"""
    import re
    
    # Find all @text- keywords
    pattern = r'@text-(\w+)'
    matches = re.finditer(pattern, text)
    
    # Track replacements and errors
    replacements = []
    missing_keywords = set()
    
    # Collect all replacements first
    for match in matches:
        keyword = match.group(1)
        if keyword in keywords:
            replacements.append((match.span(), keywords[keyword]))
        else:
            missing_keywords.add(keyword)
            
    # Report missing keywords
    if missing_keywords:
        io.tool_error("Unknown keywords:")
        for kw in sorted(missing_keywords):
            io.tool_error(f"  @text-{kw}")
        return None
        
    # Apply replacements in reverse order to not mess up positions
    expanded = text
    for (start, end), replacement in sorted(replacements, reverse=True):
        expanded = expanded[:start] + replacement + expanded[end:]
        
    if replacements:
        io.tool_output("\nExpanded message:")
        io.tool_output(expanded)
        io.tool_output("\nPress Enter to send or Ctrl-C to cancel...")
        try:
            input()
        except KeyboardInterrupt:
            return None
            
    return expanded

def cmd_customchat(self, args):
    """Enhanced chat with keyword substitution support
    Usage: /customchat <message>
    
    Your message can contain @text-keyword references that will be expanded
    based on definitions in .extn_aider.keywords.json.
    
    Example keywords file:
    {
        "api": "REST API with JSON responses",
        "tests": "Unit tests using pytest with mocking"
    }
    
    Example usage:
    /customchat Create @text-tests for the login function
    """
    if not args.strip():
        self.io.tool_error("Please provide a message")
        return
        
    # Load keywords
    keywords = load_keywords(self.io, root=self.coder.root)
    if not keywords:
        return
        
    # Expand keywords in message
    expanded = expand_keywords(args, keywords, self.io)
    if not expanded:
        return
        
    # Process based on current edit format
    edit_format = self.coder.edit_format
    
    if edit_format == "ask":
        return self.cmd_ask(expanded)
    elif edit_format == "architect":
        return self.cmd_architect(expanded)
    else:
        return self.cmd_code(expanded)

# Add completion support
def completions_customchat(self):
    """Provide completions for customchat command"""
    # Get document text before cursor
    # The completion engine automatically passes Document and CompleteEvent objects
    # We only care about text before cursor to find potential @text- pattern
    
    # Load keywords 
    keywords = load_keywords(self.io, root=self.coder.root) 
    if not keywords:
        return []

    # Filter and format completions
    completions = []
    for keyword in keywords:
        completions.append('@text-' + keyword)

    return sorted(completions)

# Register command with completions
CommandsRegistry.register("customchat", cmd_customchat, completions_customchat)