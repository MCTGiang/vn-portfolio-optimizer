# Project 1 — VN Portfolio Optimizer
## Detailed Daily Timeline: 02/04/2026 → 26/05/2026

**Thesis:** Smart Portfolio Optimization & Auto-Rebalancing System
**Student profile:** Python basic, Pandas/SQL basic, Jupyter, Git (beginner)
**Available time:** Mon–Fri 1–1.5h/evening | Sat 3–4h | Sun 5–6h
**Key changes vs original plan:** SQLite instead of PostgreSQL (Week 1), MPT theory before coding (Week 4–5), scope Week 5 = Minimum Variance only (not full Frontier), added video demo (Week 8)
**Note:** All days including public holidays are working days.

---

## Current Status — updated 08/04/2026

### Completed (Week 1 FULL ✅ + Week 2 ETL/Validation FULL ✅ + features.py written ✅)
- [x] Install Git, create GitHub account, learn add → commit → push ✅ 2026-04-02
- [x] Create repo "vn-portfolio-optimizer" (Public), clone to local machine ✅ 2026-04-02
- [x] Create folder structure: data/raw, data/processed, notebooks/, src/, app/, reports/ ✅ 2026-04-02
- [x] Create .gitignore (Python template) and README.md → first commit to GitHub ✅ 2026-04-02
- [x] Set up virtual environment (venv), install all dependencies ✅ 2026-04-03
- [x] Generate requirements.txt inside venv ✅ 2026-04-03
- [x] Test import all libraries successfully in Jupyter (00_environment_check.ipynb) ✅ 2026-04-03
- [x] Resolve vnstock3 403 error → bypassed with VCIQuote direct import ✅ 2026-04-03
- [x] Create portfolio.db using sqlite3 (Python built-in) ✅ 2026-04-03
- [x] Create table Stock_Prices: Ticker, Date, Open, High, Low, Close, Volume ✅ 2026-04-03
- [x] Write src/data_loader.py: fetch_ticker_vci(), fetch_ticker_yfinance(), fetch_ticker(), insert_to_db(), load_from_db(), get_all_tickers(), get_db_summary(), update_db() ✅ 2026-04-03
- [x] Run full ETL pipeline: 30 VN30 tickers, 2021–2026, 39,189 rows in SQLite ✅ 2026-04-03
- [x] Update README with setup instruction: python src/data_loader.py ✅ 2026-04-03
- [x] Validate all 30 tickers: row counts, missing dates, null values ✅ 2026-04-04
- [x] Verify VCB closing price against market data (CafeF) for 03/04/2026 ✅ 2026-04-04
- [x] Plot VCB and VNM price history → reports/vcb_vnm_price_history.png ✅ 2026-04-04
- [x] Write src/update_db.py as standalone CLI (--tickers, --start, --replace) ✅ 2026-04-04
- [x] Set up CLAUDE.md + prompts/daily_log.md + logs/ workflow ✅ 2026-04-05
- [x] Write src/features.py: calc_returns(), calc_log_returns(), build_returns_matrix(), calc_annualized_return(), calc_annualized_volatility(), ticker_summary() ✅ 2026-04-08

### Next: Finish Week 2 by Sun 12/04
- [ ] Test features.py end-to-end: load_from_db('VCB') → calc_returns() → verify one value vs Excel
- [ ] Plot return distribution per ticker — identify most volatile stock
- [ ] Commit: "feat: returns calculation module, verified against Excel"
- [ ] Read MPT basics before Week 3 starts Mon 13/04

---

## WEEK 1 — Setup & Git (02–03/04) FULLY COMPLETED

### Thu 02/04 DONE
- ~~[Git] Install Git, create GitHub account, learn add → commit → push~~
- ~~[Git] Create repo "vn-portfolio-optimizer", clone to local machine~~

### Fri 03/04 DONE
- ~~[Code] Create folder structure, .gitignore, README.md, requirements.txt~~
- ~~[Code] Set up venv, install all dependencies, test imports in Jupyter~~
- ~~[Code] Resolve vnstock3 → yfinance, write src/data_loader.py~~
- ~~[Code] Create portfolio.db + Stock_Prices table~~
- ~~[Code] Run ETL: 10 tickers, ~12,000 rows inserted into SQLite~~
- ~~[Git] Commit and push all changes~~

**Week 1 milestone:** DONE — GitHub repo live, ETL pipeline complete, 10 tickers in DB

---

## WEEK 2 — Data Validation & Returns Calculation (04–12/04) | ~20h
**Goal:** Verified returns_matrix, src/features.py complete and committed.

> Week 2 starts Sat 04/04 (early) because ETL completed ahead of schedule.
> Scope expanded: absorbs remaining ETL validation + full returns module.

### Theory to read before coding this week (30 min):
> Search "simple return vs log return finance python"
> In MPT: use simple return for portfolio, log return for statistical analysis.

### Sat 04/04 (3h) ✅ DONE 2026-04-04
- ~~[Data] Validate ETL output: row counts per ticker, check missing dates, inspect nulls~~ ✅
- ~~[Data] Query SQLite directly, compare VCB closing price against CafeF~~ ✅ 57,700 VND matches
- ~~[Code] Plot VCB and VNM price history to visually confirm data looks correct~~ ✅ reports/vcb_vnm_price_history.png
- ~~[Code] Write src/update_db.py as standalone CLI (argparse: --tickers, --start, --replace)~~ ✅
- ~~[Git] Commit: "feat: ETL pipeline, 30 VN30 stocks in SQLite, VCI source, update_db script"~~ ✅

### Sun 05/04 (2h actual) — Tooling setup instead of features.py
- ~~[Setup] CLAUDE.md, prompts/daily_log.md, logs/ workflow established~~ ✅ 2026-04-05
- [ ] [Finance] READ: Simple Return vs Log Return — MOVED TO Mon 06/04
- [ ] [Code] Load SQLite data, calc_returns(), calc_log_returns() — MOVED TO Mon 06/04+

### Mon 06/04 — MISSED ❌
- (Personal commitments — no session; tasks pushed to Wed 08/04)

### Tue 07/04 — MISSED ❌
- (Personal commitments — no session; 2nd consecutive missed day)

### Wed 08/04 (1h)
- ~~[Code] src/features.py written: all 5 functions + ticker_summary()~~ ✅ 2026-04-08

### Thu 09/04 (1h) ✅ DONE 2026-04-09
- ~~[Code] Refine src/features.py: rename functions, add TRADING_DAYS, method param, __main__ block~~ ✅
- ~~[Git] Commit: "feat: implement features.py — returns, annualized stats, returns matrix"~~ ✅

### Fri 10/04 (1h) — carry-over from 08/04
- [Review] Spot-check: verify VCB annualized return for 2024 vs Excel (~20m) ← 08/04 carry-over
- [Code] Plot return distribution histogram per ticker — identify most volatile stock (~30m) ← 08/04 carry-over

### Sat 11/04 (3h) — 🟢 [BUFFER]
- ~~[Code] Write update_db.py as standalone runnable script~~ ✅ Done early 2026-04-04
- [Review] Run full pipeline: load_from_db() → calc_returns() → build_returns_matrix() end-to-end
- [Finance] Read MPT: Expected Return = mean × 252, Variance, intuition behind Covariance
- [Buffer] Fix any issues, add missing docstrings, clean notebooks

### Sun 12/04 (5h)
- [Finance] Continue MPT theory: Covariance Matrix, portfolio variance formula w^T × S × w
- [Review] Re-run full pipeline from scratch — confirm no errors
- [Buffer] Extra time: any remaining fixes or prep for Week 3

**Week 2 milestone:** returns_matrix verified against Excel, src/features.py complete and committed

---

## WEEK 3 — Portfolio Financial Metrics (13–19/04) | ~17h
**Goal:** portfolio_stats() verified against Excel, correlation heatmap explainable.

### Theory to watch before coding this week (critical):
> Search "Markowitz Portfolio Theory Python" on YouTube, watch first 20 min.
> Must understand BEFORE coding:
> - Expected Return = mean of historical returns
> - Risk = Volatility = standard deviation
> - Covariance Matrix: measures co-movement between stocks
> - Portfolio variance formula: w^T x S x w
> Without understanding this formula, you cannot explain results during thesis defense.

### Mon 13/04 (1h)
- [Finance] WATCH: Markowitz MPT tutorial 20 min
- [Code] Code Expected Return per ticker: mean(daily_returns) x 252

### Tue 14/04 (1h)
- [Code] Code Volatility per ticker: std(daily_returns) x sqrt(252)
- [Review] Verify against Excel: pick 1 ticker, calculate manually vs Python

### Wed 15/04 (1h)
- [Finance] Understand Covariance Matrix: why co-movement matters for diversification
- [Code] Calculate Covariance Matrix: returns_matrix.cov() x 252 (annualized)

### Thu 16/04 (1h)
- [Code] Calculate Correlation Matrix: returns_matrix.corr() → visualize as heatmap
- [Review] Analyze heatmap: which tickers are highly correlated?

### Fri 17/04 (1h)
- [Code] Write portfolio_stats(weights, exp_returns, cov_matrix) → (return, risk, sharpe)
- [Review] Test with equal weights (10% each) — do numbers make sense?

### Sat 18/04 (3h)
- [Code] Finalize src/portfolio_metrics.py: all functions clean with docstrings
- [Review] Verify portfolio_stats() by hand calculation for 2-stock simple case
- [Code] Add helper: display_metrics(tickers, weights) → formatted summary table
- [Git] Commit: "feat: portfolio metrics module, covariance matrix"

### Sun 19/04 (5h)
- [Review] Large buffer: resolve all logic errors from the week
- [Finance] Read about Minimum Variance problem — formula and intuition (30 min)
- [Review] Final check: can you explain each number in portfolio_stats() output verbally?
- [Buffer] Improve heatmap visualization, add color formatting

**Week 3 milestone:** portfolio_stats() verified against Excel, can explain the correlation heatmap

---

## WEEK 4 — Portfolio Optimizer / Minimum Variance (20–26/04) | ~17h
**Goal:** min_variance_portfolio() returns sensible weights, tested on multiple ticker sets.

### Scope boundary for Project 1 (important):
> Only build: Minimum Variance Portfolio (1 point on Efficient Frontier).
> Do NOT attempt full Efficient Frontier in Project 1 — save for Project 2.

### Mon 20/04 (1h)
- [Finance] READ: constraints and bounds in scipy.optimize.minimize (30 min)
- [Learn] Run simple example: minimize x^2 + y^2 with constraint x + y = 1

### Tue 21/04 (1h)
- [Code] Write objective function: portfolio_variance(weights, cov_matrix)
- [Code] Define constraints: sum(weights) = 1

### Wed 22/04 (1h)
- [Code] Define bounds: 0 <= weight_i <= 1 (long-only, no short selling)
- [Code] Run scipy.optimize.minimize → get optimal weights

### Thu 23/04 (1h)
- [Review] Validate: sum(weights) == 1? All weights >= 0? Numbers make sense?
- [Code] Calculate portfolio return and risk at Minimum Variance point

### Fri 24/04 (1h)
- [Review] Compare Minimum Variance vs Equal Weights: which has lower risk and why?
- [Code] Finalize src/optimizer.py: min_variance_portfolio(tickers, start, end) → weights dict

### Sat 25/04 (3h)
- [Code] Standalone script: input ticker list → output formatted allocation table
- [Review] Test with 5–6 different ticker combinations, record results in comparison table
- [Code] Add Sharpe Ratio to output
- [Git] Commit: "feat: minimum variance portfolio optimizer"

### Sun 26/04 (5h)
- [Review] Buffer: handle edge cases — missing data tickers, weights not converging
- [Code] Ensure optimizer runs independently without notebook dependency
- [Review] Final check: can you explain why each ticker got its allocation weight?
- [Buffer] Add Max Sharpe Portfolio as optional second output if time allows

**Week 4 milestone:** min_variance_portfolio() returns sensible weights, tested on multiple combos

---

## WEEK 5 — Streamlit Dashboard (27/04–03/05) | ~17h
**Goal:** Public Streamlit URL, anyone can use without instructions.

### Sun 27/04 (5h)
- [Learn] Streamlit basics: st.multiselect, st.plotly_chart, st.metric, st.columns (1h)
- [Code] Hello World dashboard: select tickers → display price history line chart
- [Code] Connect app.py to SQLite: load data → returns → optimizer pipeline
- [Code] Display allocation results as formatted table

### Mon 28/04 (1h)
- [Viz] Draw Pie chart of portfolio allocation using Plotly

### Tue 29/04 (1h)
- [Viz] Draw Correlation Heatmap for selected tickers

### Wed 30/04 (1h) — Liberation Day, work from home
- [Code] Add Metric cards: Portfolio Return, Portfolio Volatility, Sharpe Ratio
- [Code] Side-by-side comparison: Optimized Weights vs Equal Weights

### Thu 01/05 (1h) — Labour Day, work from home
- [Review] UX test: select different ticker combos — does dashboard respond correctly?
- [Code] Fix UI issues, improve layout

### Fri 02/05 (1h)
- [Code] Update requirements.txt with all dependencies
- [Code] Deploy to Streamlit Cloud: connect GitHub repo, configure entry point

### Sat 03/05 (3h)
- [Review] Test public URL from mobile phone
- [Review] Ask 1 person to use the app without guidance — observe and note issues
- [Code] Fix UI bugs from user testing
- [Git] Commit: "feat: streamlit dashboard deployed, URL updated in README"

**Week 5 milestone:** Send Streamlit link to a friend, they use it without any explanation

---

## WEEK 6 — Buffer: Testing & Refactoring (04–10/05) | ~17h
**Goal:** Anyone can clone repo and run it without asking for help.

### Sun 04/05 (5h)
- [Code] Final dashboard polish: fix remaining bugs
- [Review] Re-run full pipeline in fresh environment (no cache)
- [Code] Refactor src/data_loader.py: clear names, complete docstrings

### Mon 05/05 (1h)
- [Code] Refactor src/features.py

### Tue 06/05 (1h)
- [Code] Refactor src/portfolio_metrics.py

### Wed 07/05 (1h)
- [Code] Refactor src/optimizer.py
- [Git] Commit: "refactor: clean all src modules, add docstrings"

### Thu 08/05 (1h)
- [Git] Update README: complete setup instructions, add screenshots
- [Review] Verify all modules importable, pipeline runs end-to-end

### Fri 09/05 (1h)
- [Review] Ask friend/mentor to clone repo and run — note any errors
- [Code] Fix reproducibility issues

### Sat 10/05 (3h)
- [Code] Fix all bugs from external testing
- [Review] Final test: clone → pip install → python src/data_loader.py → streamlit run app/app.py
- [Git] Commit: "chore: fix reproducibility issues, update requirements.txt"

**Week 6 milestone:** Stranger clones repo and runs successfully without asking anything

---

## WEEK 7 — Report Writing (11–17/05) | ~17h
**Goal:** Complete 5-chapter PDF report and video demo.

### Sun 11/05 (5h)
- [Write] Outline report: Introduction | Data | Methodology | Results | Conclusion
- [Write] Write Chapter 1: portfolio optimization problem in Vietnamese stock market
- [Write] Write Chapter 2: Data sources, 10 tickers, ETL pipeline summary

### Mon 12/05 (1h)
- [Write] Write Chapter 3: MPT theory, Covariance Matrix, scipy.optimize

### Tue 13/05 (1h)
- [Write] Write Chapter 4: Results — allocation table, Optimized vs Equal Weights

### Wed 14/05 (1h)
- [Write] Write Chapter 5: Conclusion & Future Work (Efficient Frontier P2, Rebalancing P2)

### Thu 15/05 (1h)
- [Review] Re-read full report as examiner — note and fix weak sections

### Fri 16/05 (1h)
- [Review] Record video demo 2–3 min: open dashboard → select tickers → explain each number
- [Review] Watch video back — can you explain "what is Covariance Matrix" clearly?

### Sat 17/05 (3h)
- [Write] Final polish on report language and formatting
- [Write] Export PDF report v1
- [Review] Prepare answers to 3 defense questions:
  1. Why Minimum Variance Portfolio and not Maximum Sharpe?
  2. What does the Covariance Matrix tell us economically?
  3. What are the limitations of Markowitz MPT?

**Week 7 milestone:** PDF report v1 complete, video demo recorded, defense questions prepared

---

## WEEK 8 — Final Polish & Submission (18–26/05) | ~14h
**Goal:** Submit 4 items by 26/05: PDF report + GitHub link + Streamlit URL + video demo.

### Sun 18/05 (5h)
- [Review] Buffer: re-read report, fix remaining issues
- [Code] Final check: GitHub, Streamlit URL, requirements.txt all working
- [Git] Clean commit history, README presentation-ready

### Mon 19/05 (1h)
- [Review] Re-watch video demo — clear and confident?
- [Write] Re-record if needed

### Tue 20/05 (1h)
- [Review] Final end-to-end check

### Wed 21/05 (1h)
- [Review] Ask 1 person to watch demo and give feedback
- [Write] Incorporate feedback

### Thu 22/05 (1h)
- [Write] Export absolute final PDF report
- [Git] Final commit: "docs: final report and README, ready for submission"

### Fri 23/05 (1h)
- [Review] Buffer: fix any last-minute issues

### Sat 24/05 (3h)
- [Review] Full dry run: present project as if in defense (target: 10 min)
- [Write] Write retrospective: lessons from P1, plan for P2

### Mon–Tue 25–26/05 (1h)
- [Git] DEADLINE: Submit PDF + GitHub link + Streamlit URL + video demo

**Week 8 milestone:** All 4 deliverables submitted by 26/05/2026

---

## DELIVERABLES CHECKLIST (due 26/05/2026)

- [ ] GitHub repo: clear README, consistent weekly commits
- [x] SQLite database: 30 VN30 tickers, 2021–2026 (39,189 rows) ✅ 2026-04-03
- [x] src/data_loader.py: ETL pipeline VCI primary / yfinance fallback, fully functional ✅ 2026-04-03
- [x] src/update_db.py: standalone CLI with argparse ✅ 2026-04-04
- [ ] src/features.py: returns, volatility, annualized metrics, verified vs Excel
- [ ] src/portfolio_metrics.py: Expected Return + Covariance Matrix, verified vs Excel
- [ ] src/optimizer.py: Minimum Variance Portfolio, sensible weights
- [ ] app/app.py: Streamlit dashboard with pie chart + metric cards, public URL
- [ ] Video demo: 2–3 min, explains each output number
- [ ] PDF report: 5–8 pages, explains formulas not just demo

---

## 3 DEFENSE QUESTIONS TO PREPARE

1. **Why Minimum Variance Portfolio?** → Lowest risk for given assets; good starting point before introducing return expectations
2. **What does the Covariance Matrix tell us?** → Measures how stocks move together; low covariance = better diversification; drives the w^T x S x w portfolio variance formula
3. **What are the limitations of MPT?** → Assumes normal distribution, uses historical data as future proxy, ignores transaction costs, sensitive to estimation errors

---

## ACTUAL PROGRESS LOG

| Date | Completed | Commit message |
|------|-----------|----------------|
| 02/04 | Git setup, GitHub account, repo created and cloned, folder structure, .gitignore, README, fixed push rejection | feat: initial project structure and README |
| 03/04 | venv, all deps, requirements.txt, 00_environment_check.ipynb, data_loader.py (VCI+yfinance), portfolio.db, ETL 30 tickers 39,189 rows, README updated | feat: ETL pipeline complete → feat: VCI source 30 VN30 tickers |
| 04/04 | Validated 30 tickers (row counts, nulls, price check vs CafeF ✅), update_db.py CLI, vcb_vnm_price_history.png | feat: ETL pipeline, 30 VN30 stocks in SQLite, VCI source, update_db script |
| 05/04 | CLAUDE.md, prompts/daily_log.md, logs/ directory, Claude Code workflow setup | chore: add daily log prompt and logs directory |
| 06/04 | MISSED — personal commitments | — |
| 07/04 | MISSED — personal commitments (2nd consecutive day) | — |
| 08/04 | SQLite/data_loader/update_db deep review; MPT theory (simple vs log return, ×252/×√252); data quality checks ✅; features.py: 7 functions, LPB 47.25% / SAB -7.37% | feat: implement features.py — returns, annualized stats, returns matrix for 30 VN30 tickers |

---

## PROJECT ROADMAP CONTEXT

| Phase | Timeline | Key additions |
|-------|----------|---------------|
| Project 1 | Apr–May 2026 | Minimum Variance Portfolio, SQLite, Streamlit |
| Project 2 | Jun–Sep 2026 | Efficient Frontier, Auto-Rebalancing, NLP Sentiment, LSTM |
| Thesis | Oct 2026–Mar 2027 | Ensemble ML (LSTM+XGBoost+RF), VaR/CVaR, Backtesting |

**Final thesis title (proposed):**
"Vietnamese Stock Market Investment Support System Integrating Ensemble ML Price Forecasting, Portfolio Optimization and Risk Management"

---

*Updated: 09/04/2026 (GMT+7) | For use with Claude Code or any AI coding assistant*
*Repo: https://github.com/MCTGiang/vn-portfolio-optimizer*
