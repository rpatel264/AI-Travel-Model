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

LOW_RELEVANCE_THRESHOLD = 0.6  # adjust as needed

if query:
    with st.spinner("Retrieving historical context..."):
        # Return results along with their relevance scores
        results = get_historical_context(query, top_k=5, return_scores=True)

    if not results:
        st.warning("⚠️ No relevant historical information found.")
    else:
        # Separate the chunks and scores
        chunks_output, scores = zip(*results)  # results is [(text, score), ...]
        top_score = max(scores)

        # Show message only if relevance is too low
        if top_score < LOW_RELEVANCE_THRESHOLD:
            st.info("⚠️ The system could not find a confident answer. Try rephrasing your question.")
        else:
            # Display results only if relevance is high enough
            st.markdown(f"### 📚 Results for: {query}")
            for i, chunk in enumerate(chunks_output, start=1):
                chunk = chunk.strip()
                if not chunk:
                    continue
                with st.expander(f"Result {i} (Relevance: {scores[i-1]:.2f})"):
                    st.markdown(chunk)
