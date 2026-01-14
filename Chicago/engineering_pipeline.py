"""
Engineering Pipeline - Orchestrates PDF processing and summarization workflow.

This script coordinates the entire workflow:
1. PDF ingestion from Data/Raw
2. Text extraction and chunking
3. Summarization using Ollama (LLaMA-based local model)
4. Storage of precomputed summaries in summary_chunks.json
5. Retry logic for failed chunks
"""

import pdfplumber
import subprocess
import uuid
import json
import os
import time
from pathlib import Path

# =========================
# CONFIG
# =========================
# Paths relative to Chicago/ directory
RELATIVE_PDF_PATH = os.path.join("Data", "Raw", "1891-History-of-The-Chicago-Construction.pdf")

OUTPUT_JSON = "summary_chunks.json"  # Saved in Chicago/ directory
CHUNK_SIZE_WORDS = 250
MAX_CHUNKS_FOR_TEST = 5  # Set to None to process all chunks
OLLAMA_MODEL = "llama3.1:8b"
TIMEOUT_SECONDS = 300
RETRIES = 1

# =========================
# PDF EXTRACTION
# =========================
def extract_pdf_text(pdf_path):
    """Extract text from all pages of a PDF file."""
    print(f"Extracting PDF text from {os.path.basename(pdf_path)}...")
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    full_text = "\n".join(pages)
    print(f"Total words extracted: {len(full_text.split())}")
    return full_text

# =========================
# CHUNKING
# =========================
def chunk_text(text, max_words, max_chunks=None):
    """Split text into chunks of approximately max_words words."""
    words = text.split()
    chunks = []
    current = []

    for word in words:
        current.append(word)
        if len(current) >= max_words:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    if max_chunks:
        chunks = chunks[:max_chunks]

    print(f"Total chunks created: {len(chunks)}")
    return chunks

# =========================
# OLLAMA SUMMARIZATION
# =========================
def summarize_with_ollama(text, chunk_index):
    """Summarize text using Ollama with error handling and retries."""
    prompt = f"""
Summarize the FACTS from this text only in a clear, concise paragraph.
Do NOT add interpretations, claims, or causes.
No assumptions. No conclusions.

TEXT:
{text}
"""

    last_error = ""
    for attempt in range(RETRIES + 1):
        try:
            print(f"Running Ollama on chunk {chunk_index + 1} (attempt {attempt + 1})")
            start_time = time.time()

            process = subprocess.Popen(
                ["ollama", "run", OLLAMA_MODEL],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace"
            )

            stdout, stderr = process.communicate(prompt, timeout=TIMEOUT_SECONDS)
            elapsed = round(time.time() - start_time, 1)
            print(f"Chunk {chunk_index + 1} completed in {elapsed}s")

            if stderr.strip():
                print("STDERR:", stderr.strip())

            return {
                "summary": stdout.strip(),
                "status": "success",
                "retries": attempt,
                "error": stderr.strip() if stderr.strip() else None
            }

        except subprocess.TimeoutExpired:
            process.kill()
            print(f"Ollama timed out on chunk {chunk_index + 1}")
            last_error = f"Timeout on attempt {attempt + 1}"
        except Exception as e:
            print(f"Error on chunk {chunk_index + 1}: {e}")
            last_error = str(e)

    return {
        "summary": "",
        "status": "failed",
        "retries": RETRIES,
        "error": last_error
    }

# =========================
# PROCESS SINGLE PDF
# =========================
def process_pdf(pdf_path, max_chunks=None):
    """
    Process a single PDF: extract, chunk, and summarize.
    
    Args:
        pdf_path: Path to PDF file
        max_chunks: Override MAX_CHUNKS_FOR_TEST (default: uses global MAX_CHUNKS_FOR_TEST)
    """
    if max_chunks is None:
        max_chunks = MAX_CHUNKS_FOR_TEST
    
    text = extract_pdf_text(pdf_path)
    chunks = chunk_text(text, CHUNK_SIZE_WORDS, max_chunks)

    results = []

    for i, chunk in enumerate(chunks):
        print(f"\n--- Summarizing chunk {i + 1}/{len(chunks)} ---")
        summary = summarize_with_ollama(chunk, i)
        results.append({
            "id": str(uuid.uuid4()),
            "chunk_position": i,
            "chunk_text": chunk,
            "summary_text": summary["summary"],
            "status": summary["status"],
            "retries": summary["retries"],
            "error": summary["error"],
            "text_preview": chunk[:300],
            "pdf_path": os.path.basename(pdf_path)
        })

    return results

# =========================
# RETRY FAILED CHUNKS
# =========================
def retry_failed_chunks(all_results):
    """Retry summarization for chunks that failed."""
    print("\n=== Retrying failed chunks ===")
    failed_chunks = [c for c in all_results if c['status'] == 'failed']
    print(f"Found {len(failed_chunks)} failed chunks to retry.")

    for chunk in failed_chunks:
        print(f"\nRetrying chunk {chunk['chunk_position']} from {chunk['pdf_path']}")
        summary_result = summarize_with_ollama(chunk['chunk_text'], chunk['chunk_position'])
        chunk['summary_text'] = summary_result['summary']
        chunk['status'] = summary_result['status']
        chunk['retries'] += 1
        chunk['error'] = summary_result['error']

    print("\nRetry complete.")
    return all_results

# =========================
# LIST AVAILABLE PDFs
# =========================
def list_available_pdfs(raw_dir=None):
    """List all PDF files in Data/Raw directory."""
    if raw_dir is None:
        script_dir = Path(__file__).parent
        raw_dir = script_dir / "Data" / "Raw"
    else:
        raw_dir = Path(raw_dir)
    
    if not raw_dir.exists():
        return []
    
    pdf_files = sorted(raw_dir.glob("*.pdf"))
    return pdf_files

# =========================
# LOAD EXISTING RESULTS
# =========================
def load_existing_results(output_file):
    """Load existing results from JSON file."""
    output_file = Path(output_file)
    if output_file.exists():
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Handle different JSON structures
            if isinstance(data, list):
                # Already a list of chunks
                return data
            elif isinstance(data, dict):
                # Check if it's the old format with "summaries" key
                if "summaries" in data:
                    return data["summaries"]
                # Otherwise return empty list (new format expected)
                return []
            else:
                return []
    return []

# =========================
# MERGE RESULTS
# =========================
def merge_results(existing_results, new_results):
    """Merge new results with existing, replacing chunks from same PDF."""
    if not new_results:
        return existing_results
    
    # Ensure existing_results is a list of dictionaries
    if not isinstance(existing_results, list):
        existing_results = []
    
    # Filter out any non-dict items from existing_results
    existing_results = [chunk for chunk in existing_results if isinstance(chunk, dict)]
    
    # Get PDF name from new results
    if new_results and isinstance(new_results[0], dict):
        new_pdf_name = new_results[0].get('pdf_path', '')
    else:
        new_pdf_name = ''
    
    # Remove existing chunks from the same PDF (replace with new ones)
    existing_results = [chunk for chunk in existing_results 
                       if isinstance(chunk, dict) and chunk.get('pdf_path', '') != new_pdf_name]
    
    # Add new results (ensure they're all dicts)
    new_results = [chunk for chunk in new_results if isinstance(chunk, dict)]
    
    return existing_results + new_results

# =========================
# PROCESS MULTIPLE PDFs
# =========================
def process_multiple_pdfs(pdf_paths, output_file=None, append=True, max_chunks_override=None):
    """
    Process multiple PDFs and merge results.
    
    Args:
        pdf_paths: List of PDF paths to process
        output_file: Output JSON filename
        append: If True, append to existing file; if False, overwrite
        max_chunks_override: Override MAX_CHUNKS_FOR_TEST for this run
    """
    script_dir = Path(__file__).parent
    if output_file is None:
        output_file = script_dir / OUTPUT_JSON
    else:
        output_file = Path(output_file)
    
    # Load existing results if appending
    all_results = []
    if append and output_file.exists():
        all_results = load_existing_results(output_file)
        print(f"Loaded {len(all_results)} existing chunks from {output_file.name}")
    
    # Process each PDF
    for i, pdf_path in enumerate(pdf_paths, 1):
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            print(f"⚠️  Skipping {pdf_path.name} - file not found")
            continue
        
        print(f"\n{'='*60}")
        print(f"Processing PDF {i}/{len(pdf_paths)}: {pdf_path.name}")
        print(f"{'='*60}")
        
        # Temporarily override MAX_CHUNKS_FOR_TEST if specified
        # Store original value
        original_max = MAX_CHUNKS_FOR_TEST
        # Use override if provided, otherwise use global
        chunks_to_process = max_chunks_override if max_chunks_override is not None else MAX_CHUNKS_FOR_TEST
        
        try:
            # Process the PDF with specified chunk limit
            pdf_results = process_pdf(pdf_path, max_chunks=chunks_to_process)
            
            # Retry failed chunks
            pdf_results = retry_failed_chunks(pdf_results)
            
            # Merge with existing results
            all_results = merge_results(all_results, pdf_results)
            
            print(f"✓ Processed {len(pdf_results)} chunks from {pdf_path.name}")
        except Exception as e:
            print(f"✗ Error processing {pdf_path.name}: {e}")
    
    # Save merged results
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print(f"✓ Processing complete!")
    print(f"  Total chunks: {len(all_results)}")
    print(f"  Saved to: {output_file}")
    print(f"{'='*60}")
    
    return all_results

# =========================
# MAIN PIPELINE
# =========================
def main(pdf_path=None, output_file=None, append=True, max_chunks_override=None):
    """
    Main orchestration function.
    
    Args:
        pdf_path: Path to PDF file(s) - can be single path, list of paths, or None for interactive
        output_file: Output JSON filename (default: summary_chunks.json)
        append: If True, append to existing file; if False, overwrite
        max_chunks_override: Override MAX_CHUNKS_FOR_TEST for this run
    """
    print("ENGINEERING HISTORY PIPELINE — v2 (INCREMENTAL PROCESSING MODE)")
    print("="*60)
    
    script_dir = Path(__file__).parent
    raw_dir = script_dir / "Data" / "Raw"
    
    # If no PDF specified, list available and let user choose
    if pdf_path is None:
        pdf_files = list_available_pdfs(raw_dir)
        
        if not pdf_files:
            print(f"\n⚠️  No PDFs found in {raw_dir}")
            print("Please add PDFs to Chicago/Data/Raw/")
            return
        
        print(f"\nFound {len(pdf_files)} PDF file(s):\n")
        for i, pdf in enumerate(pdf_files, 1):
            size_mb = pdf.stat().st_size / (1024 * 1024)
            print(f"  {i}. {pdf.name} ({size_mb:.2f} MB)")
        
        print("\nOptions:")
        print("  - Enter number(s) to process specific PDF(s) (e.g., '1' or '1,3,5')")
        print("  - Enter 'all' to process all PDFs")
        print("  - Enter 'test' to process first PDF with MAX_CHUNKS_FOR_TEST=5")
        print("  - Press Enter to exit")
        
        choice = input("\nYour choice: ").strip().lower()
        
        if not choice:
            print("Exiting...")
            return
        
        if choice == 'all':
            pdf_paths = pdf_files
        elif choice == 'test':
            pdf_paths = [pdf_files[0]] if pdf_files else []
            max_chunks_override = 5
            print(f"\n🧪 TEST MODE: Processing first PDF with only 5 chunks")
        else:
            # Parse numbers
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(',')]
                pdf_paths = [pdf_files[i] for i in indices if 0 <= i < len(pdf_files)]
                if not pdf_paths:
                    print("Invalid selection. Exiting...")
                    return
            except ValueError:
                print("Invalid input. Exiting...")
                return
    else:
        # Convert single path or list to list
        if isinstance(pdf_path, (str, Path)):
            pdf_paths = [pdf_path]
        else:
            pdf_paths = pdf_path
    
    # Determine output file
    if output_file is None:
        output_file = script_dir / OUTPUT_JSON
    else:
        output_file = Path(output_file)
    
    # Process PDFs
    return process_multiple_pdfs(pdf_paths, output_file, append, max_chunks_override)

if __name__ == "__main__":
    main()

