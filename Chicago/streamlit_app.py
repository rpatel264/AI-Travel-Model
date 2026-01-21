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

if query:
    with st.spinner("Retrieving historical context..."):
        # Set return_scores=True so we get similarity scores
        results = get_historical_context(query, top_k=5, return_scores=True)

    if not results:
        st.warning("No results found. Try rephrasing your question.")
    else:
        # Compute the highest similarity score
        top_score = max(result["similarity"] for result in results)
        relevance_threshold = 0.6  # tweak this threshold if needed

        # Show a message if the top score is low
        if top_score < relevance_threshold:
            st.info(
                "⚠️ The system could not find a highly relevant answer. "
                "Try rephrasing your question or asking about a different topic."
            )

        st.markdown(f"### 📚 Results for: {query}")

        # Display the chunks
        for i, result in enumerate(results, start=1):
            chunk_text = result["text"].strip()
            if not chunk_text:
                continue
            with st.expander(f"Result {i} (Score: {result['similarity']:.2f})"):
                st.markdown(chunk_text)
