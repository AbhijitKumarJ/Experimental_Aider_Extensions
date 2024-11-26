"""Commands for interacting with aichat API endpoints"""

import requests
import json
from ..commands_registry import CommandsRegistry

def cmd_query_rag_from_aichat(self, args):
    """Query a RAG using the aichat API endpoint
    Usage: /query_rag_from_aichat <rag_name> <query>
    
    Searches the specified RAG for content relevant to your query
    using the aichat RAG search API endpoint.
    
    Example:
        /query_rag_from_aichat aichat-wiki "How does feature X work?"
    """
    # Parse arguments
    parts = args.strip().split(maxsplit=1)
    if len(parts) != 2:
        self.io.tool_error("Usage: /query_rag_from_aichat <rag_name> <query>")
        return
        
    rag_name, query = parts
    
    # Prepare request
    url = "http://localhost:8000/v1/rags/search"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "name": rag_name,
        "input": query
    }
    
    # Make request
    try:
        self.io.tool_output(f"Querying RAG '{rag_name}'...")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        # Extract response data
        result = response.json()
        if "data" not in result:
            raise ValueError("Unexpected response format - missing 'data' field")
            
        # Format output
        context_data = result["data"]
        
        # Extract context from the response
        # The context is wrapped in <context> tags in the response
        import re
        context_match = re.search(r"<context>(.*?)</context>", context_data, re.DOTALL)
        if not context_match:
            raise ValueError("No context found in response")
            
        context = context_match.group(1).strip()
        
        # Format the output
        output = [
            f"\nResults from aichat RAG '{rag_name}':",
            f"\nQuery: {query}\n",
            "Context:",
            context,
            "\n--- End of results ---"
        ]
        
        formatted_output = "\n".join(output)
        
        # Display results
        self.io.tool_output(formatted_output)
        
        # Add to chat context
        self.coder.cur_messages += [
            dict(role="user", content=formatted_output),
            dict(role="assistant", content="Ok."),
        ]
        
    except requests.exceptions.ConnectionError:
        self.io.tool_error("Could not connect to aichat API. Is the server running?")
    except requests.exceptions.HTTPError as e:
        self.io.tool_error(f"API request failed: {e}")
    except ValueError as e:
        self.io.tool_error(f"Error processing response: {e}")
    except Exception as e:
        self.io.tool_error(f"Error querying RAG: {e}")

def completions_query_rag_from_aichat(self):
    """Completions for query_rag_from_aichat command"""
    # Return basic defaults since the aichat example doesn't show 
    # a RAG listing endpoint
    return ["aichat-wiki", "documentation", "codebase"]

# Register the command
CommandsRegistry.register(
    "query_rag_from_aichat", 
    cmd_query_rag_from_aichat,
    completions_query_rag_from_aichat
)
