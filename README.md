# AI Travel Assistant - Chicago Historical Context

An AI-powered travel assistant that provides historical context and information about Chicago locations, landmarks, and events to enhance your travel experience.

## Overview

This application processes historical Chicago PDFs and makes them searchable, allowing travelers to query historical information about locations they're visiting or planning to visit.

## Project Structure

```
AI-Travel-Model/
├── Chicago/                      # Core processing modules
│   ├── Data/
│   │   ├── Raw/                 # Original PDFs
│   │   ├── Proceed/             # Staging files
│   │   └── processed/           # Processed chunks and outputs
│   ├── engineering_pipeline.py  # Orchestrates PDF processing
│   ├── pdf_pipeline.py          # PDF extraction and chunking
│   ├── query_chunks.py          # Keyword/semantic search
│   ├── retrieval_v2.py          # Enhanced retrieval
│   ├── retrieval_bullets.py     # Bullet-point summaries
│  n── summary_chunks.json      # Precomputed summaries
├── notebooks/                   # Jupyter notebooks for development
│   ├── 00_template.ipynb        # Template notebook
│   └── README.md                # Notebook usage guide
├── travel_assistant.py          # Main travel assistant interface
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Features

- **PDF Processing**: Extract and process historical Chicago documents
- **Text Chunking**: Break documents into searchable chunks
- **Summarization**: Generate summaries using Ollama (local LLM)
- **Query System**: Search by keywords or semantic similarity
- **Travel Context**: Get historical information about Chicago locations

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Add PDFs**
   - Place historical Chicago PDFs in `Chicago/Data/Raw/`

3. **Process Documents**
   ```bash
   cd Chicago
   python engineering_pipeline.py
   ```

4. **Run Travel Assistant**
   ```bash
   python travel_assistant.py
   ```

## Usage

### Processing Documents
```bash
# Process all PDFs in Data/Raw/
cd Chicago
python engineering_pipeline.py
```

### Querying Historical Information
```bash
# Interactive travel assistant
python travel_assistant.py

# Or use individual modules
cd Chicago
python query_chunks.py
python retrieval_v2.py
```

### Using Jupyter Notebooks
```bash
# Start Jupyter from project root
jupyter notebook notebooks/

# Or use JupyterLab
jupyter lab notebooks/
```

Notebooks allow interactive development and testing of individual components.

## Workflow

1. **PDF Ingestion**: Add PDFs to `Chicago/Data/Raw/`
2. **Processing**: Run `engineering_pipeline.py` to extract, clean, and chunk text
3. **Summarization**: Generate summaries using Ollama
4. **Query**: Use the travel assistant or query modules to get historical context

## Configuration

- **Chunk Size**: Default ~500 words (configurable in `pdf_pipeline.py`)
- **LLM**: Uses Ollama with LLaMA models (local)
- **Storage**: Processed data stored in `Chicago/Data/processed/`

## Dependencies

See `requirements.txt` for full list. Key dependencies:
- PDF processing libraries (pdfplumber, PyPDF2)
- Ollama for local LLM
- Sentence transformers for semantic search (optional)

## Git Workflow

- Add PDFs one at a time to avoid large commits
- Consider adding large PDFs to `.gitignore`
- Keep processed outputs for faster retrieval

## Future Enhancements

- Web interface or API
- Location-based queries (GPS integration)
- Integration with travel apps
- Multi-language support
- Real-time updates

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Ollama**
   ```bash
   ollama pull llama3.1:8b
   ```

3. **Add PDFs**
   - Place historical Chicago PDFs in `Chicago/Data/Raw/`

4. **Process Documents**
   ```bash
   cd Chicago
   python engineering_pipeline.py
   ```

5. **Start Travel Assistant**
   ```bash
   python travel_assistant.py
   ```

## Detailed Documentation

For comprehensive documentation, see [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## License

[Add your license here]

