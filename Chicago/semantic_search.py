# semantic_search.py
from sentence_transformers import SentenceTransformer
import numpy as np

# Load model once
_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts):
    """Convert list of strings to embedding vectors."""
    return _model.encode(texts, normalize_embeddings=True)

def cosine_similarity(vec_a, vec_b):
    return float(np.dot(vec_a, vec_b))

def semantic_search(query, chunks, top_k=3):
    """
    Rank chunks by semantic similarity to query.
    
    Args:
        query: string
        chunks: list of dicts with "summary_text" or "summary"
        top_k: number of results to return
    """
    summaries = [chunk.get("summary_text") or chunk.get("summary", "") for chunk in chunks]
    
    query_vec = embed_texts([query])[0]
    chunk_vecs = embed_texts(summaries)
    
    scored = []
    for vec, chunk in zip(chunk_vecs, chunks):
        score = cosine_similarity(query_vec, vec)
        scored.append((score, chunk))
    
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]
