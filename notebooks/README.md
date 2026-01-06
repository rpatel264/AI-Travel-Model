# Jupyter Notebooks

This directory contains Jupyter notebooks for:
- Interactive development and testing
- Data exploration
- Experimenting with queries and retrieval
- Visualizing results

## Recommended Notebooks

- `00_main_pipeline_hub.ipynb` - **Main experimentation and orchestration hub**
  - Load and inspect PDFs
  - Test chunking and summarization
  - Prototype full pipeline
  - Debug and document issues
  - This is your primary workspace for development

- `01_pdf_processing.ipynb` - Focused test of PDF extraction and chunking
- `00_template.ipynb` - Template for creating new notebooks

## Usage

1. Start Jupyter from project root:
   ```bash
   jupyter notebook notebooks/
   ```

2. Import modules from parent directory:
   ```python
   import sys
   from pathlib import Path
   project_root = Path().parent
   chicago_dir = project_root / "Chicago"
   sys.path.insert(0, str(chicago_dir))
   
   from pdf_pipeline import process_pdf
   from query_chunks import query_chunks
   ```

## Workflow

1. **Start with `00_main_pipeline_hub.ipynb`** - This is your main experimentation workspace
2. **Test individual components** - Use focused notebooks for specific testing
3. **Refactor to scripts** - Once confident, move tested code to Python scripts in `Chicago/`

