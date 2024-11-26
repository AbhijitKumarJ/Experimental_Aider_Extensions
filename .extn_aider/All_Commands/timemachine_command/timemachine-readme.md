# Time Machine Command for Aider

This command provides intelligent exploration of code history, offering insights into how code has evolved over time. It goes beyond simple git history to show meaningful patterns in code changes.

## Features

- Timeline analysis of code changes
- Feature development tracking
- Related bug fixes discovery
- Test coverage history
- Contributor insights
- Automatic pattern recognition in changes
- Git history visualization
- Smart date range filtering

## Command Usage

```bash
/timemachine <function/feature> [--when time_period]
```

### Arguments

- `function/feature`: Function name, file path, or feature keyword to analyze
- `--when`: Optional time period specification (see Time Period Format below)

### Examples

```bash
# Analyze history of a specific function
/timemachine login_flow

# Look at changes in the last 3 months
/timemachine payment.py --when "last 3 months"

# Check changes before a refactor
/timemachine database.init --when "before refactor"

# See changes after a bug fix
/timemachine user_auth --when "after bug #123"
```

## Time Period Format

The command supports various time period formats:

1. **Relative Time Periods**
   - `last N days`
   - `last N months`
   - `last N years`

2. **Reference-based Periods**
   - `before <reference>` - Changes before a commit message reference
   - `after <reference>` - Changes after a commit message reference

## Output Sections

### 1. Overview
```
Code Evolution Analysis for: <target>
========================================
First change: YYYY-MM-DD
Latest change: YYYY-MM-DD
Total changes: N
```

### 2. Feature Development
```
Feature Development:
--------------------
YYYY-MM-DD - Added new login feature
YYYY-MM-DD - Implemented password reset
```

### 3. Bug Fixes
```
Bug Fixes:
--------------------
YYYY-MM-DD - Fixed authentication bypass
YYYY-MM-DD - Fixed memory leak
```

### 4. Test Development
```
Test Development:
--------------------
YYYY-MM-DD - Added unit tests for login
YYYY-MM-DD - Added integration tests
```

### 5. Related Changes
```
Commonly Changed Together:
--------------------
auth.py (5 times)
test_auth.py (3 times)
```

### 6. Contributors
```
Contributors:
--------------------
Alice: 10 changes
Bob: 5 changes
```

## Implementation Details

### CodeHistorian Class

The command uses the `CodeHistorian` class which provides:

1. **History Analysis**
   ```python
   def get_file_history(self, filepath, since_date=None):
       # Retrieves and analyzes commit history for a file
   ```

2. **Related Change Detection**
   ```python
   def find_related_changes(self, filepath, history):
       # Finds files commonly changed together
   ```

3. **Change Classification**
   ```python
   def analyze_changes(self, filepath, since_date=None):
       # Classifies changes into features, bugs, tests, etc.
   ```

4. **Timestamp Parsing**
   ```python
   def parse_time_period(self, time_spec):
       # Parses time period specifications
   ```

### Output Formatting

- Uses structured sections for clarity
- Includes timestamps with changes
- Shows statistics and summaries
- Provides context for each change type

## Command Completion

The command provides intelligent completions for:
- File paths in the repository
- Common time periods
- Combination suggestions

Example completions:
```python
[
    "auth.py",
    "auth.py --when last 3 months",
    "login --when last 6 months",
    "database --when last year"
]
```

## Best Practices

1. **Target Selection**
   - Use specific function/file names for focused analysis
   - Use feature keywords for broader insights
   - Consider using with specific time periods

2. **Time Period Usage**
   - Use broader periods for overview analysis
   - Use narrower periods for specific investigations
   - Reference significant events (like refactors or bugs)

3. **Analysis Tips**
   - Look for patterns in related changes
   - Check test development correlation
   - Monitor contributor distribution
   - Track bug fix clusters

## Technical Notes

1. **Git Integration**
   - Uses git commit history via `GitPython`
   - Analyzes commit messages for classification
   - Tracks file relationships through commits

2. **Pattern Recognition**
   - Identifies feature additions through commit messages
   - Detects bug fixes via commit patterns
   - Correlates test additions with changes

3. **Performance Considerations**
   - Caches commit history for faster access
   - Uses efficient git operations
   - Implements smart filtering for large histories

## Examples Use Cases

1. **Feature Investigation**
   ```bash
   /timemachine login_system --when "last year"
   # Shows how login feature evolved
   ```

2. **Bug Pattern Analysis**
   ```bash
   /timemachine auth.py --when "last 6 months"
   # Reveals bug fix patterns in auth system
   ```

3. **Test Coverage Evolution**
   ```bash
   /timemachine user_module
   # Shows how tests were added over time
   ```

4. **Change Impact Analysis**
   ```bash
   /timemachine database.py
   # Shows related files and impact patterns
   ```

## Error Handling

The command handles various error conditions:

1. **File Not Found**
   ```
   Could not find any files matching 'target'.
   Try using a more specific path or filename.
   ```

2. **Invalid Time Period**
   ```
   Error: Invalid time period format.
   Use 'last N days/months/years' or 'before/after reference'.
   ```

3. **Git Errors**
   ```
   Error getting history: <specific git error>
   ```

## Future Enhancements

Potential improvements being considered:

1. Enhanced visualization:
   - Timeline graphs
   - Change heat maps
   - Contributor networks

2. Additional analysis:
   - Code complexity trends
   - Refactoring detection
   - Performance impact analysis

3. Integration features:
   - CI/CD correlation
   - Issue tracker integration
   - Documentation changes tracking

## Contributing

When working with this command:

1. Follow the existing code structure
2. Add appropriate error handling
3. Update completions as needed
4. Maintain performance with large repositories
5. Update documentation for new features