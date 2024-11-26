# AIChat RAG Query Command

An Aider extension command that enables querying RAGs (Retrieval Augmented Generation) through the AIChat API endpoint.

## Overview

The `/aichat_rag_query` command allows you to search and retrieve information from RAGs that are set up in AIChat. It connects to AIChat's local API endpoint to perform queries and retrieves context-relevant information.

## Prerequisites

- AIChat server running locally (`aichat --serve`)
- The server should be accessible at `http://localhost:8000`
- Python `requests` library installed

## Command Usage

```bash
/aichat_rag_query <rag_name> <query>
```

### Parameters

- `rag_name`: The name of the RAG to query (e.g., "aichat-wiki")
- `query`: The search query text (e.g., "How does the RAG feature work?")

### Example Usage

```bash
# Query the aichat-wiki RAG
/aichat_rag_query aichat-wiki "How do I use RAG?"

# Query documentation RAG
/aichat_rag_query documentation "What are the available commands?"
```

## Features

- Direct integration with AIChat's RAG search API
- Automatic extraction and formatting of context from responses
- Command completion support for common RAG names
- Error handling for connection and response issues
- Results are added to the chat context for reference

## Response Format

The command displays results in a formatted structure:

```
Results from aichat RAG '<rag_name>':

Query: <your query>

Context:
<retrieved context from RAG>

--- End of results ---
```

## Error Handling

The command handles several types of errors:

- Connection errors (when AIChat server is not running)
- HTTP errors (invalid requests or server errors)
- Response format errors (unexpected response structure)
- General exceptions

## Default RAG Suggestions

The command provides basic command completion with these default RAG names:
- aichat-wiki
- documentation 
- codebase

## Technical Details

### API Endpoint

The command communicates with:
```
http://localhost:8000/v1/rags/search
```

### Request Format

```json
{
    "name": "<rag_name>",
    "input": "<query>"
}
```

### Response Processing

The command:
1. Extracts the "data" field from the response
2. Parses XML-like tags to get context
3. Formats and displays the relevant information

## Integration with Aider

The command is integrated into Aider's command system and:
- Uses Aider's IO system for output
- Adds results to the chat context
- Provides command completion support
- Follows Aider's command registry pattern

## Limitations

- Only works with locally running AIChat server
- Assumes default port 8000
- Basic command completion (no dynamic RAG list)

## Error Messages

Common error messages and their meaning:

- "Could not connect to aichat API. Is the server running?" 
  - The AIChat server is not accessible
- "API request failed: ..." 
  - The API request returned an error
- "Error processing response: ..." 
  - The response format was unexpected
- "Error querying RAG: ..." 
  - An unexpected error occurred

## Example Workflow

1. Start AIChat server:
   ```bash
   aichat --serve
   ```

2. In Aider, query a RAG:
   ```bash
   /aichat_rag_query aichat-wiki "how does it work"
   ```

3. Review the returned context and continue your chat with Aider

## Tips

- Make sure AIChat server is running before using the command
- Use specific, clear queries for better results
- Consider the context when formulating queries

This README provides:

1. A clear overview of the command and its purpose
2. Detailed usage instructions
3. Technical specifications
4. Error handling information
5. Example workflows
6. Prerequisites and limitations
7. Integration details
8. Tips for optimal usage
