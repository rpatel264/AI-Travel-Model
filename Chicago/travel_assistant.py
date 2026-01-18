"""
AI Travel Assistant for Chicago

This module handles historical context retrieval from processed Chicago PDFs.
"""

import subprocess
from pathlib import Path

# Import retrieval and query functions from Chicago modules
from query_chunks import query_chunks, load_chunks
from retrieval_bullets import search_chunks as search_with_years
from semantic_search import semantic_search  # Added for semantic search

# Cache for loaded chunks
_CACHED_CHUNKS = None

def get_chunks():
    global _CACHED_CHUNKS
    if _CACHED_CHUNKS is None:
        _CACHED_CHUNKS = load_chunks()
    return _CACHED_CHUNKS

def answer_question(query: str, top_k: int = 5, year_filter=None, search_method="Keyword Search") -> list:
    """
    Core retrieval function for UI and CLI.
    Returns structured search results.
    """
    chunks = get_chunks()
    results = []

    if search_method == "Semantic Search":
        # Use semantic search
        results = semantic_search(query, chunks, top_k=top_k)
    else:
        # Default: keyword/year-based search
        results = search_with_years(
            query,
            chunks,
            before=year_filter.get("before") if year_filter else None,
            after=year_filter.get("after") if year_filter else None,
            top_k=top_k,
        )

    structured = []
    for result in results:
    # Expect (score, chunk_dict)
    if isinstance(result, tuple) and len(result) == 2:
        score, chunk = result
    elif isinstance(result, dict):
        score = None
        chunk = result
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

def get_historical_context(location_or_query, top_k=3, year_filter=None, search_method="Keyword Search"):
    """
    Get historical context for a Chicago location or topic.
    """
    try:
        chunks = get_chunks()
        if not chunks:
            return "No historical data available. Please run the pipeline first to process PDFs."

        results = answer_question(
            location_or_query,
            top_k=top_k,
            year_filter=year_filter,
            search_method=search_method
        )

        if not results:
            return f"No historical information found for '{location_or_query}'. Try different keywords or check if the topic is covered in the processed documents."

        # Format results for display
        output = []
        output.append(f"📚 Historical Context for: {location_or_query}")
        output.append("=" * 60)

        for i, result in enumerate(results, 1):
            score = result["score"]
            summary = result["summary"]
            pdf_name = result["pdf"]
            chunk_position = result["chunk_position"]

            output.append(f"\nResult {i} - Source: {pdf_name}, Chunk #{chunk_position}")
            if score is not None:
                output.append(f"Relevance Score: {score:.3f}")
            output.append(summary)
            output.append("-" * 60)

        return "\n".join(output)

    except FileNotFoundError:
        return "Error: Historical data not found. Please run 'engineering_pipeline.py' first to process PDFs."
    except Exception as e:
        return f"Error retrieving historical context: {e}"
