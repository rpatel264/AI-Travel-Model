"""
Query Chunks - Allows keyword search through processed chunks with PDF filtering.

This module provides functionality to:
- Search chunks by keywords
- Filter results by specific PDF file
- Retrieve relevant chunks based on queries
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
        List of chunk dictionaries (empty list if file not found)
    """
    if path is None:
        # Get script directory and construct path
        script_dir = Path(__file__).parent
        path = script_dir / SUMMARY_FILE
    else:
        path = Path(path)
    
    if not path.exists():
        print(f"Summary file not found: {path}")
        return []
    
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
    text_lower = text.lower()
    return sum(word in text_lower for word in query_words)

def search(query, chunks, top_k=5, pdf_filter=None):
    """
    Search chunks by query with optional PDF filtering.
    
    Args:
        query: Search query string
        chunks: List of chunk dictionaries
        top_k: Number of top results to return
        pdf_filter: Optional PDF filename to filter by (partial match, case-insensitive)
    
    Returns:
        List of tuples: (score, chunk)
    """
    query_words = query.lower().split()
    scored = []

    for chunk in chunks:
        # Skip chunks from PDFs not matching the filter
        if pdf_filter:
            # Handle different PDF path field names
            pdf_path = chunk.get("pdf_path", "")
            if isinstance(pdf_path, str):
                pdf_name = os.path.basename(pdf_path)
            else:
                pdf_name = str(pdf_path)
            
            if pdf_filter.lower() not in pdf_name.lower():
                continue

        # Try different summary field names for compatibility
        summary = chunk.get("summary_text") or chunk.get("summary", "")
        if not summary:
            continue
            
        score = score_chunk(query_words, summary)
        if score > 0:
            scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]

def format_results(results, query, pdf_filter=None):
    """Format search results for display."""
    if not results:
        return "No matching results found."
    
    output = []
    output.append(f"\nQuery: {query}")
    if pdf_filter:
        output.append(f"Filtered by PDF: {pdf_filter}")
    output.append("")
    
    for rank, (score, chunk) in enumerate(results, start=1):
        output.append(f"Result {rank} (score={score})")
        
        # Handle different PDF path field names
        pdf_path = chunk.get("pdf_path", "")
        if isinstance(pdf_path, str):
            pdf_name = os.path.basename(pdf_path)
        else:
            pdf_name = str(pdf_path)
        
        chunk_pos = chunk.get('chunk_position', 'N/A')
        output.append(f"Chunk #{chunk_pos} from {pdf_name}")
        
        # Handle different summary field names
        summary = chunk.get("summary_text") or chunk.get("summary", "")
        output.append(summary)
        output.append("-" * 60)
    
    return "\n".join(output)

def query_chunks(query, chunks=None, summary_file=None, top_k=5, pdf_filter=None):
    """
    Main query function that can be used programmatically.
    
    Args:
        query: Search query string
        chunks: Optional pre-loaded chunks (if None, loads from file)
        summary_file: Optional path to summary file
        top_k: Number of top results to return
        pdf_filter: Optional PDF filename to filter by
    
    Returns:
        List of tuples: (score, chunk)
    """
    if chunks is None:
        chunks = load_chunks(summary_file)
    
    return search(query, chunks, top_k=top_k, pdf_filter=pdf_filter)

def main():
    """Command-line interface for searching chunks."""
    if len(sys.argv) < 2:
        print("Usage: python query_chunks.py <search terms> [--pdf <filename>]")
        print("\nExamples:")
        print("  python query_chunks.py mayor chicago")
        print("  python query_chunks.py architecture --pdf Chicago_Timeline")
        return

    args = sys.argv[1:]
    query = []
    pdf_filter = None

    # Parse optional --pdf argument
    i = 0
    while i < len(args):
        if args[i] == "--pdf" and i + 1 < len(args):
            pdf_filter = args[i + 1]
            i += 2
        else:
            query.append(args[i])
            i += 1

    query = " ".join(query)
    
    try:
        chunks = load_chunks()
        if not chunks:
            print("No chunks to search. Run the pipeline first.")
            print("\nMake sure you've run engineering_pipeline.py to generate summary_chunks.json")
            return

        results = search(query, chunks, pdf_filter=pdf_filter)
        print(format_results(results, query, pdf_filter))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


