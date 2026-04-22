# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Vietnamese stock market portfolio optimization system built with Modern Portfolio Theory (Markowitz), targeting HOSE and HNX exchanges. Stock data is fetched via the `vnstock` library (no credentials required).

**Roadmap phases:**
- Project 1 (Apr–May 2025): Minimum Variance Portfolio, SQLite pipeline, Streamlit dashboard
- Project 2 (Jun–Sep 2025): Efficient Frontier, Auto-Rebalancing, NLP Sentiment Analysis
- Thesis (Oct 2025–Mar 2026): Ensemble ML, VaR/CVaR Risk Management, Backtesting Engine

## Setup

```bash
pip install -r requirements.txt
```

Run the Streamlit dashboard:
```bash
streamlit run app/app.py
```

## Architecture

The pipeline flows through four layers in `src/`:

1. **`data_loader.py`** — ETL: fetch OHLCV data from vnstock, persist to SQLite under `data/raw/`
2. **`features.py`** — Compute returns and volatility from raw OHLCV data; output goes to `data/processed/`
3. **`portfolio_metrics.py`** — Build expected return vectors and covariance matrices from features
4. **`optimizer.py`** — Run `scipy.optimize` to solve for minimum variance / efficient frontier weights

**`app/app.py`** is the Streamlit frontend that calls into `src/` modules and renders Plotly charts.

**`notebooks/`** is for EDA and experimentation — results that prove out should be promoted to `src/`.

Raw data (`data/raw/`), processed data (`data/processed/`), model artifacts (`*.pkl`, `*.db`), and report outputs (`reports/`) are all gitignored.

## Tech Stack

- Data: `vnstock3` (VCIQuote primary), `yfinance` (fallback), `pandas`, SQLite
- Optimization: `numpy`, `scipy.optimize`
- Visualization: `streamlit`, `plotly`
- ML (Phase 2+): `scikit-learn`, `xgboost`, `tensorflow`

## Current Status — updated 21/04/2026

**Week 5: COMPLETE** — Streamlit dashboard live at mctgiangproject1.streamlit.app; report Chapter 2 drafted

### Completed src/ files
- `src/data_loader.py` — Full ETL: VCIQuote primary, yfinance fallback, SQLite insert/load; VN30 updated Q1/2026 (VPL in, BCM out), 30 tickers current as of 21/04/2026
- `src/update_db.py` — Standalone CLI: `python src/update_db.py [--tickers X Y Z] [--start YYYY-MM-DD] [--replace]`
- `src/features.py` — calc_returns(), calc_log_returns(), build_returns_matrix(method='simple'|'log'), annualized_return(), annualized_volatility(), ticker_stats(), all_ticker_stats(); TRADING_DAYS=252; verified vs Excel ✅
- `src/portfolio_metrics.py` — expected_returns(), covariance_matrix(), correlation_matrix(), portfolio_stats(weights, μ, Σ), display_metrics(); end date auto-read from DB ✅
- `src/optimizer.py` — portfolio_variance(), min_variance_portfolio(), display_portfolio(), CLI; SLSQP solver; RISK_FREE_RATE=0.045; 30-ticker MVP: 33.9% Vol reduction ✅

### Completed app/ files
- `app/app.py` — Production Streamlit dashboard: green brand palette (#146026), Inter font, HTML KPI cards, donut chart, MVP vs EW bar chart, correlation heatmap, allocation table, VIE/ENG toggle, PDF export (browser print), Excel export (3 sheets), Update data button, cloud auto-init DB

### Live deployment
- **URL:** https://mctgiangproject1.streamlit.app
- Cloud DB: auto-init via `_db_is_ready()` (file + COUNT>1000), auto-reinit on container restart

### Next: Wed 22/04 — mobile test + friend UAT
- Test public URL from mobile phone
- Ask 1 person to use app without guidance — note issues
- Continue report Chapter 3 (MPT theory, SLSQP)

### Data source note
`vnstock3` VCI Company API returns 403 Forbidden. **Use `VCIQuote` direct import:**
```python
from vnstock3.explorer.vci.quote import Quote as VCIQuote
```
VCI Guest tier rate limit: 20 req/min → `time.sleep(4)` already in `fetch_ticker_vci()`.

### DB path note
`data_loader.py` resolves DB path relative to `__file__`: `../data/raw/portfolio.db`.
In notebooks (CWD = `notebooks/`), always use `load_from_db()` function — not raw sqlite3 path.
