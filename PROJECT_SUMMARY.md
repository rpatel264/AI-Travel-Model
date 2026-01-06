# AI Travel Model - Chicago Historical Context Assistant

## Project Overview

This project is an AI-powered travel assistant that provides historical context and information about Chicago locations, landmarks, and events to enhance travel experiences. The system processes historical Chicago PDFs, extracts and summarizes content, and makes it searchable for travelers.

## Project Structure

```
AI-Travel-Model/
├── Chicago/                          # Core processing modules
│   ├── Data/
│   │   ├── Raw/                      # Original PDFs (add your PDFs here)
│   │   ├── Proceed/                  # Staging files
│   │   └── processed/                # Processed chunks and outputs
│   ├── engineering_pipeline.py      # Main orchestration with error handling
│   ├── pdf_pipeline.py               # PDF extraction, chunking, summarization
│   ├── query_chunks.py               # Keyword search with PDF filtering
│   ├── retrieval_v2.py               # Simple keyword search
│   ├── retrieval_bullets.py          # Keyword search with year filtering
│   ├── summary_chunks.json           # Precomputed summaries (generated)
│   └── .gitignore                    # Git ignore rules
├── notebooks/                        # Jupyter notebooks for development
│   ├── 00_main_pipeline_hub.ipynb   # Main experimentation hub
│   ├── 01_pdf_processing.ipynb       # PDF processing tests
│   └── 00_template.ipynb             # Template notebook
├── travel_assistant.py               # Main travel assistant interface
├── requirements.txt                  # Python dependencies
├── README.md                         # Project documentation
└── PROJECT_SUMMARY.md                # This file
```

## Core Modules

### 1. `pdf_pipeline.py`
**Purpose**: PDF text extraction, chunking, and summarization

**Key Functions**:
- `extract_pdf_text(pdf_path)` - Extract text from PDF
- `chunk_text(text, max_tokens=500)` - Split text into chunks
- `summarize_with_ollama(text)` - Summarize using Ollama
- `process_pdf(pdf_path)` - Full pipeline: extract → chunk → summarize → save

**Features**:
- Uses pdfplumber for extraction
- Chunks by word count (~500 words default)
- Integrates with Ollama (llama3.1:8b)
- Saves chunks to `Data/processed/`

### 2. `engineering_pipeline.py`
**Purpose**: Production-ready pipeline with error handling

**Key Functions**:
- `process_pdf(pdf_path)` - Process single PDF with retry logic
- `retry_failed_chunks(all_results)` - Retry failed summarizations
- `main(pdf_path, output_file)` - Main orchestration

**Features**:
- Error handling and retries
- Timeout protection (300 seconds)
- Status tracking per chunk
- Configurable chunk size (250 words default)
- Test mode with `MAX_CHUNKS_FOR_TEST`
- Saves to `summary_chunks.json`

**Configuration**:
```python
CHUNK_SIZE_WORDS = 250
MAX_CHUNKS_FOR_TEST = 5  # Set to None for all chunks
OLLAMA_MODEL = "llama3.1:8b"
TIMEOUT_SECONDS = 300
RETRIES = 1
```

### 3. `query_chunks.py`
**Purpose**: Keyword search with PDF filtering

**Key Functions**:
- `load_chunks(path)` - Load chunks from JSON
- `search(query, chunks, top_k, pdf_filter)` - Search with PDF filter
- `query_chunks(query, ...)` - Programmatic search function

**Features**:
- Keyword-based scoring
- Filter by specific PDF file
- Top-K result ranking
- Command-line and programmatic interfaces

**Usage**:
```bash
python query_chunks.py "mayor chicago"
python query_chunks.py "architecture" --pdf Chicago_Timeline
```

### 4. `retrieval_v2.py`
**Purpose**: Simple keyword search

**Key Functions**:
- `load_chunks(path)` - Load chunks from JSON
- `search_chunks(query, chunks, top_k)` - Simple keyword search
- `enhanced_search(query, ...)` - Programmatic search

**Features**:
- Simple keyword matching
- Top-K ranking
- Easy to use interface

**Usage**:
```bash
python retrieval_v2.py "mayor chicago"
python retrieval_v2.py "architecture history"
```

### 5. `retrieval_bullets.py`
**Purpose**: Keyword search with year filtering

**Key Functions**:
- `load_chunks(path)` - Load chunks from JSON
- `search_chunks(query, chunks, before, after, top_k)` - Search with year filters
- `extract_years(text)` - Extract years from text

**Features**:
- Keyword-based search
- Year filtering (`--before`, `--after`)
- Top-K results
- Formatted bullet-point output

**Usage**:
```bash
python retrieval_bullets.py "architecture" --before 1900
python retrieval_bullets.py "fire" --after 1870
```

### 6. `travel_assistant.py`
**Purpose**: Main user interface for the travel assistant

**Key Functions**:
- `get_historical_context(query, top_k, year_filter)` - Get context for query
- `main()` - Interactive command-line interface

**Features**:
- Interactive query interface
- Automatic year filter detection
- Formatted output for travel context
- Help system

**Usage**:
```bash
python travel_assistant.py
```

## Workflow

### 1. Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Ensure Ollama is installed and running
# ollama pull llama3.1:8b
```

### 2. Add PDFs
Place historical Chicago PDFs in `Chicago/Data/Raw/`

### 3. Process Documents
```bash
cd Chicago
python engineering_pipeline.py
```

This will:
- Extract text from PDFs
- Chunk into ~250 word pieces
- Summarize each chunk with Ollama
- Save to `summary_chunks.json`
- Retry any failed chunks

### 4. Query Historical Information

**Option A: Interactive Travel Assistant**
```bash
python travel_assistant.py
```

**Option B: Command Line Tools**
```bash
cd Chicago
python query_chunks.py "mayor chicago"
python retrieval_v2.py "architecture"
python retrieval_bullets.py "fire" --after 1870
```

**Option C: Jupyter Notebooks**
```bash
jupyter notebook notebooks/00_main_pipeline_hub.ipynb
```

## Jupyter Notebooks

### `00_main_pipeline_hub.ipynb`
Main experimentation hub for:
- Loading and inspecting PDFs
- Testing chunking
- Testing summarization
- Prototyping full pipeline
- Loading and inspecting processed chunks
- Testing queries
- Documentation

### `01_pdf_processing.ipynb`
Focused testing of PDF processing workflow

## Data Flow

```
PDF Files (Data/Raw/)
    ↓
engineering_pipeline.py
    ↓
Extract Text → Chunk → Summarize (Ollama)
    ↓
summary_chunks.json
    ↓
Query Modules (query_chunks, retrieval_v2, retrieval_bullets)
    ↓
travel_assistant.py
    ↓
User-friendly Historical Context
```

## Configuration

### Chunk Sizes
- `pdf_pipeline.py`: 500 words (default)
- `engineering_pipeline.py`: 250 words (default)

### Ollama Settings
- Model: `llama3.1:8b`
- Timeout: 300 seconds
- Retries: 1

### Output Files
- `summary_chunks.json`: Main summary file (Chicago/)
- `*_chunks.json`: Individual PDF chunks (Data/processed/)

## Dependencies

Key dependencies (see `requirements.txt`):
- `pdfplumber` - PDF text extraction
- `ollama` - Local LLM for summarization
- Standard library: `json`, `subprocess`, `pathlib`, `argparse`

## Usage Examples

### Process a PDF
```bash
cd Chicago
python engineering_pipeline.py
```

### Search for Information
```bash
# Interactive
python travel_assistant.py

# Command line
cd Chicago
python query_chunks.py "mayor chicago"
python retrieval_bullets.py "architecture" --before 1900
```

### Use in Code
```python
from query_chunks import query_chunks, load_chunks

chunks = load_chunks()
results = query_chunks("mayor chicago", chunks, top_k=5)

for score, chunk in results:
    print(chunk['summary_text'])
```

## Troubleshooting

### No chunks found
- Run `engineering_pipeline.py` first
- Check that `summary_chunks.json` exists in `Chicago/`

### Ollama errors
- Ensure Ollama is installed and running
- Check model is available: `ollama list`
- Pull model if needed: `ollama pull llama3.1:8b`

### PDF extraction issues
- Some PDFs may need OCR (scanned images)
- Check extraction quality in notebook first
- Verify PDF is not encrypted

## Future Enhancements

- [ ] Web interface or API
- [ ] Location-based queries (GPS integration)
- [ ] Semantic search with embeddings
- [ ] Multi-language support
- [ ] Real-time updates
- [ ] Integration with travel apps
- [ ] Better error recovery
- [ ] Progress tracking for large batches

## Git Workflow

- Add PDFs one at a time to avoid large commits
- Consider adding large PDFs to `.gitignore`
- Keep processed outputs for faster retrieval
- Commit code changes separately from data

## Notes

- All paths are relative to their respective directories
- Modules handle both `summary_text` and `summary` field names for compatibility
- Error handling is built into `engineering_pipeline.py`
- Notebooks are for experimentation; scripts are for production

## Getting Started

1. Clone or download the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Ollama: `ollama pull llama3.1:8b`
4. Add PDFs to `Chicago/Data/Raw/`
5. Run pipeline: `cd Chicago && python engineering_pipeline.py`
6. Start assistant: `python travel_assistant.py`

---

**Last Updated**: Project setup complete with all modules integrated
**Status**: Ready for use

