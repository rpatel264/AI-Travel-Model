"""
Retrieval Bullets - Search summary chunks and display bullet points.

This module:
- Loads processed chunks from summary_chunks.json
- Searches chunks by keywords
- Filters by year constraints (before/after)
- Displays results as bullet points for quick review
"""

import json
import sys
import re
import argparse
from pathlib import Path

# Default summary file (relative to Chicago/ directory)
SUMMARY_FILE = "summary_chunks.json"

# -------------------------
# Load all chunks
# -------------------------
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
        raise FileNotFoundError(f"Summary file not found: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# -------------------------
# Extract years from text
# -------------------------
def extract_years(text):
    """Extract 4-digit years (1700-2099) from text."""
    return [int(y) for y in re.findall(r"\b(1[7-9]\d{2}|20\d{2})\b", text)]

# -------------------------
# Score a chunk based on query words
# -------------------------
def score_chunk(query_words, text):
    """Score chunk based on how many query words appear in text."""
    text_lower = text.lower()
    return sum(word in text_lower for word in query_words)

# -------------------------
# Filter chunks by query and optional year constraints
# -------------------------
def search_chunks(query, chunks, before=None, after=None, top_k=5):
    """
    Search chunks by query with optional year filtering.
    
    Args:
        query: Search query string
        chunks: List of chunk dictionaries
        before: Filter out chunks with years >= this year
        after: Filter out chunks with years <= this year
        top_k: Number of top results to return
    
    Returns:
        List of tuples: (score, chunk, years)
    """
    query_words = query.lower().split()
    scored = []

    for chunk in chunks:
        # Try different summary field names for compatibility
        summary = chunk.get("summary_text") or chunk.get("summary", "")
        if not summary:
            continue
            
        score = score_chunk(query_words, summary)
        if score == 0:
            continue

        years = extract_years(summary)
        if before and any(y >= before for y in years):
            continue
        if after and any(y <= after for y in years):
            continue

        scored.append((score, chunk, years))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]

# -------------------------
# Format results for display
# -------------------------
def format_results(results, query, before=None, after=None):
    """Format search results for display."""
    if not results:
        return "No matching results found."
    
    output = []
    output.append(f"\nQuery: {query}")
    if before:
        output.append(f"Before: {before}")
    if after:
        output.append(f"After: {after}")
    output.append("")
    
    for rank, (score, chunk, years) in enumerate(results, start=1):
        output.append(f"Result {rank} (score={score}, years={years})")
        # Handle different PDF path field names
        pdf_name = chunk.get('pdf_path') or chunk.get('pdf_name', 'N/A')
        output.append(f"PDF: {Path(pdf_name).name if pdf_name != 'N/A' else 'N/A'}")
        output.append(f"Chunk #{chunk.get('chunk_position', 'N/A')}")
        summary = chunk.get("summary_text") or chunk.get("summary", "")
        output.append(summary)
        output.append("-" * 60)
    
    return "\n".join(output)

# -------------------------
# Main
# -------------------------
def main():
    """Command-line interface for searching chunks."""
    parser = argparse.ArgumentParser(
        description="Search summary chunks for bullet points.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python retrieval_bullets.py "mayor chicago"
  python retrieval_bullets.py "architecture" --before 1900
  python retrieval_bullets.py "fire" --after 1870
        """
    )
    parser.add_argument("query", type=str, help="Search query")
    parser.add_argument("--before", type=int, default=None, 
                       help="Filter results before this year (exclude chunks with years >= this)")
    parser.add_argument("--after", type=int, default=None,
                       help="Filter results after this year (exclude chunks with years <= this)")
    parser.add_argument("--file", type=str, default=None,
                       help="Path to summary_chunks.json (default: Chicago/summary_chunks.json)")
    parser.add_argument("--top-k", type=int, default=5,
                       help="Number of top results to return (default: 5)")
    args = parser.parse_args()

    try:
        chunks = load_chunks(args.file)
        results = search_chunks(args.query, chunks, before=args.before, 
                               after=args.after, top_k=args.top_k)
        
        print(format_results(results, args.query, args.before, args.after))
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nMake sure you've run engineering_pipeline.py first to generate summary_chunks.json")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

