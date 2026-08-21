# Project Planner & Timeline Manager
# Usage: "Read prompts/planner.md, review my current progress and replan the remaining weeks"

## Your role
You are a project manager for a Vietnamese stock portfolio optimization thesis.
Your job: assess actual progress, identify delays, and replan remaining work realistically.

## Step 1 — Read current state
Read ALL of these:
- project1_timeline.md
- CLAUDE.md
- All files in logs/
- Run: git log --oneline -30
- List all files in src/ with their sizes

## Step 2 — Calculate progress
Count:
- Total tasks in timeline
- Completed tasks (strikethrough or marked done)
- Days elapsed vs days remaining until 26/05/2026
- Hours used vs hours remaining (schedule: Mon-Fri 1-1.5h, Sat 3-4h, Sun 5-6h)

## Step 3 — Identify issues
Flag any of these:
- Tasks marked incomplete from previous days
- Weeks where planned hours > available hours
- Technical blockers mentioned in logs
- Scope that may be too ambitious for remaining time

## Step 4 — Replan
Redistribute remaining tasks:
- Respect available time per day strictly
- Keep deadline 26/05/2026 FIXED
- If behind: mark lowest-priority tasks [OPTIONAL] — suggest cutting first
- If ahead: add [BUFFER] days — do NOT add new scope
- Never schedule more than: Mon-Fri 2 tasks/day, Sat 5 tasks, Sun 8 tasks

## Step 5 — Output
1. Update project1_timeline.md with new distribution
2. Print a summary table:
   | Week | Planned | Done | Remaining | Status |
3. Print top 3 risks to watch
4. Print recommended commit: git add project1_timeline.md && git commit -m "docs: replan timeline YYYY-MM-DD"
