# Daily Progress Log Generator
# Usage: Tell Claude Code "Read prompts/daily_log.md and execute it"

## Instructions for Claude Code

You are a project tracking assistant. When this file is called, do the following automatically:

### Step 1 — Read project state
Read these files to understand current state:
- CLAUDE.md
- project1_timeline.md
- All files in logs/ (to see history)
- All files in src/ (to see what is implemented)
- Run: git log --oneline -20 (to see recent commits)

### Step 2 — Ask user ONE question
Ask only: "What did you complete today and what issues did you encounter?"
Wait for the answer before proceeding.

### Step 3 — Generate daily log
Create file: logs/YYYY-MM-DD_progress.md (use today's actual date)

Use this exact template:

---
# Daily Progress Log — [Weekday] DD/MM/YYYY
**Phase:** Week [N] — [Week title from timeline]
**Time invested:** ~[X]h (Mon–Fri 1–1.5h | Sat 3–4h | Sun 5–6h)
**Cumulative progress:** [X]% of Project 1

## Tasks completed today
- [x] Task description — `file_modified.py`

## Tasks not completed (reason)
- [ ] Task description — *Reason: [why]*

## Code changes
| File | Change type | Description |
|------|-------------|-------------|
| src/xxx.py | created/modified | What was done |

## Git commits
- `commit message here`

## Key decisions
- Decision and why

## Issues encountered
| Issue | Resolution |
|-------|------------|
| Description | How resolved |

## Tomorrow — Top 3 priorities
1. 🔴 [Critical path task]
2. 🔴 [Critical path task]
3. 🟡 [Important but flexible]

## Week [N] milestone progress
- [x] Done item
- [ ] Pending item
**On track:** Yes / No / Ahead
---

### Step 4 — Update project1_timeline.md
Apply these changes:
1. Mark completed tasks with ~~strikethrough~~ and ✅ YYYY-MM-DD
2. Redistribute incomplete tasks to next available days:
   - Mon–Fri: 1–1.5h evening → max 2 small tasks per day
   - Sat: 3–4h → max 5 tasks
   - Sun: 5–6h → max 8 tasks
3. Keep deadline 26/05/2026 FIXED — never move it
4. If ahead: add [BUFFER] tag to freed-up days
5. If behind: mark low-priority tasks [OPTIONAL] and compress
6. Update ACTUAL PROGRESS LOG table at bottom with today's entry

### Step 5 — Update CLAUDE.md
Update only the Current Status section:
- Current week number
- Next task to do
- Any new src/ files created

### Step 6 — Print commit command
Print exactly this for user to run:
git add logs/YYYY-MM-DD_progress.md project1_timeline.md CLAUDE.md
git commit -m "docs: daily log YYYY-MM-DD, [one line summary]"
git push origin main

## Rules
- All output files in English
- Use actual function names and file names — never generic placeholders
- Flag scope changes with ⚠️
- Mark critical path with 🔴, optional with 🟡, buffer with 🟢
- Never move the 26/05/2026 deadline
- Keep each log file under 80 lines
- One log file per calendar day — never merge two days into one file