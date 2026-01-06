# Git Workflow - Test First, Then Upload

## Your Plan ✅
1. Test with 1 PDF
2. Verify it works
3. Upload to Git
4. Add rest of PDFs later

## Step-by-Step Guide

### Step 1: Test with 1 PDF

```bash
cd Chicago
python engineering_pipeline.py
```

**When prompted:**
- Enter `test` for quick test (5 chunks, ~5 minutes)
- OR enter `1` to process first PDF fully

**Verify it works:**
```bash
# Test queries
python query_chunks.py "test query"
python retrieval_v2.py "chicago"

# Or use travel assistant
cd ..
python travel_assistant.py
```

### Step 2: Prepare for Git

**Check what will be committed:**
```bash
# From project root
git status
```

**Important files that SHOULD be committed:**
- ✅ All Python scripts (`Chicago/*.py`)
- ✅ `travel_assistant.py`
- ✅ `requirements.txt`
- ✅ `README.md`, `PROJECT_SUMMARY.md`, etc.
- ✅ Notebooks (`notebooks/*.ipynb`)
- ✅ `summary_chunks.json` (if you want to include test data)

**Files that should NOT be committed:**
- ❌ PDFs in `Chicago/Data/Raw/*.pdf` (too large, ignored)
- ❌ `Chicago/Data/processed/*.json` (generated files, optional)
- ❌ `.ipynb_checkpoints/` (Jupyter checkpoints)

### Step 3: Initialize Git (if not already done)

```bash
# From project root
git init
git add .
git commit -m "Initial commit: Chicago travel assistant with test PDF processed"
```

### Step 4: Create .gitignore (if needed)

The `.gitignore` should already be set up, but verify it includes:

```
# Large PDF files
Chicago/Data/Raw/*.pdf

# Processed data (optional - uncomment if you don't want to track)
# Chicago/Data/processed/*.json

# Jupyter checkpoints
.ipynb_checkpoints/
**/.ipynb_checkpoints/
```

### Step 5: Commit and Push

```bash
# Check status
git status

# Add all files (PDFs will be ignored)
git add .

# Commit
git commit -m "Chicago travel assistant - tested with 1 PDF, ready for more"

# Add remote (if not already added)
git remote add origin <your-repo-url>

# Push
git push -u origin main
# or
git push -u origin master
```

### Step 6: Add Rest of PDFs Later

When ready to add more PDFs:

```bash
# Process additional PDFs
cd Chicago
python engineering_pipeline.py
# Enter: 2,3,4,5  (or specific numbers)

# Test again
python query_chunks.py "test query"

# Commit the updated summary_chunks.json (if you want)
cd ..
git add Chicago/summary_chunks.json
git commit -m "Added more PDFs to knowledge base"
git push
```

## Recommended Git Structure

### What to Commit Now:
```
✅ Code files (all .py files)
✅ Configuration (requirements.txt, .gitignore)
✅ Documentation (README.md, guides)
✅ Test data (summary_chunks.json with 1 PDF) - optional
✅ Notebooks
```

### What NOT to Commit:
```
❌ Large PDF files (in .gitignore)
❌ Generated processed files (optional)
❌ Checkpoints
```

## Quick Commands

### Test with 1 PDF:
```bash
cd Chicago
python engineering_pipeline.py
# Enter: test  (or 1 for full)
```

### Verify it works:
```bash
python query_chunks.py "chicago"
cd ..
python travel_assistant.py
```

### Git workflow:
```bash
git status                    # Check what will be committed
git add .                     # Add all (PDFs ignored)
git commit -m "Your message"  # Commit
git push                      # Push to remote
```

## Notes

### PDFs in .gitignore
- PDFs are automatically ignored
- They won't be committed to Git
- You can add them locally without worrying

### summary_chunks.json
- You can commit this if you want to share test data
- Or add it to .gitignore if you prefer to regenerate it
- Your choice!

### Adding More PDFs Later
- Process them the same way
- Results merge into same `summary_chunks.json`
- Commit the updated file when ready

## Troubleshooting

### "PDFs are being tracked"
- Check `.gitignore` includes `Chicago/Data/Raw/*.pdf`
- If already tracked: `git rm --cached Chicago/Data/Raw/*.pdf`

### "File too large"
- PDFs should be in .gitignore
- If `summary_chunks.json` is too large, add it to .gitignore too

### "Want to start fresh"
- Delete `summary_chunks.json`
- Process PDFs again
- Commit new file

