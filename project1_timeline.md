# Project 1 — VN Portfolio Optimizer
## Detailed Daily Timeline: 02/04/2025 → 26/05/2025

**Thesis:** Smart Portfolio Optimization & Auto-Rebalancing System  
**Student profile:** Python basic, Pandas/SQL basic, Jupyter, Git (beginner)  
**Available time:** Mon–Fri 1–1.5h/evening | Sat 3–4h | Sun 5–6h  
**Key changes vs original plan:** SQLite instead of PostgreSQL (Week 1), MPT theory before coding (Week 4–5), scope Week 5 = Minimum Variance only (not full Frontier), added video demo (Week 8)

---

## WEEK 1 — Setup & Git (02–06/04) | ~9h
**Goal:** GitHub repo live, SQLite schema created, comfortable with git basics

### Thu 02/04 (1.5h) ★ TODAY
- [Git] Install Git, create GitHub account, learn add → commit → push
- [Git] Create repo "vn-portfolio-optimizer", clone to local machine

### Fri 03/04 (1h)
- [Code] Create folder structure: data/raw, data/processed, notebooks/, src/, app/, reports/
- [Git] Create .gitignore (Python template), README.md → first commit to GitHub

### Sat 04/04 (3h)
- [Learn] Set up virtual environment, pip install: pandas numpy matplotlib jupyter vnstock
- [Learn] Read about SQLite: why use instead of PostgreSQL for Project 1 (20 min)
- [Code] Test import all libraries successfully in Jupyter

### Sun 05/04 (2h)
- [Code] Create portfolio.db using sqlite3 (Python built-in, no installation needed)
- [Code] Create table Stock_Prices: Ticker, Date, Open, High, Low, Close, Volume
- [Git] Commit: "feat: project structure + SQLite schema"

**Week 1 milestone:** Push 1 commit to GitHub, portfolio.db exists locally with empty table

---

## WEEK 2 — Data Collection / ETL Foundation (07–13/04) | ~17h
**Goal:** SQLite has 10 VN30 stocks, 3 years of data. load/insert functions reusable.

### Mon 07/04 (1h)
- [Learn] vnstock library 30 min: how to fetch OHLCV by ticker and date range
- [Data] Test fetch VCB data 2021–2024, inspect raw output

### Tue 08/04 (1h)
- [Data] Write script to fetch 10 VN30 tickers: VCB, VNM, HPG, FPT, MWG, VIC, GAS, BID, CTG, TCB
- [Code] Save to CSV temporarily before importing to DB

### Wed 09/04 (1h)
- [Code] Write insert_to_db(df, ticker): push DataFrame into SQLite Stock_Prices table
- [Code] Loop 10 tickers → insert all into database

### Thu 10/04 (1h)
- [Data] Validate data: row count per ticker, check missing dates, inspect null values
- [Code] Write load_from_db(ticker, start, end) → DataFrame

### Fri 11/04 (1h)
- [Review] Query SQLite directly, compare VCB price visually against CafeF

### Sat 12/04 (3h)
- [Code] Finalize src/data_loader.py: get_prices(), get_all_tickers() functions
- [Code] Write update_db.py script for future data updates
- [Git] Commit: "feat: ETL pipeline, 10 stocks in SQLite"

### Sun 13/04 (2h)
- [Review] Buffer: fix any remaining bugs, ensure load_from_db() is stable
- [Code] Quick plot VCB and VNM prices to visually validate data

**Week 2 milestone:** Query VCB price from DB, plot chart looks correct visually

---

## WEEK 3 — Data Processing & Returns Calculation (14–20/04) | ~17h
**Goal:** Clean returns_matrix, calculation functions verified against Excel.

### ⚠️ Theory to read before coding this week (30 min):
> Search "simple return vs log return finance python" — understand when to use each.
> In MPT: use simple return for portfolio, log return for statistical analysis.

### Mon 14/04 (1h)
- [Finance] READ: Simple Return vs Log Return — when to use which (30 min)
- [Code] Load data from SQLite into DataFrame, set index=Date, check dtypes

### Tue 15/04 (1h)
- [Code] Handle missing values: forward fill for non-trading days
- [Code] Check Adjusted Close — is vnstock data already adjusted?

### Wed 16/04 (1h)
- [Code] Write calc_returns(df): daily simple return = (P_t - P_{t-1}) / P_{t-1}
- [Code] Write calc_log_returns(df): log(P_t / P_{t-1})

### Thu 17/04 (1h)
- [Code] Build returns_matrix: DataFrame with 10 columns (tickers) × N rows (dates)
- [Review] Verify: manually calculate VCB return for a specific date, compare with Python

### Fri 18/04 (1h)
- [Code] Calculate Annualized Return (× 252) and Annualized Volatility (× sqrt(252))
- [Code] Export to Excel for cross-validation

### Sat 19/04 (3h)
- [Code] Finalize src/features.py: all return calculation functions in one module
- [Code] Plot return distribution per ticker — which stock is most volatile?
- [Git] Commit: "feat: returns calculation module, verified"

### Sun 20/04 (2h)
- [Review] Buffer: re-read code, add docstrings to all functions
- [Finance] Start reading basic MPT theory — prepare mindset for Week 4 (1h)

**Week 3 milestone:** Export CSV of returns for 10 tickers, manually verify 3 rows and confirm correct

---

## WEEK 4 — Portfolio Financial Metrics (21–27/04) | ~17h
**Goal:** portfolio_stats() function verified against Excel, can explain correlation heatmap.

### ⚠️ Theory to read/watch before coding this week (critical):
> Search "Markowitz Portfolio Theory Python" on YouTube, watch first 20 min.
> Must understand BEFORE coding:
> - Expected Return = mean of historical returns
> - Risk = Volatility = standard deviation
> - Covariance Matrix Σ: measures co-movement between stocks
> - Portfolio variance formula: w^T × Σ × w
> Without understanding this formula, you cannot explain results during thesis defense.

### Mon 21/04 (1h)
- [Finance] WATCH: Markowitz MPT tutorial 20 min — understand return and risk formulas
- [Code] Code Expected Return: mean(daily_returns) × 252 per ticker

### Tue 22/04 (1h)
- [Code] Code Volatility: std(daily_returns) × sqrt(252) per ticker
- [Review] Verify against Excel: pick 1 ticker, calculate manually then compare with Python

### Wed 23/04 (1h)
- [Finance] Understand Covariance Matrix: why co-movement matters for diversification
- [Code] Calculate Covariance Matrix: returns_matrix.cov() × 252 (annualized)

### Thu 24/04 (1h)
- [Code] Calculate Correlation Matrix: returns_matrix.corr() → visualize as heatmap
- [Review] Analyze heatmap: which tickers are highly correlated? What does it mean?

### Fri 25/04 (1h)
- [Code] Write portfolio_stats(weights, exp_returns, cov_matrix) → (return, risk, sharpe)
- [Review] Test with equal weights (10% each) — do the numbers make sense?

### Sat 26/04 (3h)
- [Code] Finalize src/portfolio_metrics.py, verify portfolio_stats() by hand calculation
- [Git] Commit: "feat: portfolio metrics module, covariance matrix"

### Sun 27/04 (2h)
- [Review] Large buffer: resolve all logic errors from the week
- [Finance] Read about Minimum Variance problem — formula and intuition (30 min)

**Week 4 milestone:** portfolio_stats() verified against Excel, can explain what the correlation heatmap shows

---

## WEEK 5 — Portfolio Optimizer / Minimum Variance (28/04–04/05) | ~17h
**Goal:** Call min_variance_portfolio(["VCB","VNM","HPG","FPT","MWG"]) and get sensible weights.

### ⚠️ Scope boundary for Project 1 (important):
> Only build: Minimum Variance Portfolio (1 point on Efficient Frontier).
> Do NOT attempt full Efficient Frontier in Project 1 — save for Project 2.
> Reason: scipy.optimize is complex enough to get right; adding Frontier risks
> edge case bugs with no time to debug before deadline.

### Mon 28/04 (1h)
- [Finance] READ: what are constraints and bounds in scipy.optimize.minimize (30 min)
- [Learn] Run simple example: minimize x^2 + y^2 with constraint x + y = 1

### Tue 29/04 (1h)
- [Code] Write objective function: portfolio_variance(weights, cov_matrix)
- [Code] Define constraints: sum(weights) = 1
- [Code] Define bounds: 0 ≤ weight_i ≤ 1 (long-only, no short selling)

### Wed 30/04 (1h)
- [Code] Run scipy.optimize.minimize → get optimal weights
- [Review] Validate: sum(weights) == 1? All weights ≥ 0? Numbers make sense?

### Thu 01/05 (1h)
- [Code] Calculate portfolio return and risk at Minimum Variance point
- [Review] Compare with equal weights: which is better and why?

### Fri 02/05 (1h)
- [Code] Finalize src/optimizer.py: min_variance_portfolio(tickers, start, end) → weights dict
- [Git] Commit: "feat: minimum variance portfolio optimizer"

### Sat 03/05 (3h)
- [Code] Standalone script: input ticker list → output formatted allocation table
- [Review] Test with 5–6 different ticker combinations, record results in comparison table
- [Code] Add Sharpe Ratio to output (if time allows)

### Sun 04/05 (2h)
- [Review] Buffer: handle edge cases — missing data tickers, weights not converging
- [Code] Ensure optimizer runs independently without notebook dependency

**Week 5 milestone:** min_variance_portfolio() returns sensible allocation weights, tested on multiple ticker combinations

---

## WEEK 6 — Streamlit Dashboard (05–11/05) | ~17h
**Goal:** Public Streamlit URL, anyone can use without instructions.

### Mon 05/05 (1h)
- [Learn] Streamlit basics: st.multiselect, st.plotly_chart, st.metric, st.columns (1h)
- [Code] Hello World dashboard: select tickers → display price history line chart

### Tue 06/05 (1h)
- [Code] Connect app.py to SQLite: load data → calculate returns → run optimizer
- [Code] Display allocation results as formatted table

### Wed 07/05 (1h)
- [Viz] Draw Pie chart of portfolio allocation using Plotly
- [Viz] Draw Correlation Heatmap for selected tickers

### Thu 08/05 (1h)
- [Code] Add Metric cards: Portfolio Return, Portfolio Volatility, Sharpe Ratio
- [Code] Side-by-side comparison: Optimized Weights vs Equal Weights

### Fri 09/05 (1h)
- [Review] UX test: select different ticker combinations — does dashboard respond correctly?
- [Code] Fix UI issues, improve layout

### Sat 10/05 (3h)
- [Code] Create requirements.txt with all dependencies
- [Code] Deploy to Streamlit Cloud: connect GitHub repo, configure app entry point
- [Review] Test public URL from mobile phone
- [Git] Commit: "feat: streamlit dashboard deployed, URL updated in README"

### Sun 11/05 (2h)
- [Review] Ask 1 person to open the link and use it without guidance — observe and note issues
- [Code] Buffer: fix UI bugs found during real user testing

**Week 6 milestone:** Send Streamlit link to a friend, they can use it without any explanation

---

## WEEK 7 — Buffer: Testing & Refactoring (12–18/05) | ~12h
**Goal:** Anyone can clone repo and run it without asking for help.

### Mon–Fri (12–16/05) (1h/evening)
- [Review] Each evening: fix remaining bugs, improve code quality incrementally

### Sat 17/05 (3h)
- [Review] Re-run entire pipeline from scratch in a fresh environment (no cache)
- [Code] Refactor: clear variable names, add docstrings, clean module separation
- [Git] Update README: complete setup and local run instructions

### Sun 18/05 (2h)
- [Review] Ask friend/mentor to clone repo and run on their machine — note any errors
- [Code] Fix reproducibility issues, ensure requirements.txt is complete

**Week 7 milestone:** Stranger clones repo and runs successfully without asking anything

---

## WEEK 8 — Report, Video Demo & Submission (19–26/05) | ~12h
**Goal:** Submit 4 items by 26/05: PDF report + GitHub link + Streamlit URL + video demo.

### Mon 19/05 (1h)
- [Write] Outline 5-chapter report: Introduction | Data | Methodology | Results | Conclusion
- [Write] Write Chapter 1: portfolio optimization problem in Vietnamese stock market

### Tue 20/05 (1h)
- [Write] Write Chapter 2: Data sources, 10 ticker descriptions, ETL pipeline summary
- [Write] Write Chapter 3: Methodology — explain MPT, Covariance Matrix, scipy.optimize

### Wed 21/05 (1h)
- [Write] Write Chapter 4: Results — allocation table, Optimized vs Equal Weights comparison
- [Write] Write Chapter 5: Conclusion & Future Work — Efficient Frontier (P2), Rebalancing (P2)

### Thu 22/05 (1h)
- [Review] Record video demo 2–3 min: open dashboard → select tickers → explain each number
- [Review] Watch video back — can you clearly explain "what is Covariance Matrix"?

### Fri 23/05 (1h)
- [Review] Re-read report as an examiner — note weak sections
- [Code] Final check: GitHub link, Streamlit URL, requirements.txt all working

### Sat 24/05 (3h)
- [Write] Export final PDF report
- [Review] Prepare answers to 3 defense questions:
  1. Why Minimum Variance Portfolio and not Maximum Sharpe?
  2. What does the Covariance Matrix tell us economically?
  3. What are the limitations of Markowitz MPT?

### Sun–Mon 26/05 (2h)
- [Git] DEADLINE: Submit PDF report + GitHub link + Streamlit URL + video demo
- [Write] Write retrospective note: lessons from P1, plan for P2 (Efficient Frontier + Rebalancing)

**Week 8 milestone:** All 4 deliverables submitted by 26/05/2025

---

## DELIVERABLES CHECKLIST (due 26/05/2025)

- [ ] GitHub repo: clear README, consistent weekly commits
- [ ] SQLite database: 10 VN30 tickers, 2021–2024 price history
- [ ] src/portfolio_metrics.py: Expected Return + Covariance Matrix, verified against Excel
- [ ] src/optimizer.py: Minimum Variance Portfolio, returns sensible weights
- [ ] app/app.py: Streamlit dashboard with pie chart allocation + metric cards, public URL
- [ ] Video demo: 2–3 min, explains what each output number means
- [ ] PDF report: 5–8 pages, explains formulas not just demo

---

## 3 DEFENSE QUESTIONS TO PREPARE

1. **Why Minimum Variance Portfolio?** → Lowest risk for given set of assets; good starting point before introducing return expectations
2. **What does the Covariance Matrix tell us?** → Measures how stocks move together; low covariance = better diversification; drives the w^T×Σ×w portfolio variance formula
3. **What are the limitations of MPT?** → Assumes normal return distribution, uses historical data as proxy for future, ignores transaction costs, sensitive to input estimation errors

---

## PROJECT ROADMAP CONTEXT

| Phase | Timeline | Key additions |
|-------|----------|---------------|
| **Project 1** | Apr–May 2025 | Minimum Variance Portfolio, SQLite, Streamlit |
| **Project 2** | Jun–Sep 2025 | Efficient Frontier, Auto-Rebalancing, NLP Sentiment, Multi-stock LSTM |
| **Thesis** | Oct 2025–Mar 2026 | Ensemble ML (LSTM+XGBoost+RF), VaR/CVaR Risk Management, Backtesting Engine |

**Final thesis title (proposed):**
"Vietnamese Stock Market Investment Support System Integrating Ensemble ML Price Forecasting, Portfolio Optimization and Risk Management"

---

*Generated: 02/04/2025 | For use with Claude Code or any AI coding assistant*
*Repo: https://github.com/MCTGiang/vn-portfolio-optimizer*
