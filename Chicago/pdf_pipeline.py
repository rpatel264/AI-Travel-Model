"""
PDF Pipeline - Extracts text, cleans formatting, and chunks documents.

This module handles:
- PDF text extraction using pdfplumber
- Text chunking into ~500-word sections
- Summarization using Ollama (LLaMA-based local model)
- Storing processed chunks in Data/processed/
"""

import pdfplumber
import subprocess
import uuid
import json
from pathlib import Path

##################################################
# STEP 1: LOAD PDF + EXTRACT TEXT
##################################################

def extract_pdf_text(pdf_path):
    """Extract text from all pages of a PDF file."""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for p in pdf.pages:
            text = p.extract_text()
            if text:
                pages.append(text)
    return "\n".join(pages)

##################################################
# STEP 2: CHUNK THE TEXT
##################################################

def chunk_text(text, max_tokens=500):
    """Split text into chunks of approximately max_tokens words."""
    words = text.split()
    chunks = []
    current = []

    for word in words:
        current.append(word)

        if len(current) >= max_tokens:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks

##################################################
# STEP 3: SUMMARIZE EACH CHUNK WITH OLLAMA
##################################################

def summarize_with_ollama(text):
    """Summarize text using Ollama with LLaMA model."""
    prompt = f"""
Summarize the FACTS from this text only.
Do NOT add interpretations, claims, or causes.
No assumptions. No conclusions.
Return 2-4 bullet points maximum.

TEXT:
{text}
"""

    process = subprocess.Popen(
        ["ollama", "run", "llama3.1:8b"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8"
    )

    stdout, stderr = process.communicate(prompt)

    if stderr:
        print("Ollama warning:", stderr)

    return stdout.strip()

##################################################
# STEP 4: PIPELINE FUNCTION
##################################################

def process_pdf(pdf_path, output_dir="Data/processed", save_chunks=True):
    """
    Process a PDF: extract text, chunk it, and summarize each chunk.
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save processed chunks (relative to Chicago/)
        save_chunks: Whether to save chunks to JSON file
    
    Returns:
        List of enhanced chunks with summaries
    """
    # Step 1: Extract text from PDF
    text = extract_pdf_text(pdf_path)
    
    # Step 2: Chunk the text
    raw_chunks = chunk_text(text)
    
    # Step 3: Summarize each chunk
    enhanced_chunks = []
    for i, ch in enumerate(raw_chunks):
        print(f"Processing chunk {i+1}/{len(raw_chunks)}...")
        summary = summarize_with_ollama(ch)
        enhanced_chunks.append({
            "id": str(uuid.uuid4()),
            "text": ch,
            "summary": summary,
            "pdf_path": str(pdf_path),
            "chunk_position": i
        })
    
    # Step 4: Save chunks to file if requested
    if save_chunks:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create filename from PDF name
        pdf_name = Path(pdf_path).stem
        output_file = output_path / f"{pdf_name}_chunks.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(enhanced_chunks, f, indent=2, ensure_ascii=False)
        
        print(f"\nSaved {len(enhanced_chunks)} chunks to {output_file}")
    
    return enhanced_chunks

##################################################
# STEP 5: SIMPLE RETRIEVAL TEST
##################################################

def ask_question_ollama(question, chunks):
    """
    Naive retrieval: search for question keywords in summaries.
    
    Args:
        question: Query string
        chunks: List of chunk dictionaries
    
    Returns:
        Top matching chunk or None
    """
    # Naive retrieval: search for the question keyword in summaries
    ranked = [c for c in chunks if question.lower() in c["summary"].lower()]
    
    if not ranked:
        print("No matching chunks found.")
        return None
    
    top = ranked[0]
    print("\n=== TOP CHUNK MATCH ===")
    print("Chunk ID:", top["id"])
    print("Summary:", top["summary"])
    print("Source PDF:", top["pdf_path"])
    
    return top


if __name__ == "__main__":
    # Example usage - adjust path as needed
    # Get the Chicago directory path relative to this script
    script_dir = Path(__file__).parent
    pdf_path = script_dir / "Data" / "Raw" / "Chicago_Timeline_Honorary_Chicago.pdf"
    
    if not pdf_path.exists():
        print(f"PDF not found at: {pdf_path}")
        print("Please add a PDF to Chicago/Data/Raw/")
    else:
        # Process the PDF: extract text, chunk it, summarize each chunk
        chunks = process_pdf(pdf_path)
        
        print("\n=== PROCESSING COMPLETE ===")
        print(f"Extracted {len(chunks)} chunks.")
        
        # Test retrieval by asking a sample question
        ask_question_ollama("mayor chicago", chunks)

