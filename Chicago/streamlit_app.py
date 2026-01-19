import streamlit as st
from travel_assistant import get_historical_context, get_chunks

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

# Always use semantic search
search_method = "Semantic Search"

# Optional: debug info for chunks (can remove entirely later)
chunks = get_chunks()
st.sidebar.write("✅ Loaded chunks")
if chunks:
    st.sidebar.write(f"Number of chunks: {len(chunks)}")
    st.sidebar.write(f"First chunk preview: {chunks[0]['summary_text'][:100]}...")

# User query input
query = st.text_input("🔍 Your question:")

if query:
    with st.spinner("Retrieving historical context..."):
        result_text = get_historical_context(query, top_k=5)

    # Split results by chunk separator
    chunks_output = result_text.split("-" * 60)

    st.markdown(f"### 📚 Results for: {query}")

    for i, chunk in enumerate(chunks_output, start=1):
        chunk = chunk.strip()
        if not chunk:
            continue
        with st.expander(f"Result {i}"):
            st.markdown(chunk)
