import streamlit as st
from travel_assistant import get_historical_context

# Page configuration
st.set_page_config(
    page_title="Chicago Historical Travel Assistant",
    page_icon="🏙️",
    layout="wide"
)

st.title("🏙️ Chicago Historical Travel Assistant")
st.write(
    "Ask questions about Chicago's history, landmarks, events, or locations.\n"
    "Examples: 'mayor chicago', 'architecture', 'great fire', '1871'"
)

# User query input
query = st.text_input("🔍 Your question:")

# Threshold for low relevance
LOW_RELEVANCE_THRESHOLD = 0.6

if query:
    with st.spinner("Retrieving historical context..."):
        # Return structured results with relevance scores
        results = get_historical_context(query, top_k=5, return_scores=True)

    if not results:
        st.warning(f"No historical information found for '{query}'.")
    else:
        top_score = results[0]['score']

        if top_score < LOW_RELEVANCE_THRESHOLD:
            st.warning(
                "⚠️ The system could not find a confident answer. "
                "Try rephrasing your question or asking about a different topic."
            )
        else:
            st.markdown(f"### 📚 Results for: {query}")
            for i, r in enumerate(results, start=1):
                with st.expander(f"Result {i} - Source: {r['pdf']}, Chunk #{r['chunk_position']} (Score: {r['score']:.2f})"):
                    st.markdown(r['summary'])
