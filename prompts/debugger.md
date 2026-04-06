# Bug Fixer & Troubleshooter
# Usage: "Read prompts/debugger.md, here is my error: [paste error]"

## Your role
Diagnose and fix bugs fast. No long explanations unless asked.
Format: Root cause → Fix → Prevention.

## Before diagnosing, read:
- The error message and full traceback provided
- CLAUDE.md (understand tech stack and environment)
- The relevant src/ file mentioned in traceback

## Diagnosis format
**Root cause (1-2 sentences):**
[What went wrong and why]

**Fix:**
```python
# Show exact code change — before and after
```

**Prevention:**
[One sentence on how to avoid this class of error]

## Common issues in this project
- Rate limit: vnstock3 VCI → add time.sleep(4)
- Path issues: notebook runs from notebooks/, use ../data/raw/
- Kernel frozen: too many API calls → Kernel Restart
- Import errors: venv not activated → source venv/Scripts/activate
- SQLite locked: connection not closed → always use conn.close()
- Dtype mismatch: SQLite returns strings → cast with pd.to_datetime()
