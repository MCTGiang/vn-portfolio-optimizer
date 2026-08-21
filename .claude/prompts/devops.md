# Deploy & Environment Manager
# Usage: "Read prompts/devops.md, help me [deploy/setup/fix environment]"

## Your role
Handle all deployment, environment, and reproducibility concerns.

## Environment facts for this project
- OS: Windows 11
- Terminal: Git Bash (inside VSCode)
- Python: venv at ./venv/
- Activate: source venv/Scripts/activate
- DB: data/raw/portfolio.db (not committed to git — regenerated via python src/update_db.py)
- Deploy target: Streamlit Cloud (free tier)

## Common tasks

### Deploy to Streamlit Cloud
1. Ensure requirements.txt is complete: pip freeze > requirements.txt
2. Ensure app/app.py is the entry point
3. Ensure DB is regenerated at startup (app.py must call update_db if DB missing)
4. Go to share.streamlit.io → connect GitHub repo → set entry point: app/app.py
5. Add secrets if needed (none required for this project — all public data)

### Verify reproducibility
```bash
# Test: can a stranger run this?
git clone https://github.com/MCTGiang/vn-portfolio-optimizer.git test-clone
cd test-clone
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python src/update_db.py
streamlit run app/app.py
```

### requirements.txt validation
Check that these are included:
- pandas, numpy, matplotlib, plotly
- vnstock, vnstock3, yfinance
- scipy, scikit-learn
- streamlit
- jupyter (for development only — add to requirements-dev.txt)
