# Project 1 — VN Portfolio Optimizer
## Detailed Daily Timeline: 02/04/2026 → 26/05/2026

**Thesis:** Smart Portfolio Optimization & Auto-Rebalancing System
**Student profile:** Python basic, Pandas/SQL basic, Jupyter, Git (beginner)
**Available time:** Mon–Fri 1–1.5h/evening | Sat 3–4h | Sun 5–6h
**Key changes vs original plan:** SQLite instead of PostgreSQL (Week 1), MPT theory before coding (Week 4–5), scope Week 5 = Minimum Variance only (not full Frontier), added video demo (Week 8)
**Note:** All days including public holidays are working days.

---

## Current Status — updated 20/04/2026

### Completed (Week 1 ✅ + Week 2 ✅ + Week 3 ✅ + Week 4 ✅ + Week 5 partial — ~2 weeks ahead)
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
- [x] Write src/features.py: calc_returns(), calc_log_returns(), build_returns_matrix(), annualized_return(), annualized_volatility(), ticker_stats(), all_ticker_stats() ✅ 2026-04-08
- [x] Read MPT papers: Markowitz 1952, Elton/Gruber, Palomar — MVP rationale, SLSQP convex proof ✅ 2026-04-10
- [x] Spot-check VCB annualized return vs Excel: 8.90% / 25.61% ✅ 2026-04-13
- [x] Plot return distribution histograms for all 30 tickers (fat tails noted) ✅ 2026-04-13
- [x] Write src/portfolio_metrics.py: expected_returns(), covariance_matrix(), correlation_matrix(), portfolio_stats(), display_metrics() ✅ 2026-04-13
- [x] Verify portfolio_stats() by hand — VCB+VNM+KDC: 5.29% / 16.50% / Sharpe 0.048 ✅ 2026-04-13
- [x] Equal-weights 30-ticker baseline: 18.98% / 20.67% / Sharpe 0.701 ✅ 2026-04-13
- [x] Write src/optimizer.py: portfolio_variance(), min_variance_portfolio(), display_portfolio(), CLI ✅ 2026-04-20
- [x] Verify: sum(weights)==1, all ≥ 0, Vol < 20.67% — 30-ticker: 33.9% reduction ✅ 2026-04-20
- [x] Test optimizer on 5 ticker combos + edge cases (high-corr, high-vol, invalid ticker) ✅ 2026-04-20
- [x] Build app/app.py: full Streamlit dashboard with metrics, donut, bar, heatmap, VI/EN toggle ✅ 2026-04-20

### Next: Deploy Streamlit dashboard (Tue 21/04)
- [ ] Commit app/app.py to GitHub
- [ ] Deploy to Streamlit Cloud — connect GitHub repo, set entry point app/app.py
- [ ] Verify public URL works end-to-end; test on mobile

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
- ~~[Review] Spot-check: verify VCB annualized return for 2024 vs Excel~~ ✅ 2026-04-13 (done in Mon session)
- ~~[Code] Plot return distribution histogram per ticker~~ ✅ 2026-04-13

### Sat 11/04 — 🟢 [BUFFER — skipped, not needed]
- ~~[Code] Write update_db.py as standalone runnable script~~ ✅ Done early 2026-04-04
- (Remaining tasks absorbed into Mon 13/04 extended session)

### Sun 12/04 — 🟢 [BUFFER — skipped, not needed]
- (All Week 2 + Week 3 content completed Mon 13/04)

**Week 2 milestone:** ✅ DONE — returns_matrix verified vs Excel, src/features.py committed

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

### Mon 13/04 (5h extended) ✅ DONE — ENTIRE WEEK 3 COMPLETED
- ~~[Finance] Read MPT theory: Var, Cov, Corr, Covariance Matrix concepts~~ ✅
- ~~[Code] Update portfolio.db to 10/04~~ ✅
- ~~[Review] Spot-check VCB annualized return vs Excel (carry-over)~~ ✅ 8.90% / 25.61% match
- ~~[Code] Plot return distribution histograms 30 tickers (carry-over)~~ ✅ fat tails noted
- ~~[Code] Calculate Covariance Matrix (30×30, annualized)~~ ✅ variance 0.0324–0.1828
- ~~[Code] Calculate Correlation Matrix + heatmap~~ ✅ banks cluster 0.5–0.7, KDC low-corr
- ~~[Code] Implement src/portfolio_metrics.py: expected_returns, covariance_matrix, correlation_matrix, portfolio_stats, display_metrics~~ ✅
- ~~[Review] Verify portfolio_stats() by hand — VCB+VNM+KDC: 5.29% / 16.50% / 0.048~~ ✅
- ~~[Code] Compute equal-weights 30-ticker baseline: 18.98% / 20.67% / 0.701~~ ✅
- ~~[Git] Commit: "feat: implement portfolio_metrics.py — covariance matrix, portfolio_stats, Sharpe ratio, verified"~~ ✅

### Tue 14/04 (1h) — 🟢 [BUFFER / early Week 4]
- [Finance] READ: scipy.optimize.minimize — constraints, bounds, SLSQP method (30m)
- [Code] Start src/optimizer.py: write portfolio_variance() objective function

### Wed 15/04 (1h) — early Week 4
- [Code] Define constraints: sum(weights) = 1
- [Code] Define bounds: 0 ≤ weight_i ≤ 1 (long-only)

### Thu 16/04 (1h) — early Week 4
- [Code] Run scipy.optimize.minimize → get optimal weights vector
- [Review] Sanity check: sum(weights)==1? All weights ≥ 0?

### Fri 17/04 (1h) — early Week 4
- [Code] Calculate portfolio return and risk at Minimum Variance point
- [Review] Compare Min Variance vs Equal Weights — confirm lower volatility

### Sat 18/04 (3h) — Week 4 core
- [Code] Finalize src/optimizer.py: min_variance_portfolio(tickers, start, end) → weights dict
- [Review] Test with 5–6 different ticker combinations, record results
- [Code] Add Sharpe Ratio to optimizer output
- [Git] Commit: "feat: minimum variance portfolio optimizer"

### Sun 19/04 (5h) — Week 4 buffer
- [Review] Handle edge cases: missing data tickers, weights not converging
- [Review] Final check: can you explain why each ticker got its allocation weight?
- [Finance] Read about Efficient Frontier (optional prep for P2)
- [Buffer] Any remaining Week 4 fixes

**Week 3 milestone:** ✅ DONE — portfolio_stats() verified vs Excel, correlation heatmap analyzed

---

## WEEK 4 — Portfolio Optimizer / Minimum Variance (14–19/04 early + 20–26/04) | ~17h
**Goal:** min_variance_portfolio() returns sensible weights, tested on multiple ticker sets.
> ⚠️ Started early (Tue 14/04) — Week 3 completed fully on Mon 13/04

### Scope boundary for Project 1 (important):
> Only build: Minimum Variance Portfolio (1 point on Efficient Frontier).
> Do NOT attempt full Efficient Frontier in Project 1 — save for Project 2.

### Tue 14/04 (1h) — 🟢 early start
- [Finance] READ: scipy.optimize.minimize — constraints, bounds, SLSQP method (30m)
- [Code] Start src/optimizer.py: write portfolio_variance() objective function

### Wed 15/04 (1h)
- [Code] Define constraints: sum(weights) = 1
- [Code] Define bounds: 0 ≤ weight_i ≤ 1 (long-only, no short selling)

### Thu 16/04 (1h)
- [Code] Run scipy.optimize.minimize → get optimal weights vector
- [Review] Sanity check: sum(weights)==1? All weights ≥ 0?

### Fri 17/04 (1h)
- [Code] Calculate portfolio return and risk at Minimum Variance point
- [Review] Compare Min Variance vs Equal Weights — confirm lower volatility than 20.67%

### Sat 18/04 (3h)
- [Code] Finalize src/optimizer.py: min_variance_portfolio(tickers, start, end) → weights dict
- [Review] Test with 5–6 different ticker combinations, record results in comparison table
- [Code] Add Sharpe Ratio to optimizer output
- [Git] Commit: "feat: minimum variance portfolio optimizer"

### Sun 19/04 (5h)
- [Review] Buffer: handle edge cases — missing data tickers, weights not converging
- [Code] Ensure optimizer runs independently without notebook dependency
- [Review] Final check: can you explain why each ticker got its allocation weight?
- [Buffer] Add Max Sharpe Portfolio as optional second output if time allows

### Mon 20/04 ✅ DONE 2026-04-20 — extended session (~7h)
- ~~[Finance] Learned w^T×Σ×w formula, diversification visualization~~ ✅
- ~~[Finance] Learned scipy.optimize.minimize: constraints, bounds, SLSQP, OptimizeResult~~ ✅
- ~~[Code] src/optimizer.py: portfolio_variance(), min_variance_portfolio(), display_portfolio(), CLI~~ ✅
- ~~[Review] Tested 5 combos — 30 VN30 tickers: Vol 33.9% below equal-weights baseline~~ ✅
- ~~[Review] Edge cases: 2 high-corr tickers, PDR/HVN high-vol, invalid ticker → ValueError~~ ✅
- ~~[Git] Commit: "feat: minimum variance portfolio optimizer, tested on 5 ticker combos"~~ ✅
- ~~[Code] app/app.py: full Streamlit dashboard — metrics, donut, bar chart, heatmap, alloc table~~ ✅
- ~~[UI] Language toggle VI/EN, donut labels, heatmap auto-font, bar chart colors~~ ✅

### Tue 21/04 ✅ DONE 2026-04-21 — extended session (~5-6h)
- ~~[Code] app/app.py full UI redesign: green palette, Inter font, HTML KPI cards, PDF/Excel export~~ ✅
- ~~[Code] Sidebar Update data button + auto `st.cache_data.clear()` + `st.rerun()`~~ ✅
- ~~[Deploy] Streamlit Cloud: mctgiangproject1.streamlit.app — connected, live~~ ✅
- ~~[Fix] `_db_is_ready()`: file check + COUNT>1000 guard before all sidebar components~~ ✅
- ~~[Fix] Auto-reinit DB on cloud container restart in optimizer except block~~ ✅
- ~~[Fix] Synced start date 2021-01-01 cloud ↔ local~~ ✅
- ~~[Data] VN30 updated Q1/2026: VPL in, BCM out; 10 new tickers fetched~~ ✅
- ~~[Code] portfolio_metrics.py: hardcoded end date → get_db_summary()['end_date'].max()~~ ✅
- ~~[Docs] README: Streamlit URL + badge added~~ ✅
- ~~[Report] Chapter 2.3 Class Diagram, 2.4 Class Detail, Lời Nói Đầu, Chi Tiết Công Việc~~ ✅

### Wed 22/04 (1h) — 🔴 verify + user test
- [Review] Test public URL from mobile phone
- [Review] Ask 1 person to use app without guidance — note issues

### Thu 23/04 (1h) — 🟢 [BUFFER / report]
- [Report] Continue Chapter 3: MPT theory, SLSQP explanation
- [Code] Fix any UI bugs from user testing (Wed)

### Fri 24/04 – Sun 26/04 — 🟢 [BUFFER]
- (Buffer: Week 6 refactor early start or report Chapter 3 continuation)

**Week 4 milestone:** ✅ DONE — min_variance_portfolio() tested on 5 combos, Vol 33.9% below baseline

---

## WEEK 5 — Streamlit Dashboard (20/04 early + 21/04 complete) | ~17h
**Goal:** Public Streamlit URL, anyone can use without instructions.
> ✅ Dashboard built 20/04, deployed + full redesign 21/04 — 12 days ahead of 03/05 target

### ~~Sun 27/04 (5h)~~ DONE EARLY 2026-04-20
- ~~[Learn] Streamlit basics: st.multiselect, st.plotly_chart, st.metric, st.columns~~ ✅
- ~~[Code] Hello World → connect pipeline → display allocation table~~ ✅
- ~~[Viz] Donut chart, bar chart MVP vs EW, correlation heatmap, metric cards~~ ✅
- ~~[Code] Language toggle VI/EN, @st.cache_data, compact CSS~~ ✅

### ~~Mon 28/04~~ DONE EARLY 2026-04-20/21
- ~~[Viz] Donut chart of portfolio allocation~~ ✅

### ~~Tue 29/04~~ DONE EARLY 2026-04-21
- ~~[Viz] Correlation Heatmap for selected tickers~~ ✅

### ~~Wed 30/04~~ DONE EARLY 2026-04-21 — Liberation Day
- ~~[Code] Metric cards: Return, Volatility, Sharpe, Active Positions~~ ✅
- ~~[Code] Side-by-side MVP vs Equal Weights comparison~~ ✅

### ~~Fri 02/05~~ DONE EARLY 2026-04-21
- ~~[Code] requirements.txt finalized with pinned versions~~ ✅
- ~~[Deploy] mctgiangproject1.streamlit.app live~~ ✅

### Thu 01/05 (1h) — Labour Day — 🟢 [BUFFER]
- (Mobile test + friend test done Wed 22/04 — this day is buffer)

### Sat 03/05 (3h) — 🟢 [BUFFER → report writing]
- [Report] Chapter 3 draft: MPT theory, covariance matrix, SLSQP explanation
- [Review] Any remaining UI polish if needed

**Week 5 milestone:** ✅ DONE — mctgiangproject1.streamlit.app live; mobile + friend test pending Wed 22/04

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
- [x] src/features.py: returns, volatility, annualized metrics, verified vs Excel ✅ 2026-04-13
- [x] src/portfolio_metrics.py: Expected Return + Covariance Matrix, verified vs Excel ✅ 2026-04-13
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
| 10/04 | MPT theory: Markowitz 1952, Elton/Gruber, Palomar — why MVP (no return estimation), SLSQP convex proof, fat tails as P1 limitation | — |
| 11/04 | OFF — personal commitments (was buffer day in plan) | — |
| 12/04 | OFF — personal commitments (was buffer day in plan) | — |
| 13/04 | DB updated to 10/04; VCB spot-check ✅ 8.90%/25.61%; 30-ticker histograms (fat tails noted); Cov/Corr matrices; portfolio_metrics.py: 5 functions verified (VCB+VNM+KDC 5.29%/16.50%/0.048); baseline 18.98%/20.67%/0.701 | feat: implement portfolio_metrics.py — covariance matrix, portfolio_stats, Sharpe ratio, verified |
| 20/04 | MVP theory + scipy SLSQP learned; optimizer.py: portfolio_variance(), min_variance_portfolio(), display_portfolio(), CLI (239 lines); 5 combo tests, 33.9% Vol reduction on 30 tickers; edge cases verified; app/app.py: full Streamlit dashboard with metrics, donut, bar, heatmap, VI/EN toggle (uncommitted) | feat: minimum variance portfolio optimizer, tested on 5 ticker combos |
| 21/04 | app/app.py full redesign: green palette #146026, Inter font, HTML KPI cards, PDF/Excel export (3-sheet), Update data button; deployed mctgiangproject1.streamlit.app; 4 cloud DB fixes (_db_is_ready, auto-reinit); VN30 Q1/2026 update (VPL in, BCM out); portfolio_metrics end date from DB; report Ch2.3–2.4 drafted | feat: streamlit dashboard complete + 10 fix commits |

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
