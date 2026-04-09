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

## Current Status — updated 08/04/2026

**Week 2: IN PROGRESS** — features.py committed; Excel verification + plot remaining

### Completed src/ files
- `src/data_loader.py` — Full ETL: VCIQuote primary, yfinance fallback, SQLite insert/load, 30 VN30 tickers, 39,189 rows (2021–2026)
- `src/update_db.py` — Standalone CLI: `python src/update_db.py [--tickers X Y Z] [--start YYYY-MM-DD] [--replace]`
- `src/features.py` — Committed 08/04: calc_returns(), calc_log_returns(), build_returns_matrix(method='simple'|'log'), annualized_return(), annualized_volatility(), ticker_stats(), all_ticker_stats(); TRADING_DAYS=252

### Next: Finish Week 2 (Fri 10/04)
- Spot-check: verify VCB annualized return for 2024 vs Excel (~20m)
- Plot return distribution histogram per ticker — identify most volatile stock (~30m)

### Data source note
`vnstock3` VCI Company API returns 403 Forbidden. **Use `VCIQuote` direct import:**
```python
from vnstock3.explorer.vci.quote import Quote as VCIQuote
```
VCI Guest tier rate limit: 20 req/min → `time.sleep(4)` already in `fetch_ticker_vci()`.

### DB path note
`data_loader.py` resolves DB path relative to `__file__`: `../data/raw/portfolio.db`.
In notebooks (CWD = `notebooks/`), always use `load_from_db()` function — not raw sqlite3 path.
