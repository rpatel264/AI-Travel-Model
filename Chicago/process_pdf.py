"""
Quick script to process a single PDF for testing.

Usage:
    python process_pdf.py <pdf_filename>
    python process_pdf.py  # Lists PDFs and lets you choose
"""

import sys
from pathlib import Path
from engineering_pipeline import main, list_available_pdfs

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Process specific PDF
        pdf_name = sys.argv[1]
        script_dir = Path(__file__).parent
        pdf_path = script_dir / "Data" / "Raw" / pdf_name
        
        if not pdf_path.exists():
            print(f"PDF not found: {pdf_path}")
            print("\nAvailable PDFs:")
            for pdf in list_available_pdfs():
                print(f"  - {pdf.name}")
            sys.exit(1)
        
        main(pdf_path=pdf_path, append=True, max_chunks_override=5)
    else:
        # Interactive mode
        main()


