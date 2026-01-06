# Incremental PDF Processing Guide

This guide explains how to process PDFs incrementally - test with a few first, then process the rest.

## Quick Start: Test with One PDF

### Option 1: Interactive Mode (Recommended)

```bash
cd Chicago
python engineering_pipeline.py
```

This will:
1. List all PDFs in `Data/Raw/`
2. Let you choose which to process
3. Support test mode (5 chunks) or full processing
4. Append results to existing `summary_chunks.json`

**Interactive Options:**
- Enter a number (e.g., `1`) to process that PDF
- Enter multiple numbers (e.g., `1,3,5`) to process multiple PDFs
- Enter `all` to process all PDFs
- Enter `test` to process first PDF with only 5 chunks (for testing)
- Press Enter to exit

### Option 2: Command Line

```bash
cd Chicago

# Process specific PDF (test mode - 5 chunks)
python process_pdf.py <pdf_filename>

# Process specific PDF (full)
python engineering_pipeline.py <path_to_pdf>

# Process multiple PDFs
python -c "from engineering_pipeline import main; main(pdf_path=['Data/Raw/pdf1.pdf', 'Data/Raw/pdf2.pdf'], append=True)"
```

### Option 3: Jupyter Notebook

Open `notebooks/00_main_pipeline_hub.ipynb` and use Step 4 to test with limited chunks first.

## Processing Workflow

### Step 1: Test with One PDF (5 chunks)

```bash
cd Chicago
python engineering_pipeline.py
# Choose: test
```

This processes only 5 chunks from the first PDF to verify everything works.

### Step 2: Verify Results

Check the output:
- Are summaries being generated?
- Do they look reasonable?
- Any errors?

You can also test queries:
```bash
python query_chunks.py "test query"
```

### Step 3: Process One Full PDF

```bash
cd Chicago
python engineering_pipeline.py
# Choose: 1
```

This processes all chunks from the first PDF.

### Step 4: Process Additional PDFs

```bash
cd Chicago
python engineering_pipeline.py
# Choose: 2,3,4  (or specific numbers)
```

Or process all remaining:
```bash
# Choose: all
```

## Features

### Append Mode (Default)
- New results are merged with existing `summary_chunks.json`
- If you process the same PDF again, old chunks are replaced
- Safe to run multiple times

### Test Mode
- Process only 5 chunks per PDF
- Fast way to verify everything works
- Use `max_chunks_override=5` parameter

### Selective Processing
- Choose specific PDFs to process
- Skip PDFs you don't want yet
- Process in any order

## Example Session

```bash
$ cd Chicago
$ python engineering_pipeline.py

ENGINEERING HISTORY PIPELINE — v2 (INCREMENTAL PROCESSING MODE)
============================================================

Found 5 PDF file(s):

  1. Chicago_Timeline_Honorary_Chicago.pdf (2.3 MB)
  2. History_of_Chicago_Construction.pdf (5.1 MB)
  3. Chicago_Architecture_Guide.pdf (1.8 MB)
  4. Chicago_Fire_History.pdf (3.2 MB)
  5. Chicago_Mayors.pdf (0.9 MB)

Options:
  - Enter number(s) to process specific PDF(s) (e.g., '1' or '1,3,5')
  - Enter 'all' to process all PDFs
  - Enter 'test' to process first PDF with MAX_CHUNKS_FOR_TEST=5
  - Press Enter to exit

Your choice: test

🧪 TEST MODE: Processing first PDF with only 5 chunks

============================================================
Processing PDF 1/1: Chicago_Timeline_Honorary_Chicago.pdf
============================================================
...
✓ Processed 5 chunks from Chicago_Timeline_Honorary_Chicago.pdf

============================================================
✓ Processing complete!
  Total chunks: 5
  Saved to: summary_chunks.json
============================================================
```

## Tips

1. **Start Small**: Always test with `test` mode or `max_chunks_override=5` first
2. **Verify Results**: Check that summaries look good before processing more
3. **Process Incrementally**: Do 1-2 PDFs at a time, especially for large files
4. **Use Append Mode**: Keeps existing results safe
5. **Check Progress**: Results are saved after each PDF, so you can stop anytime

## Troubleshooting

### PDF Not Found
- Make sure PDFs are in `Chicago/Data/Raw/`
- Check filename spelling

### Ollama Errors
- Ensure Ollama is running: `ollama list`
- Check model is available: `ollama pull llama3.1:8b`

### Out of Memory
- Process smaller PDFs first
- Use test mode to verify before full processing
- Process one PDF at a time

### Want to Start Over
- Delete `summary_chunks.json`
- Run pipeline again (will create new file)

## Advanced Usage

### Programmatic Processing

```python
from engineering_pipeline import main, list_available_pdfs

# List PDFs
pdfs = list_available_pdfs()

# Process first PDF (test mode)
main(pdf_path=pdfs[0], append=True, max_chunks_override=5)

# Process first PDF (full)
main(pdf_path=pdfs[0], append=True)

# Process multiple PDFs
main(pdf_path=pdfs[:3], append=True)  # First 3 PDFs

# Process all PDFs
main(pdf_path=pdfs, append=True)
```

### Custom Configuration

Edit `engineering_pipeline.py`:
```python
CHUNK_SIZE_WORDS = 250  # Adjust chunk size
MAX_CHUNKS_FOR_TEST = 5  # Test mode chunk limit
OLLAMA_MODEL = "llama3.1:8b"  # Change model
TIMEOUT_SECONDS = 300  # Adjust timeout
RETRIES = 1  # Number of retries
```

## Next Steps

After processing PDFs:
1. Test queries: `python query_chunks.py "your query"`
2. Use travel assistant: `python travel_assistant.py`
3. Explore in notebook: `jupyter notebook notebooks/00_main_pipeline_hub.ipynb`

