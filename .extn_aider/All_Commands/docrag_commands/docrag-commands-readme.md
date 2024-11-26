# Document RAG Commands for Aider

This module provides Retrieval Augmented Generation (RAG) capabilities for Aider, allowing you to create, query, and manage RAG indices from text documents. The RAG system uses HuggingFace embeddings and enables semantic search through document content.

## Features

- Create RAG indices from text/markdown documents
- Query existing RAGs with natural language questions
- List and manage RAG indices
- Persistent storage of RAG data
- Cross-session availability of RAGs

## Requirements

The following packages are required:
```bash
pip install llama-index-core
pip install llama-index-embeddings-huggingface
```

## Command Overview

### Create RAG
```bash
/createragfromdoc <nickname> <document_path>
```
Creates a new RAG index from a text/markdown document.

- `nickname`: Alphanumeric identifier for the RAG
- `document_path`: Path to the source document

Example:
```bash
/createragfromdoc docs_rag ./documentation.md
```

### Query RAG
```bash
/queryragfromdoc <nickname> <query>
```
Searches the specified RAG for relevant content.

- `nickname`: Name of the RAG to query
- `query`: Natural language search query

Example:
```bash
/queryragfromdoc docs_rag "How do I configure logging?"
```

### List RAGs
```bash
/listrag
```
Shows all available RAGs with details including:
- Source document paths
- Creation dates
- Number of chunks
- File information

### Delete RAG
```bash
/deleterag <nickname>
```
Permanently removes a RAG and its associated data.

- `nickname`: Name of the RAG to delete

Example:
```bash
/deleterag docs_rag
```

## Storage and Data Management

RAGs are stored in the user's home directory:
```
~/.extn_aider/rags/
├── <nickname>/           # RAG storage directory
│   ├── docstore.json    # Document chunks
│   ├── index.json       # Vector index
│   └── embeddings/      # Cached embeddings
└── metadata.json        # RAG metadata
```

## Completion Support

Command completion is available for:
- `/queryragfromdoc` - Shows existing RAG nicknames
- `/deleterag` - Shows existing RAG nicknames

## Implementation Details

### Models and Embeddings

- Uses BAAI/bge-small-en-v1.5 embedding model
- Handles document chunking via MarkdownNodeParser
- Supports similarity search with configurable k results

### Error Handling

The commands handle various error conditions:
- Invalid document formats
- Missing files
- Non-existent RAGs
- Embedding/indexing failures
- Storage/retrieval errors

## Usage Tips

1. Use descriptive RAG nicknames for easy identification
2. Keep source documents in text/markdown format
3. Use specific queries for better search results
4. Regularly clean up unused RAGs
5. Monitor storage usage in the RAGs directory

## Example Workflow

```bash
# Create a RAG from documentation
/createragfromdoc api_docs ./api_documentation.md

# Verify RAG creation
/listrag

# Query the documentation
/queryragfromdoc api_docs "How to authenticate API requests?"

# Remove when no longer needed
/deleterag api_docs
```

## Technical Notes

- RAGs persist across Aider sessions
- Embeddings are cached for performance
- Memory usage scales with document size
- Search results include relevance scores

## Troubleshooting

### Common Issues

1. **RAG Creation Fails**
   - Verify document is text/markdown
   - Check file permissions
   - Ensure sufficient disk space

2. **Poor Search Results**
   - Make queries more specific
   - Check document content quality
   - Verify RAG was created successfully

3. **Performance Issues**
   - Monitor disk space
   - Clean up unused RAGs
   - Consider document size

### Debug Steps

1. Check RAG metadata:
   ```bash
   /listrag
   ```

2. Verify source document:
   ```bash
   ls -l <document_path>
   ```

3. Test with simple query:
   ```bash
   /queryragfromdoc <nickname> "basic test query"
   ```

## Future Improvements

Potential enhancements being considered:
- Support for PDF and other document formats
- Bulk RAG creation from directories
- Enhanced search relevance tuning
- Memory usage optimizations
- Improved metadata management

## Contributing

When contributing to this command:
1. Maintain consistent error handling
2. Update command documentation
3. Follow existing code structure
4. Add relevant tests
5. Update completion support as needed