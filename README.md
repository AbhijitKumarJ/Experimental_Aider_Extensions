# Unofficial and experimental Aider Extension

Experimental Custom extensions for the Aider AI coding assistant.
The purpose of this repository is to experiment with possible new features and suggest to aider contributor to add based on their judgement.
Do not consider this in any way related to official distribution of aider.

## Important Notice

This is just for experimentation and not for serious use. If you want to use these files, 
please verify the code yourself and experiment with it before using it to any work.



Project Layout:
```
./
├── main.py           # New simple runner
└── custom_aider/
    ├── __init__.py
    ├── monkey_patch.py
    ├── custom_aider_main.py
    ├── custom_coder.py
    ├── commands_registry.py
    └── commands/
        ├── __init__.py
        ├── git_commands.py
        └── utility_commands.py
        .
        .
        .
```


## Usage

Run the extended version of aider: 

```bash
python main.py
```

## New Commands

/createragfromdoc Create a RAG from a text/markdown document
    Usage: /createragfromdoc <nickname> <document_path>
    
    Creates a RAG (Retrieval Augmented Generation) index from a text/markdown document.
    The document must be a text file - PDFs and other binary formats are not supported.
    The RAG can later be queried using /queryragfromdoc.
    
    Example:
        /createragfromdoc docs_rag /path/to/document.md
    
/customchat       Enhanced chat with keyword substitution support
    Usage: /customchat <message>
    
    Your message can contain @text-keyword references that will be expanded
    based on definitions in .aider.keywords.json.
    
    Example keywords file:
    {
        "api": "REST API with JSON responses",
        "tests": "Unit tests using pytest with mocking"
    }
    
    Example usage:
    /customchat Create @text-tests for the login function
    
/deleterag        Delete a RAG
    Usage: /deleterag <nickname>
    
    Permanently deletes the specified RAG and frees up disk space.
    

/files            List all files with details
    Usage: /files [pattern]
    
    Shows files in chat with their sizes and last modified times
    Optional pattern to filter files
    

/glog             Show pretty git log with branch graph and stats
    Usage: /glog [options]
    
    Options:
        -n N     Show last N commits (default: 10)
        --all    Show all branches
        --stat   Show changed files statistics
    

/listrag          List all available RAGs
    Usage: /listrag
    
    Shows information about all available RAGs including
    their source documents, number of chunks, and creation dates.
    

/queryragfromdoc  Query an existing RAG
    Usage: /queryragfromdoc <nickname> <query>
    
    Searches the specified RAG for content relevant to your query
    and returns the most similar passages.
    
    Example:
        /queryragfromdoc docs_rag "How do I use the git commands?"
    

/showcontext      Save and display current chat context as HTML
    Usage: /showcontext
    
    Saves the current chat context including files, messages, and metadata 
    as a formatted HTML file and opens it in the default browser.
    Files are saved in .aider/context/ with timestamps.
    
/stats            Show statistics about files in chat
    Usage: /stats
    
    Shows total lines, words, characters for all files in chat
    Breaks down by file type
    
/zadd             Enhanced /add command with validation and git status

/zclear           Enhanced /clear command with history backup

/zcommit          Enhanced /commit command with stats and message enhancement

/zdrop            Enhanced /drop command with confirmation and backup

/zmodel           Enhanced /model command with model comparison

/zvoice           Enhanced /voice command with confidence check and retry

/zweb             Enhanced /web command with saving scraped data in .aider/web folder and timing and retry support

/clip-edit        Apply clipboard contents as edits to specified files
    Usage: /clip-edit <filename>
    
    Gets code edits from clipboard (copied from ChatGPT/Claude) and applies them to the specified file.
    The clipboard content should contain code changes in a supported format (diff, whole file, etc).
   
## Development

To add new commands:

1. Create a new module in `custom_aider/commands/`
2. Define command functions with docstrings
3. Register commands using `CommandsRegistry.register()`
```



## For rag related commands, help system should work properly, so first check if help is installed properly.

```
$ aider
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────
Aider v0.64.1
Model: gemini/gemini-1.5-flash-latest with whole edit format
Git repo: .git with 8 files
Repo-map: using 1024 tokens, auto refresh
VSCode terminal detected, pretty output has been disabled.
Use /help <question> for help, run "aider --help" to see cmd line args
──────────────────────────────────────────────────────────────────────────────────────────────────────────
> /help how to configure llm                                                                                       

To use interactive /help you need to install the help extras

python -m pip install --upgrade --upgrade-strategy only-if-needed 'aider-chat[help]' --extra-index-url 
https://download.pytorch.org/whl/cpu
Run pip install? (Y)es/(N)o [Yes]:                                                                                 

Installing: python -m pip install --upgrade --upgrade-strategy only-if-needed 'aider-chat[help]' --extra-index-url https://download.pytorch.org/whl/cpu
Installing...
```


This provides a clean, maintainable structure for extending aider with new commands. The CommandsRegistry manages registration and installation of commands, while the custom coder ensures proper initialization. Each command is well-documented and properly integrated with aider's existing functionality.

You can easily add more commands by creating new modules in the commands directory and registering them with the CommandsRegistry. The extension system is modular and type-safe, making it easy to maintain and extend further.







## Samples:

--------------------------------------------------------------------------------------------------
> /zweb https://aider.chat/docs/install.html                                                                                          

Fetching https://aider.chat/docs/install.html (retries left: 3)...
Scraping https://aider.chat/docs/install.html...
... added to chat.
Fetched in 1.15 seconds
Word count: 119
I understand the instructions.  However, you have only provided the content of a webpage, not a code file.  I cannot suggest code     
changes without access to the code itself.  Please provide the code files you want me to review.                                      


Tokens: 2.5k sent, 48 received. Cost: $0.00020 message, $0.00035 session.
───────────────────────────────────────────────────────────────────────────────────────────────────────────

------------------------------------------------------------------------------------------------
ask> /customchat how to do @text-tests                                                                                                


Expanded message:
how to do Unit tests using pytest with mocking

Press Enter to send or Ctrl-C to cancel...

-----------------------------------------------------------------------------------------------

> /createragfromdoc lancedblessons lancedb_lessons_ragsource.md                                                                       

Creating RAG 'lancedblessons'...
Successfully created RAG 'lancedblessons' with 222 chunks
───────────────────────────────────────────────────────────────────────────────────────────────────────────
---------------------------------------------------------------------------------------------------
> /listrag                                                                                                                            

Available RAGs:

lancedblessons:
  Source: /home/Experimental_Aider_Extensions/lancedb_lessons_ragsource.md
  Chunks: 222
  Created: 2024-11-23 06:10
───────────────────────────────────────────────────────────────────────────────────────────────────────────
------------------------------------------------------------------------------------------------------

> /queryragfromdoc lancedblessons "how to save a record in lance db?"                                                                 

Querying RAG 'lancedblessons'...
For the query:

"how to save a record in lance db?"

Search results from RAG 'lancedblessons':


--- Result 1 (Relevance: 77.69%) ---
### Concurrent Access
```python
# Configure for concurrent access
db = lancedb.connect(
    "s3+ddb://bucket/path",
    storage_options={
        "ddb_table_name": "lance_locks"
    }
)
```

Source: lancedb_lessons_ragsource.md

--- Result 2 (Relevance: 77.64%) ---
## 9. Backup and Recovery

```python
class BackupManager:
    def __init__(self, source_uri, backup_uri):
        self.source = lancedb.connect(source_uri)
        self.backup = lancedb.connect(backup_uri)
        
    async def create_backup(self, table_name):
        source_table = self.source.open_table(table_name)
        data = await source_table.to_arrow()
        backup_table = self.backup.create_table(
            f"{table_name}_backup_{int(time.time())}",
            data
        )
        
    async def restore_from_backup(self, backup_name, target_name):
        backup_table = self.backup.open_table(backup_name)
        data = await backup_table.to_arrow()
        self.source.create_table(target_name, data)
```

Source: lancedb_lessons_ragsource.md

--- Result 3 (Relevance: 77.34%) ---
### Local Storage Optimization
```python
# Configure for local performance
db = lancedb.connect(
    "/path/to/storage",
    read_consistency_interval=timedelta(seconds=0)  # Strong consistency
)
```

Source: lancedb_lessons_ragsource.md

--- End of results ---
───────────────────────────────────────────────────────────────────────────────────────────────────────────
------------------------------------------------------------------------------------------------




