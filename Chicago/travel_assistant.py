"""
AI Travel Assistant for Chicago

Handles historical context retrieval from processed Chicago PDFs using semantic search only.
"""

from pathlib import Path
from semantic_search import semantic_search
from query_chunks import load_chunks

# Cache loaded chunks
_CACHED_CHUNKS = None


def get_chunks():
    """Load and cache summary chunks."""
    global _CACHED_CHUNKS
    if _CACHED_CHUNKS is None:
        _CACHED_CHUNKS = load_chunks()
    return _CACHED_CHUNKS


def answer_question(query: str, top_k: int = 5):
    """
    Core retrieval function using semantic search only.
    Returns structured results for UI.
    """
    chunks = get_chunks()
    if not chunks:
        return []

    # Semantic search returns a list of (score, chunk_dict) tuples
    raw_results = semantic_search(query, chunks, top_k=top_k)

    structured = []
    for item in raw_results:
        # Ensure correct unpacking
        if isinstance(item, tuple) and len(item) == 2:
            score, chunk = item
        elif isinstance(item, dict):
            score = None
            chunk = item
        else:
            # Skip malformed results
            continue

        structured.append({
            "score": score,
            "summary": chunk.get("summary_text") or chunk.get("summary", ""),
            "pdf": Path(chunk.get("pdf_path", "")).name,
            "chunk_position": chunk.get("chunk_position"),
        })

    return structured


def get_historical_context(location_or_query, top_k=3):
    """
    Get formatted historical context for display using semantic search only.
    """
    try:
        results = answer_question(location_or_query, top_k=top_k)

        if not results:
            return f"No historical information found for '{location_or_query}'."

        output = [f"📚 Historical Context for: {location_or_query}", "=" * 60]

        for i, r in enumerate(results, start=1):
            output.append(f"\nResult {i} - Source: {r['pdf']}, Chunk #{r['chunk_position']}")
            if r["score"] is not None:
                output.append(f"Relevance Score: {r['score']:.3f}")
            output.append(r["summary"])
            output.append("-" * 60)

        return "\n".join(output)

    except Exception as e:
        return f"Error retrieving historical context: {e}"
