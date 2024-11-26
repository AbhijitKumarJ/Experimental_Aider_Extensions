"""Command for intelligent exploration of code history"""

import re
from datetime import datetime, timedelta
from pathlib import Path
from ..commands_registry import CommandsRegistry

class CodeHistorian:
    """Analyzes and presents code history intelligently"""
    
    def __init__(self, repo, io):
        self.repo = repo
        self.io = io
        
    def parse_time_period(self, time_spec):
        """Parse time specification into a start date"""
        if not time_spec:
            return None
            
        # Handle relative time periods
        if match := re.match(r'last\s+(\d+)\s+(day|month|year)s?', time_spec.lower()):
            number, unit = match.groups()
            number = int(number)
            # Use UTC for consistency with git timestamps
            now = datetime.now().replace(tzinfo=None)
            
            if unit == 'day':
                return now - timedelta(days=number)
            elif unit == 'month':
                return now - timedelta(days=number * 30)
            elif unit == 'year':
                return now - timedelta(days=number * 365)
                
        # Handle "before/after" references
        if match := re.match(r'(before|after)\s+(.+)', time_spec.lower()):
            direction, reference = match.groups()
            
            # Look for commit with reference in message
            for commit in self.repo.repo.iter_commits():
                if reference.lower() in commit.message.lower():
                    if direction == 'before':
                        return commit.authored_datetime
                    else:
                        return commit.authored_datetime
                        
        return None
        
    def get_file_history(self, filepath, since_date=None):
        """Get commit history for a specific file"""
        history = []
        try:
            commits = self.repo.repo.iter_commits(paths=filepath)
            for commit in commits:
                # Convert to naive datetime for comparison
                commit_date = commit.authored_datetime.replace(tzinfo=None)
                if since_date and commit_date < since_date:
                    continue
                    
                # Get diff for this file in this commit
                diff = commit.diff(commit.parents[0] if commit.parents else None)
                file_diff = next((d for d in diff if d.a_path == filepath or d.b_path == filepath), None)
                
                if file_diff:
                    history.append({
                        'commit': commit,
                        'diff': file_diff,
                        'date': commit.authored_datetime,
                        'author': commit.author.name,
                        'message': commit.message.strip()
                    })
        except Exception as e:
            self.io.tool_error(f"Error getting history: {e}")
            
        return history
        
    def find_related_changes(self, filepath, history):
        """Find related changes in other files"""
        related = {}
        base_name = Path(filepath).stem
        
        for entry in history:
            commit = entry['commit']
            
            # Look for related files changed in same commits
            for diff in commit.diff(commit.parents[0] if commit.parents else None):
                other_path = diff.a_path or diff.b_path
                if other_path != filepath:
                    # Check if file looks related
                    other_name = Path(other_path).stem
                    if (base_name in other_name or 
                        other_name in base_name or
                        'test' in other_path.lower()):
                        related[other_path] = related.get(other_path, 0) + 1
                        
        return related
        
    def analyze_changes(self, filepath, since_date=None):
        """Analyze evolution of code in a file"""
        history = self.get_file_history(filepath, since_date)
        if not history:
            return None
            
        # Find related files
        related = self.find_related_changes(filepath, history)
        
        # Group changes by type
        features = []
        bugs = []
        tests = []
        refactors = []
        other = []
        
        for entry in history:
            msg = entry['message'].lower()
            if 'feat' in msg or 'add' in msg or 'new' in msg:
                features.append(entry)
            elif 'fix' in msg or 'bug' in msg or 'issue' in msg:
                bugs.append(entry)
            elif 'test' in msg:
                tests.append(entry)
            elif 'refactor' in msg or 'clean' in msg:
                refactors.append(entry)
            else:
                other.append(entry)
                
        return {
            'history': history,
            'related_files': related,
            'features': features,
            'bugs': bugs, 
            'tests': tests,
            'refactors': refactors,
            'other': other
        }
        
    def format_results(self, results, filepath):
        """Format analysis results into readable output"""
        if not results:
            return "No history found for the specified criteria."
            
        output = []
        
        # Overview section
        output.append(f"\nCode Evolution Analysis for: {filepath}")
        output.append("=" * 50)
        
        # Timeline summary
        output.append("\nTimeline Summary:")
        output.append("-" * 20)
        first = results['history'][-1]['date']
        last = results['history'][0]['date']
        total = len(results['history'])
        output.append(f"First change: {first.strftime('%Y-%m-%d')}")
        output.append(f"Latest change: {last.strftime('%Y-%m-%d')}")
        output.append(f"Total changes: {total}")
        
        # Feature development
        if results['features']:
            output.append("\nFeature Development:")
            output.append("-" * 20)
            for entry in results['features']:
                date = entry['date'].strftime('%Y-%m-%d')
                output.append(f"{date} - {entry['message'].split('\n')[0]}")
                
        # Bug fixes
        if results['bugs']:
            output.append("\nBug Fixes:")
            output.append("-" * 20)
            for entry in results['bugs']:
                date = entry['date'].strftime('%Y-%m-%d')
                output.append(f"{date} - {entry['message'].split('\n')[0]}")
                
        # Test changes
        if results['tests']:
            output.append("\nTest Development:")
            output.append("-" * 20)
            for entry in results['tests']:
                date = entry['date'].strftime('%Y-%m-%d')
                output.append(f"{date} - {entry['message'].split('\n')[0]}")
                
        # Related files
        if results['related_files']:
            output.append("\nCommonly Changed Together:")
            output.append("-" * 20)
            for file, count in sorted(results['related_files'].items(), 
                                    key=lambda x: x[1], reverse=True)[:5]:
                output.append(f"{file} ({count} times)")
                
        # Contributors
        contributors = {}
        for entry in results['history']:
            contributors[entry['author']] = contributors.get(entry['author'], 0) + 1
            
        output.append("\nContributors:")
        output.append("-" * 20)
        for author, count in sorted(contributors.items(), 
                                  key=lambda x: x[1], reverse=True):
            output.append(f"{author}: {count} changes")
            
        return "\n".join(output)

def cmd_timemachine(self, args):
    """Intelligent exploration of code history
    Usage: /timemachine <function/feature> [--when time_period]
    
    Beyond simple git history, shows:
    - When and why code evolved
    - Related bug fixes over time  
    - Feature development timeline
    - Key commits that modified behavior
    - Contributors and their changes
    - Test changes that accompanied code changes
    
    Examples:
    /timemachine login_flow --when "last 3 months"
    /timemachine payment.py --when "before refactor"
    /timemachine database.init --when "after bug #123"
    
    Like having a historian explain how your code evolved.
    """
    if not args.strip():
        self.io.tool_error("Please specify what to analyze")
        return
        
    if not self.coder.repo:
        self.io.tool_error("No git repository found")
        return
        
    # Parse arguments
    parts = args.split('--when')
    target = parts[0].strip()
    when = parts[1].strip() if len(parts) > 1 else None
    
    # Initialize historian
    historian = CodeHistorian(self.coder.repo, self.io)
    
    # Get date range if specified
    since_date = historian.parse_time_period(when) if when else None
    
    # Find target file/path
    found = False
    for fname in self.coder.get_all_relative_files():
        if (target in fname or
            target == Path(fname).stem or 
            target in Path(fname).stem):
            
            self.io.tool_output(f"\nAnalyzing history of {fname}...")
            results = historian.analyze_changes(fname, since_date)
            output = historian.format_results(results, fname)
            self.io.tool_output(output)
            found = True
            
    if not found:
        self.io.tool_error(
            f"Could not find any files matching '{target}'. "
            "Try using a more specific path or filename."
        )

def completions_timemachine(self):
    """Provide completions for timemachine command"""
    # Get list of files
    files = []
    if self.coder.repo:
        files = self.coder.get_all_relative_files()
        
    # Add common time periods
    time_periods = [
        'last 3 months',
        'last 6 months', 
        'last year',
        'last 2 years'
    ]
    
    completions = []
    
    # Add file completions
    for f in files:
        name = f
        stem = Path(f).stem
        completions.append(name)
        completions.append(stem)
        # Add with time periods
        for period in time_periods:
            completions.append(f"{name} --when {period}")
            completions.append(f"{stem} --when {period}")
            
    return sorted(set(completions))

# Register command
CommandsRegistry.register(
    "timemachine",
    cmd_timemachine,
    completions_timemachine
)
