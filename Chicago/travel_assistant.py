"""
AI Travel Assistant for Chicago - Main Interface

This is the main entry point for the Chicago historical context travel assistant.
Users can query historical information about Chicago locations, events, and landmarks.
"""

import sys
from pathlib import Path

# Import retrieval and query functions from Chicago modules
from query_chunks import query_chunks, load_chunks
from retrieval_bullets import search_chunks as search_with_years
from retrieval_v2 import enhanced_search
from semantic_search import semantic_search

# Cache for loaded chunks
_CACHED_CHUNKS = None
def get_chunks():
    global _CACHED_CHUNKS
    if _CACHED_CHUNKS is None:
        _CACHED_CHUNKS = load_chunks()
    return _CACHED_CHUNKS

def answer_question(query: str, top_k: int = 5, year_filter=None) -> list:
    """
    Core retrieval function for UI and CLI.
    Returns structured search results.
    """
    chunks = get_chunks()

    if year_filter:
        results = search_with_years(
            query,
            chunks,
            before=year_filter.get("before"),
            after=year_filter.get("after"),
            top_k=top_k,
        )
    else:
        results = semantic_search(query, chunks, top_k=top_k)

    structured = []

    for result in results:
        if isinstance(result, tuple):
            score, chunk = result
        else:
            score = None
            chunk = result

        structured.append({
            "score": score,
            "summary": chunk.get("summary_text") or chunk.get("summary", ""),
            "pdf": Path(chunk.get("pdf_path", "")).name,
            "chunk_position": chunk.get("chunk_position"),
        })

    return structured

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
def synthesize_answer(question, retrieved_chunks):
    """
    Combine multiple factual summaries into a single coherent
    engineering-focused historical answer with numbered citations.
    """
    # Build a reference map: (pdf, chunk) -> reference number
    ref_map = {}
    references = []
    for idx, c in enumerate(retrieved_chunks, start=1):
        pdf = c.get("pdf", "Unknown PDF")
        chunk = c.get("chunk_position", "?")
        key = (pdf, chunk)
        if key not in ref_map:
            ref_map[key] = len(ref_map) + 1
            references.append((ref_map[key], pdf, chunk))

    # Add citation numbers inline
    combined = "\n\n".join(
        f"- {c['summary']} [{ref_map[(c['pdf'], c['chunk_position'])]}]"
        for c in retrieved_chunks if c.get("summary")
    )

    prompt = f"""
You are an engineering historian.

Using ONLY the factual summaries below, write a single,
coherent paragraph that answers the question.

Focus on engineering, construction methods, infrastructure,
and technical constraints. Do NOT add facts beyond the summaries.
Include inline reference numbers as shown.

Question:
{question}

Factual summaries:
{combined}
"""

    try:
        process = subprocess.Popen(
            ["C:\\Users\\Rishi\\AppData\\Local\\Programs\\Ollama\\ollama.exe", "run", "llama3.1:8b"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        output, _ = process.communicate(prompt, timeout=300)
        return output.strip(), references
    
    except subprocess.TimeoutExpired:
        process.kill()
        return "⚠️ Error: Ollama timed out while synthesizing the answer.", references
    except Exception as e:
        return f"⚠️ Error: Failed to synthesize answer. {e}", references

=======
>>>>>>> parent of a8b1227 (editing chunking and summaries)
=======
>>>>>>> parent of a8b1227 (editing chunking and summaries)
=======
>>>>>>> parent of a8b1227 (editing chunking and summaries)
=======
>>>>>>> parent of a8b1227 (editing chunking and summaries)

def get_historical_context(location_or_query, top_k=3, year_filter=None):
    """
    Get historical context for a Chicago location or topic.
    
    Args:
        location_or_query: String describing a location, landmark, or historical topic
        top_k: Number of results to return (default: 3)
        year_filter: Optional dict with 'before' or 'after' keys for year filtering
        
    Returns:
        Formatted historical context information
    """
    try:
        # Load chunks
        chunks = get_chunks()
        
        if not chunks:
            return "No historical data available. Please run the pipeline first to process PDFs."
        
        results = answer_question(
            location_or_query,
            top_k=top_k,
            year_filter=year_filter
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


            # Format results for paragraph display
            output.append(f"\nResult {i} - Source: {pdf_name}, Chunk #{chunk_position}")
            if score is not None:
                output.append(f"Relevance Score: {score}")
            output.append(summary)
            output.append("-" * 60)


        
        return "\n".join(output)
        
    except FileNotFoundError:
        return "Error: Historical data not found. Please run 'engineering_pipeline.py' first to process PDFs."
    except Exception as e:
        return f"Error retrieving historical context: {e}"

def main():
    """Main interface for the travel assistant."""
    print("=" * 60)
    print("🏙️  Chicago Historical Context Travel Assistant")
    print("=" * 60)
    print("\nAsk questions about Chicago's history, landmarks, events, or locations.")
    print("Examples: 'mayor chicago', 'architecture', 'great fire', '1871'")
    print("\nCommands: 'quit' or 'exit' to leave, 'help' for more options")
    
    # Load chunks once at startup
    try:
        chunks = load_chunks()
        if not chunks:
            print("\n⚠️  Warning: No historical data loaded. Run the pipeline first.")
            print("   Run: cd Chicago && python engineering_pipeline.py")
    except FileNotFoundError:
        print("\n⚠️  Warning: Historical data file not found.")
        print("   Run: cd Chicago && python engineering_pipeline.py")
        chunks = None
    
    while True:
        query = input("\n🔍 Your question: ").strip()
        
        if not query:
            continue
            
        if query.lower() in ['quit', 'exit', 'q']:
            break
        
        if query.lower() == 'help':
            print("\n" + "=" * 60)
            print("HELP - Available Commands")
            print("=" * 60)
            print("• Ask any question about Chicago history")
            print("• Use keywords like: mayor, architecture, fire, construction")
            print("• Try year-based queries: '1871', 'before 1900'")
            print("• Commands: 'quit', 'exit', 'help'")
            print("=" * 60)
            continue
        
        # Check for year filter hints in query
        year_filter = None
        query_lower = query.lower()
        
        if 'before' in query_lower:
            # Try to extract year after 'before'
            try:
                parts = query_lower.split('before')
                if len(parts) > 1:
                    year = int(parts[1].strip().split()[0])
                    year_filter = {'before': year}
                    query = query_lower.split('before')[0].strip()
            except:
                pass
        
        if 'after' in query_lower and not year_filter:
            try:
                parts = query_lower.split('after')
                if len(parts) > 1:
                    year = int(parts[1].strip().split()[0])
                    year_filter = {'after': year}
                    query = query_lower.split('after')[0].strip()
            except:
                pass
        
        # Get and display historical context
        context = get_historical_context(query, top_k=3, year_filter=year_filter)
        print(f"\n{context}")
    
    print("\n" + "=" * 60)
    print("Thank you for using the Chicago Travel Assistant! 👋")
    print("=" * 60)

if __name__ == "__main__":
    main()


