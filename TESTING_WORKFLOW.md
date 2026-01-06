# Testing Workflow - Verify Before Processing All PDFs

## Your Goal
✅ Have the AI model use information from **ALL PDFs**  
✅ But **test first** to make sure everything works  
✅ Then process the rest incrementally

## Recommended Testing Workflow

### Phase 1: Test with ONE PDF (5 chunks) - 5 minutes

```bash
cd Chicago
python engineering_pipeline.py
# Enter: test
```

**What this does:**
- Processes only 5 chunks from the first PDF
- Creates `summary_chunks.json` with test data
- Takes ~2-5 minutes depending on Ollama speed

**Why this first:**
- Verifies Ollama is working
- Checks that summarization works
- Ensures no errors in the pipeline
- Fast feedback

### Phase 2: Test Queries - 2 minutes

```bash
# Test that queries work
python query_chunks.py "mayor"
python retrieval_v2.py "chicago"
python travel_assistant.py
# Try a few queries
```

**What this verifies:**
- Search functionality works
- Results are returned correctly
- Travel assistant can access the data

### Phase 3: Process ONE Full PDF - 10-30 minutes

```bash
cd Chicago
python engineering_pipeline.py
# Enter: 1
```

**What this does:**
- Processes ALL chunks from the first PDF
- Replaces the test chunks with full data
- Gives you a complete dataset to test with

**Why this second:**
- Tests with real data volume
- Verifies performance is acceptable
- Confirms full pipeline works end-to-end

### Phase 4: Test Full Workflow - 5 minutes

```bash
# Test queries with full PDF data
python travel_assistant.py
# Try various queries about Chicago history
# Verify results are good quality
```

**What this verifies:**
- Quality of summaries is good
- Queries return relevant results
- System is ready for more PDFs

### Phase 5: Process Remaining PDFs - As needed

Once you're confident it works:

```bash
cd Chicago
python engineering_pipeline.py
# Enter: 2,3,4,5  (or however many you have)
# Or enter: all
```

**What this does:**
- Processes remaining PDFs
- **Automatically merges** all results into `summary_chunks.json`
- Final file contains data from ALL PDFs

## Key Points

### ✅ Results Are Merged Automatically
- Each time you process a PDF, results are **added** to `summary_chunks.json`
- The final file will contain chunks from **ALL processed PDFs**
- The AI model queries this single file, so it has access to everything

### ✅ Safe to Process Incrementally
- You can process 1 PDF, test, then process more
- Each PDF's results are merged into the master file
- If you process the same PDF again, old chunks are replaced (no duplicates)

### ✅ Test Before Committing
- Start with test mode (5 chunks) - takes 5 minutes
- Then one full PDF - takes 10-30 minutes
- Test queries to verify quality
- Then process the rest

## Example Session

```bash
# Step 1: Quick test (5 chunks)
$ cd Chicago
$ python engineering_pipeline.py
Your choice: test
# ... processes 5 chunks ...
# ✓ Done in 5 minutes

# Step 2: Test queries work
$ python query_chunks.py "mayor"
# ✓ Returns results - system works!

# Step 3: Process one full PDF
$ python engineering_pipeline.py
Your choice: 1
# ... processes all chunks from PDF 1 ...
# ✓ Done in 20 minutes

# Step 4: Test with real data
$ python travel_assistant.py
# Try queries, verify quality
# ✓ Everything looks good!

# Step 5: Process remaining PDFs
$ python engineering_pipeline.py
Your choice: 2,3,4,5
# ... processes remaining PDFs ...
# ✓ All PDFs now in summary_chunks.json
```

## Final Result

After processing all PDFs:
- `summary_chunks.json` contains chunks from **ALL PDFs**
- Travel assistant queries this file
- AI model has access to information from **every PDF you processed**

## What If Something Goes Wrong?

### If test mode fails:
- Check Ollama is running
- Verify PDF is readable
- Check error messages

### If one PDF fails:
- Skip it, process others
- Come back to fix it later
- System continues with other PDFs

### If you want to start over:
- Delete `summary_chunks.json`
- Start fresh with test mode

## Summary

1. **Test first** (5 chunks) - 5 min
2. **Verify queries work** - 2 min  
3. **Process one full PDF** - 10-30 min
4. **Test full workflow** - 5 min
5. **Process remaining PDFs** - As needed

This approach ensures:
- ✅ You verify it works before committing time
- ✅ Final system has ALL PDFs
- ✅ Safe incremental processing
- ✅ No wasted time if something's wrong

