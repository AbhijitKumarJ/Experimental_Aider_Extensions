import os
import json
import shutil
from pathlib import Path
from datetime import datetime
import warnings

from llama_index.core import (
    Document,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from ..commands_registry import CommandsRegistry

# Suppress FutureWarning from tree-sitter
warnings.simplefilter("ignore", category=FutureWarning)

# Constants
RAG_CACHE_DIR = Path.home() / ".extn_aider" / "rags"

class RAGManager:
    """Manages RAG operations and persistence using aider's help infrastructure"""
    
    def __init__(self):
        """Initialize RAG manager with HuggingFace embeddings"""
        os.environ["TOKENIZERS_PARALLELISM"] = "true"
        self.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )
        self.parser = MarkdownNodeParser()
        self.cache_dir = RAG_CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()

    def _load_metadata(self):
        """Load RAG metadata from disk"""
        if self.metadata_file.exists():
            try:
                return json.loads(self.metadata_file.read_text())
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_metadata(self):
        """Save RAG metadata to disk"""
        self.metadata_file.write_text(json.dumps(self.metadata, indent=2))

    def create_rag(self, nickname: str, doc_path: str) -> str:
        """Create a new RAG from document"""
        try:
            doc_path = Path(doc_path).resolve()
            if not doc_path.exists():
                return f"Error: Document not found at {doc_path}"

            # Create RAG directory
            rag_dir = self.cache_dir / nickname
            if rag_dir.exists():
                return f"Error: RAG '{nickname}' already exists"

            # Read document content
            try:
                content = doc_path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                return f"Error: Could not read {doc_path}. File must be text/markdown"

            # Create document
            doc = Document(
                text=content,
                metadata=dict(
                    filename=doc_path.name,
                    extension=doc_path.suffix,
                )
            )

            # Parse nodes
            nodes = self.parser.get_nodes_from_documents([doc])

            # Create and save index
            index = VectorStoreIndex(nodes, embed_model=self.embed_model)
            
            # Save index
            rag_dir.mkdir(parents=True, exist_ok=True)
            index.storage_context.persist(persist_dir=str(rag_dir))

            # Update metadata
            self.metadata[nickname] = {
                "path": str(doc_path),
                "created": datetime.now().isoformat(),
                "num_nodes": len(nodes)
            }
            self._save_metadata()

            return f"Successfully created RAG '{nickname}' with {len(nodes)} chunks"

        except Exception as e:
            # Clean up if failed
            if rag_dir.exists():
                shutil.rmtree(rag_dir)
            return f"Error creating RAG: {str(e)}"

    def query_rag(self, nickname: str, query: str, k: int = 3, coder=None) -> str:
        """Query an existing RAG"""
        try:
            if nickname not in self.metadata:
                return f"Error: RAG '{nickname}' not found"

            rag_dir = self.cache_dir / nickname
            if not rag_dir.exists():
                return f"Error: RAG directory for '{nickname}' not found"

            # Load index
            try:
                storage_context = StorageContext.from_defaults(
                    persist_dir=str(rag_dir)
                )
                index = load_index_from_storage(
                    storage_context,
                    embed_model=self.embed_model
                )
            except Exception as e:
                return f"Error loading RAG: {str(e)}"

            # Create retriever
            retriever = index.as_retriever(similarity_top_k=k)

            # Get results
            nodes = retriever.retrieve(query)

            # Format results
            output = [f"\nSearch results from RAG '{nickname}':\n"]
            
            for i, node in enumerate(nodes, 1):
                score = node.score or 0
                relevance = max(0, min(1, score))  # Clamp between 0 and 1
                
                output.append(f"\n--- Result {i} (Relevance: {relevance:.2%}) ---")
                output.append(node.text.strip())
                if node.metadata:
                    source = node.metadata.get('filename', 'unknown')
                    output.append(f"\nSource: {source}")

            output.append("\n--- End of results ---")
            outputstr = "\n".join(output)
            return True, outputstr

        except Exception as e:
            return False, f"Error querying RAG: {str(e)}"

    def get_rag_list(self) -> str:
        """Get formatted list of available RAGs"""
        if not self.metadata:
            return "No RAGs available"

        output = ["Available RAGs:"]
        for nickname, info in self.metadata.items():
            created = datetime.fromisoformat(info['created']).strftime('%Y-%m-%d %H:%M')
            num_nodes = info.get('num_nodes', 'unknown')
            path = info.get('path', 'unknown')
            output.append(f"\n{nickname}:")
            output.append(f"  Source: {path}")
            output.append(f"  Chunks: {num_nodes}")
            output.append(f"  Created: {created}")

        return "\n".join(output)

    def delete_rag(self, nickname: str) -> str:
        """Delete a RAG"""
        if nickname not in self.metadata:
            return f"Error: RAG '{nickname}' not found"

        rag_dir = self.cache_dir / nickname
        if rag_dir.exists():
            try:
                shutil.rmtree(rag_dir)
            except Exception as e:
                return f"Error deleting RAG directory: {str(e)}"

        del self.metadata[nickname]
        self._save_metadata()

        return f"Successfully deleted RAG '{nickname}'"

# Initialize RAG manager
rag_manager = RAGManager()

def cmd_createragfromdoc(self, args):
    """Create a RAG from a text/markdown document
    Usage: /createragfromdoc <nickname> <document_path>
    
    Creates a RAG (Retrieval Augmented Generation) index from a text/markdown document.
    The document must be a text file - PDFs and other binary formats are not supported.
    The RAG can later be queried using /queryragfromdoc.
    
    Example:
        /createragfromdoc docs_rag /path/to/document.md
    """
    parts = args.strip().split(maxsplit=1)
    if len(parts) != 2:
        self.io.tool_error("Usage: /createragfromdoc <nickname> <document_path>")
        return
        
    nickname, doc_path = parts
    
    # Validate nickname
    if not nickname.isalnum():
        self.io.tool_error("Nickname must be alphanumeric")
        return
        
    # Create RAG
    self.io.tool_output(f"Creating RAG '{nickname}'...")
    result = rag_manager.create_rag(nickname, doc_path)
    self.io.tool_output(result)

def cmd_queryragfromdoc(self, args):
    """Query an existing RAG
    Usage: /queryragfromdoc <nickname> <query>
    
    Searches the specified RAG for content relevant to your query
    and returns the most similar passages.
    
    Example:
        /queryragfromdoc docs_rag "How do I use the git commands?"
    """
    parts = args.strip().split(maxsplit=1)
    if len(parts) != 2:
        self.io.tool_error("Usage: /queryragfromdoc <nickname> <query>")
        return
        
    nickname, query = parts
    
    # Query RAG
    self.io.tool_output(f"Querying RAG '{nickname}'...")
    success,result = rag_manager.query_rag(nickname, query, 3)
    if success:
        result = result.strip()
        result = "For the query:\n\n" + query + "\n\n" + result
        self.io.tool_output(result)
        
        self.coder.cur_messages += [
            dict(role="user", content=result),
            dict(role="assistant", content="Ok."),
        ]
    else:
        self.io.tool_error(result)

def cmd_listrag(self, args=""):
    """List all available RAGs
    Usage: /listrag
    
    Shows information about all available RAGs including
    their source documents, number of chunks, and creation dates.
    """
    self.io.tool_output(rag_manager.get_rag_list())

def cmd_deleterag(self, args):
    """Delete a RAG
    Usage: /deleterag <nickname>
    
    Permanently deletes the specified RAG and frees up disk space.
    """
    nickname = args.strip()
    if not nickname:
        self.io.tool_error("Usage: /deleterag <nickname>")
        return
        
    result = rag_manager.delete_rag(nickname)
    self.io.tool_output(result)

def completions_createragfromdoc(self):
    """No completions for createragfromdoc - nickname should be new"""
    return ["ragnickname", "documentpath"]

def completions_queryragfromdoc(self):
    """Provide completions for queryragfromdoc command - existing nicknames"""
    return list(rag_manager.metadata.keys())

def completions_deleterag(self):
    """Provide completions for deleterag command - existing nicknames"""
    return list(rag_manager.metadata.keys())

# Register commands
CommandsRegistry.register("createragfromdoc", cmd_createragfromdoc, completions_createragfromdoc)
CommandsRegistry.register("queryragfromdoc", cmd_queryragfromdoc, completions_queryragfromdoc)
CommandsRegistry.register("listrag", cmd_listrag)
CommandsRegistry.register("deleterag", cmd_deleterag, completions_deleterag)