import streamlit as st
from travel_assistant import get_historical_context

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

# Sidebar for optional year filtering
st.sidebar.header("Optional Year Filter")
before_year = st.sidebar.number_input(
    "Before year", min_value=1700, max_value=2099, value=None
)
after_year = st.sidebar.number_input(
    "After year", min_value=1700, max_value=2099, value=None
)

# User query input
query = st.text_input("🔍 Your question:")

if query:
    year_filter = {}
    if before_year is not None:
        year_filter["before"] = before_year
    if after_year is not None:
        year_filter["after"] = after_year

    st.info("Retrieving historical context...")
    result = get_historical_context(query, top_k=5, year_filter=year_filter or None)
    
    st.text(result)
