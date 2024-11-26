# Git Commands for Aider

Extensions to Aider's git functionality providing enhanced git log viewing and repository insights.

## Overview

The git commands module provides the `/glog` command which enhances git log viewing with:
- Commit graph visualization 
- Branch information
- Commit statistics
- Customizable output

## Commands

### /glog - Enhanced Git Log

```bash
/glog [options]
```

#### Options

- `-n N` - Show last N commits (default: 10)
- `--all` - Show all branches 
- `--stat` - Show changed files statistics

#### Examples

```bash
# Show last 10 commits with graph
/glog

# Show last 5 commits
/glog -n 5

# Show all branches
/glog --all

# Show commit stats
/glog --stat

# Combine options
/glog -n 5 --all --stat
```

#### Output Format

The command produces git log output with:

- Yellow commit hashes
- Green dates
- Bold blue author names
- Red branch/tag references
- Commit messages
- ASCII graph showing branch structure
- Optional file statistics

Example output:
```
* 1a2b3c4 - 2024-01-15 10:30 Bob Smith (HEAD -> main)
| Add user authentication
|
* 5d6e7f8 - 2024-01-14 16:45 Alice Jones (origin/main)
| Update dependencies
|
* 9b8a7c6 - 2024-01-13 14:20 Bob Smith
  Fix login bug
```

## Implementation Details

### Command Registration

The command is registered with Aider's command registry:

```python
CommandsRegistry.register("glog", cmd_glog, completions_glog)
```

### Command Function

Core implementation:
```python
def cmd_glog(self, args):
    # Parse arguments
    num_commits = "10"  # default
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
    
    # Build git command
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
```

### Command Completion

Provides completions for command options:

```python
def completions_glog(self):
    return ["--all", "--stat", "-n"]
```

## Error Handling

The command handles several error cases:

1. No git repository:
```python
if not self.coder.repo:
    self.io.tool_error("No git repository found")
    return
```

2. Git command errors:
```python
try:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        self.io.tool_output(result.stdout)
    else:
        self.io.tool_error(f"Git error: {result.stderr}")
except Exception as e:
    self.io.tool_error(f"Error running git command: {e}")
```

## Format Options

The command uses several git format options for better output:

- `--graph` - Show ASCII graph
- `--date=format:%Y-%m-%d %H:%M` - Custom date format
- Pretty format:
  - `%C(yellow)%h` - Yellow commit hash
  - `%C(green)%ad` - Green author date
  - `%C(bold blue)%an` - Bold blue author name
  - `%C(red)%d` - Red ref names
  - `%s` - Commit subject

## Usage Tips

1. View Recent History
```bash
# Last 5 commits
/glog -n 5

# Last 10 commits with stats
/glog --stat
```

2. Branch Analysis 
```bash
# See all branches
/glog --all

# Branches with stats
/glog --all --stat
```

3. Debugging
```bash
# Check merge history
/glog --all -n 20

# See detailed changes
/glog --stat -n 5
```

## Best Practices

1. **Viewing History**
   - Start with default view to see recent commits
   - Use `-n` to adjust commit count as needed
   - Add `--stat` when needing change details

2. **Branch Work**
   - Use `--all` to understand branch structure
   - Combine with `-n` to limit output
   - Add `--stat` for detailed branch work

3. **Troubleshooting**
   - Use `--all` to see full branch context
   - Include `--stat` for change impact
   - Adjust `-n` to see enough history

## Integration with Aider

The command integrates with Aider's:
- Git repository handling
- Command completion system
- Output formatting
- Error reporting

## Technical Notes

1. **Performance**
   - Uses git's built-in formatting
   - Minimal processing of git output
   - Efficient subprocess handling

2. **Compatibility**
   - Works with all git versions
   - Supports all repository types
   - Handles various git configurations

3. **Output Handling**
   - Preserves git's colored output
   - Maintains graph structure
   - Supports unicode output

## Future Enhancements

Potential improvements being considered:

1. Additional Options
   - File filtering
   - Author filtering
   - Date range selection
   - Pattern matching

2. Enhanced Visualization
   - Custom graph styles
   - Additional statistics
   - Commit grouping

3. Integration Features
   - Issue tracker links
   - CI status integration
   - Pull request information

## Contributing

When working on this command:

1. Follow git's output conventions
2. Maintain colored output support
3. Handle all git error cases
4. Update completions for new options
5. Document new features
6. Test with various repository types

## See Also

- [Git Pretty Formats](https://git-scm.com/docs/pretty-formats)
- [Git Log Documentation](https://git-scm.com/docs/git-log)
- [Aider Git Integration](https://aider.chat/docs/git.html)