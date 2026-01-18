"""
AI Travel Assistant for Chicago

Handles historical context retrieval from processed Chicago PDFs.
"""

from pathlib import Path

# Imports from project modules
from query_chunks import load_chunks
from retrieval_bullets import search_chunks as search_with_years
from semantic_search import semantic_search

# Cache loaded chunks
_CACHED_CHUNKS = None


def get_chunks():
    """Load and cache summary chunks."""
    global _CACHED_CHUNKS
    if _CACHED_CHUNKS is None:
        _CACHED_CHUNKS = load_chunks()
    return _CACHED_CHUNKS


def answer_question(
    query: str,
    top_k: int = 5,
    year_filter=None,
    search_method: str = "Keyword Search",
):
    """
    Core retrieval function.
    Returns structured results for UI.
    """
    chunks = get_chunks()
    if not chunks:
        return []

    # Run selected search method
    if search_method == "Semantic Search":
        # Returns [(score, chunk_dict), ...]
        raw_results = semantic_search(query, chunks, top_k=top_k)
    else:
        # Keyword + year filtering
        raw_results = search_with_years(
            query,
            chunks,
            before=year_filter.get("before") if year_filter else None,
            after=year_filter.get("after") if year_filter else None,
            top_k=top_k,
        )

    structured = []

    for item in raw_results:
        # Normalize result format
        if isinstance(item, tuple) and len(item) == 2:
            score, chunk = item
        elif isinstance(item, dict):
            score = None
            chunk = item
        else:
            continue

        structured.append({
            "score": score,
            "summary": chunk.get("summary_text") or chunk.get("summary", ""),
            "pdf": Path(chunk.get("pdf_path", "")).name,
            "chunk_position": chunk.get("chunk_position"),
        })

    return structured


def get_historical_context(
    location_or_query,
    top_k=3,
    year_filter=None,
    search_method="Keyword Search",
):
    """
    Get formatted historical context for display.
    """
    try:
        results = answer_question(
            location_or_query,
            top_k=top_k,
            year_filter=year_filter,
            search_method=search_method,
        )

        if not results:
            return (
                f"No historical information found for "
                f"'{location_or_query}'."
            )

        output = []
        output.append(f"📚 Historical Context for: {location_or_query}")
        output.append("=" * 60)

        for i, r in enumerate(results, start=1):
            output.append(
                f"\nResult {i} - Source: {r['pdf']}, "
                f"Chunk #{r['chunk_position']}"
            )

            if r["score"] is not None:
                output.append(f"Relevance Score: {r['score']:.3f}")

            output.append(r["summary"])
            output.append("-" * 60)

        return "\n".join(output)

    except Exception as e:
        return f"Error retrieving historical context: {e}"
