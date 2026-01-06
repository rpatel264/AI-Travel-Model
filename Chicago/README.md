# Chicago Historical Documents Processing Module

## Purpose

This module extracts and summarizes historical Chicago PDFs, making text searchable, chunkable, and summarize-able for the AI Travel Assistant.

## Project Structure

```
Chicago/
├── Data/
│   ├── Raw/                 # Original PDFs
│   ├── Proceed/             # Placeholder or staged files
│   └── processed/           # Outputs from pipelines
├── .ipynb_checkpoints/      # Jupyter checkpoints (optional)
├── engineering_pipeline.py  # Orchestrates PDF processing and summarization
├── pdf_pipeline.py          # PDF extraction, cleaning, and chunking
├── query_chunks.py          # Querying chunks by keywords
├── retrieval_v2.py          # Enhanced retrieval/search functions
├── retrieval_bullets.py     # Summarizes chunks into bullet points
├── summary_chunks.json      # Precomputed summaries of text chunks
├── python                   # Placeholder or environment script
└── README.md               # This file
```

## Workflow

### 1. PDF Ingestion
- Store original PDFs in `Data/Raw/`
- Use `Data/Proceed/` for staging files if needed

### 2. Text Processing Pipeline
- **pdf_pipeline.py.txt**: Extracts text, cleans formatting, chunks documents into ~500-word sections
- Processed chunks stored in `Data/processed/`

### 3. Summarization
- **engineering_pipeline.py**: Orchestrates the workflow
- Summarization via Ollama (LLaMA-based local model)
- Precomputed summaries stored in `summary_chunks.json`

### 4. Query and Retrieval
- **query_chunks.py**: Keyword or semantic search
- **retrieval_v2.py**: Enhanced retrieval/search functions
- **retrieval_bullets.py**: Generates bullet-point summaries for quick review

## Usage

### Processing PDFs
```bash
# Run the engineering pipeline
python engineering_pipeline.py
```

### Querying Chunks
```bash
# Search by keywords
python query_chunks.py

# Enhanced search
python retrieval_v2.py

# Get bullet summaries
python retrieval_bullets.py
```

## File Notes

- **PDFs**: Historical Chicago documents
- **Processed JSON/TXT files**: Store cleaned text and summaries
- **Python scripts**: Drive the workflow from extraction → summarization → retrieval
- **.ipynb_checkpoints/**: Optional, mostly for local development

## Best Practices

1. **Git Workflow**: Only add one PDF at a time to avoid large Git pushes
2. **Processed Outputs**: Keep processed outputs and precomputed summaries to speed up retrieval
3. **Git Ignore**: Consider adding heavy PDFs to `.gitignore` if pushing to GitHub frequently

## Future Improvements

- Add proper error handling
- Implement caching for processed files
- Add configuration file for pipeline parameters
- Enhance semantic search with embeddings
- Add progress tracking for large PDF batches

## Dependencies

- PDF processing library (PyPDF2, pdfplumber, etc.)
- Ollama for local LLM summarization
- JSON for data storage
- (Additional dependencies to be added as needed)

