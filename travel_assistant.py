"""
AI Travel Assistant for Chicago - Main Interface

This is the main entry point for the Chicago historical context travel assistant.
Users can query historical information about Chicago locations, events, and landmarks.
"""

import sys
from pathlib import Path

# Add Chicago directory to path
sys.path.insert(0, str(Path(__file__).parent / "Chicago"))

# Import retrieval and query functions from Chicago modules
from query_chunks import query_chunks, load_chunks
from retrieval_bullets import search_chunks as search_with_years
from retrieval_v2 import enhanced_search

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
        chunks = load_chunks()
        
        if not chunks:
            return "No historical data available. Please run the pipeline first to process PDFs."
        
        # Use retrieval_bullets if year filtering is requested
        if year_filter:
            before = year_filter.get('before')
            after = year_filter.get('after')
            results = search_with_years(location_or_query, chunks, 
                                       before=before, after=after, top_k=top_k)
        else:
            # Use query_chunks for general search
            results = query_chunks(location_or_query, chunks=chunks, top_k=top_k)
        
        if not results:
            return f"No historical information found for '{location_or_query}'. Try different keywords or check if the topic is covered in the processed documents."
        
        # Format results for display
        output = []
        output.append(f"📚 Historical Context for: {location_or_query}")
        output.append("=" * 60)
        
        for i, result in enumerate(results, 1):
            if isinstance(result, tuple):
                score, chunk = result
            else:
                chunk = result
                score = None
            
            # Get summary text
            summary = chunk.get("summary_text") or chunk.get("summary", "")
            
            # Get PDF name
            pdf_path = chunk.get("pdf_path", "")
            if isinstance(pdf_path, str):
                pdf_name = Path(pdf_path).name
            else:
                pdf_name = str(pdf_path)
            
            output.append(f"\n📍 Result {i}")
            if score:
                output.append(f"   Relevance Score: {score}")
            output.append(f"   Source: {pdf_name}")
            output.append(f"   Chunk #{chunk.get('chunk_position', 'N/A')}")
            output.append(f"\n   {summary}")
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


