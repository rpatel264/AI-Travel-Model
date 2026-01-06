"""
Retrieval V2 - Enhanced retrieval/search functions.

This module provides improved search and retrieval capabilities:
- Keyword-based search with scoring
- Top-K result ranking
- Integration with summary_chunks.json
"""

import json
import sys
import os
from pathlib import Path

# Default summary file (relative to Chicago/ directory)
SUMMARY_FILE = "summary_chunks.json"

def load_chunks(path=None):
    """
    Load chunks from JSON file.
    
    Args:
        path: Path to summary_chunks.json (default: Chicago/summary_chunks.json)
    
    Returns:
        List of chunk dictionaries
    """
    if path is None:
        # Get script directory and construct path
        script_dir = Path(__file__).parent
        path = script_dir / SUMMARY_FILE
    else:
        path = Path(path)
    
    if not path.exists():
        print(f"Summary file not found: {path}")
        print("\nMake sure you've run engineering_pipeline.py first to generate summary_chunks.json")
        sys.exit(1)
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def score_chunk(query_words, text):
    """
    Score a chunk based on how many query words appear in text.
    
    Args:
        query_words: List of query words (lowercase)
        text: Text to search in (will be lowercased)
    
    Returns:
        Score (number of matching words)
    """
    text = text.lower()
    return sum(word in text for word in query_words)

def search_chunks(query, chunks, top_k=5):
    """
    Search chunks by query and return top-K results.
    
    Args:
        query: Search query string
        chunks: List of chunk dictionaries
        top_k: Number of top results to return
    
    Returns:
        List of tuples: (score, chunk)
    """
    query_words = query.lower().split()
    scored = []

    for chunk in chunks:
        # Try different summary field names for compatibility
        summary_text = chunk.get("summary_text") or chunk.get("summary", "")
        if not summary_text:
            continue
            
        score = score_chunk(query_words, summary_text)
        if score > 0:
            scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]

def format_results(results, query):
    """Format search results for display."""
    if not results:
        return "No matching results found."
    
    output = []
    output.append(f"\nQuery: {query}\n")
    
    for i, (score, chunk) in enumerate(results, start=1):
        output.append(f"Result {i} (score={score})")
        output.append(f"Chunk #{chunk.get('chunk_position', 'N/A') + 1 if isinstance(chunk.get('chunk_position'), int) else 'N/A'}")
        # Handle different summary field names
        summary = chunk.get("summary_text") or chunk.get("summary", "")
        output.append(summary)
        output.append("-" * 60)
    
    return "\n".join(output)

def enhanced_search(query, chunks=None, summary_file=None, top_k=5):
    """
    Enhanced search function that can be used programmatically.
    
    Args:
        query: Search query string
        chunks: Optional pre-loaded chunks (if None, loads from file)
        summary_file: Optional path to summary file
        top_k: Number of top results to return
    
    Returns:
        List of tuples: (score, chunk)
    """
    if chunks is None:
        chunks = load_chunks(summary_file)
    
    return search_chunks(query, chunks, top_k=top_k)

def main():
    """Command-line interface for searching chunks."""
    if len(sys.argv) < 2:
        print("Usage: python retrieval_v2.py <query terms>")
        print("\nExample:")
        print("  python retrieval_v2.py mayor chicago")
        print("  python retrieval_v2.py architecture history")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    
    try:
        chunks = load_chunks()
        results = search_chunks(query, chunks)
        print(format_results(results, query))
    except FileNotFoundError:
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


