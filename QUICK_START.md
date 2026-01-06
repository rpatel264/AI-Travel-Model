# Quick Start - Test, Verify, Git, Then Add More

## Your Plan ✅
1. Test with 1 PDF
2. Verify it works  
3. Upload to Git
4. Add rest of PDFs later

## Step 1: Test with 1 PDF (5-20 minutes)

### Quick Test (5 minutes - Recommended First)
```bash
cd Chicago
python engineering_pipeline.py
```
**When prompted, enter:** `test`

This processes 5 chunks from the first PDF to verify everything works.

### Verify It Works (2 minutes)
```bash
# Test a query
python query_chunks.py "chicago"

# Or test travel assistant
cd ..
python travel_assistant.py
# Try: "mayor" or "architecture" or "fire"
```

### Full Test (20 minutes - Optional)
If quick test works, process the full first PDF:
```bash
cd Chicago
python engineering_pipeline.py
```
**When prompted, enter:** `1`

## Step 2: Verify Everything Works

```bash
# From project root
cd Chicago

# Test queries work
python query_chunks.py "test query"
python retrieval_v2.py "chicago"

# Test travel assistant
cd ..
python travel_assistant.py
# Try a few queries to verify quality
```

**✅ If queries return results, you're good to go!**

## Step 3: Prepare for Git

### Check What Will Be Committed
```bash
# From project root
git status
```

**Should see:**
- ✅ All `.py` files
- ✅ `requirements.txt`
- ✅ Documentation files
- ✅ Notebooks
- ✅ `summary_chunks.json` (your test data)
- ❌ PDFs should NOT appear (they're in .gitignore)

### If PDFs Show Up
```bash
# Remove them from tracking (they're already in .gitignore)
git rm --cached Chicago/Data/Raw/*.pdf
```

## Step 4: Commit and Push to Git

### Initialize Git (if not done)
```bash
git init
```

### Add Remote Repository
```bash
git remote add origin <your-github-repo-url>
```

### Commit Everything
```bash
git add .
git commit -m "Initial commit: Chicago travel assistant - tested with 1 PDF"
```

### Push to GitHub
```bash
git branch -M main  # or 'master' if that's your default
git push -u origin main
```

## Step 5: Add Rest of PDFs Later

When you're ready to add more PDFs:

```bash
cd Chicago
python engineering_pipeline.py
```

**When prompted:**
- Enter `2,3,4,5` to process specific PDFs
- Or enter `all` to process all remaining PDFs

**Then commit the update:**
```bash
cd ..
git add Chicago/summary_chunks.json
git commit -m "Added more PDFs to knowledge base"
git push
```

## Quick Reference

### Test Commands
```bash
cd Chicago
python engineering_pipeline.py  # Enter: test (or 1)
python query_chunks.py "test"   # Verify it works
```

### Git Commands
```bash
git status                      # Check what will be committed
git add .                       # Add all files (PDFs ignored)
git commit -m "Your message"   # Commit
git push                        # Push to GitHub
```

## What Gets Committed

✅ **Will be committed:**
- All Python code
- Configuration files
- Documentation
- Test data (`summary_chunks.json`)

❌ **Will NOT be committed (in .gitignore):**
- PDF files (too large)
- Jupyter checkpoints
- Python cache files

## Troubleshooting

### "PDFs are showing in git status"
- Check `.gitignore` has `Chicago/Data/Raw/*.pdf`
- Run: `git rm --cached Chicago/Data/Raw/*.pdf`

### "Ollama not working"
- Check Ollama is running: `ollama list`
- Pull model: `ollama pull llama3.1:8b`

### "No results from queries"
- Make sure `summary_chunks.json` exists
- Check it has data: `cat Chicago/summary_chunks.json | head -20`

## You're Ready! 🚀

1. ✅ Test with 1 PDF
2. ✅ Verify it works
3. ✅ Commit to Git
4. ✅ Add more PDFs later

The system is set up perfectly for this workflow!

