# Git & GitHub Workflow Helper
# Usage: "Read prompts/git_helper.md, help me with: [git issue]"

## Your role
Help with git operations. Be precise — git mistakes are hard to undo.

## Project git conventions

### Commit message format (Conventional Commits)
feat:     new feature or module
fix:      bug fix
docs:     README, logs, comments
refactor: code improvement, no new feature
test:     test cases
chore:    tooling, config, dependencies

### Examples for this project
feat: implement calc_returns() in src/features.py
feat: add minimum variance optimizer, test on 5 ticker combos
fix: handle missing dates with forward fill in features.py
docs: daily log 2026-04-06, week 3 returns module started
refactor: extract db connection to helper function in data_loader.py
chore: add scipy to requirements.txt

### Daily workflow
```bash
# Start of session
source venv/Scripts/activate

# End of session  
git add [specific files — never git add .]
git status  # review what's being committed
git commit -m "type: description"
git push origin main
```

### Files to NEVER commit
- data/raw/portfolio.db (in .gitignore)
- venv/ (in .gitignore)
- .ipynb_checkpoints/ (in .gitignore)
- *.csv, *.h5, *.pkl (in .gitignore)

### Common fixes
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo changes to a file
git checkout -- src/filename.py

# See what changed
git diff src/filename.py

# Check what will be committed
git status
git diff --staged
```
