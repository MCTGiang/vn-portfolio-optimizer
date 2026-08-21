# VN Portfolio Optimizer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mctgiangproject1.streamlit.app/)

Optimal Portfolio Allocation for VN30: A Minimum Variance Approach Using Modern Portfolio Theory

## 🚀 Live Demo

👉 **[https://mctgiangproject1.streamlit.app/](https://mctgiangproject1.streamlit.app/)**

---

## Roadmap

| Phase | Timeline | Scope |
|-------|----------|-------|
| Project 1 | Apr–Jun 2026 | Minimum Variance Portfolio, SQLite pipeline, Streamlit dashboard |
| Project 2 | Sep–Nov 2026 | Efficient Frontier, Auto-Rebalancing, NLP Sentiment Analysis |
| Project 3 | Dec 2026 – Jan 2027 | Ensemble ML, VaR/CVaR Risk Management, Backtesting Engine |
| Thesis | Feb–May 2027 | Production System |

## Tech Stack

- **Data collection**: vnstock, pandas, SQLite
- **Optimization**: numpy, scipy.optimize
- **Visualization**: Streamlit, Plotly
- **ML (Phase 2+)**: scikit-learn, XGBoost, TensorFlow

## Project Structure
```
vn-portfolio-optimizer/
├── data/
│   ├── raw/               # Raw OHLCV data from vnstock
│   └── processed/         # Cleaned data and feature matrices
├── notebooks/             # EDA and experimentation notebooks
├── src/                   # Reusable Python modules
│   ├── data_loader.py     # ETL pipeline, SQLite connection
│   ├── features.py        # Returns, volatility calculations
│   ├── portfolio_metrics.py  # Expected return, covariance matrix
│   └── optimizer.py       # scipy-based portfolio optimizer
├── app/
│   └── app.py             # Streamlit dashboard
├── reports/               # PDF reports and result figures
├── requirements.txt
└── README.md
```

## Getting Started

```bash
git clone https://github.com/MCTGiang/vn-portfolio-optimizer.git
cd vn-portfolio-optimizer
pip install -r requirements.txt

# Fetch stock data (run once to populate local database)
python src/data_loader.py
```
## Live Demo

🚀 **[Try it live at mctgiangproject1.streamlit.app →](https://mctgiangproject1.streamlit.app)**

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mctgiangproject1.streamlit.app)

Try these sample portfolios:
- **Diverse 5 sectors:** VCB, VNM, HPG, FPT, MWG
- **Bank sector focus:** VCB, BID, CTG, TCB, MBB  
- **Full VN30 basket:** Select all 29 stocks

Features to explore: interactive optimization, correlation heatmap, Excel/PDF export.

## Data Source

Stock price data is sourced from the Ho Chi Minh Stock Exchange (HOSE)
and Hanoi Stock Exchange (HNX) via the `vnstock` library (public data, no credentials required).

## Results — Project 1

| Portfolio | # Assets | MVP Return | MVP Vol | EW Vol | Vol Reduction | Sharpe (MVP) |
|-----------|----------|------------|---------|--------|---------------|--------------|
| VCB + BID (high correlation) | 2 | 8.98% | 24.51% | 25.47% | 3.8% | 0.183 |
| 5 diverse sectors | 5 | 7.10% | 19.64% | 21.46% | 8.5% | 0.132 |
| 5 banks (same sector) | 5 | 12.06% | 22.65% | 24.84% | 8.8% | 0.334 |
| 10 VN30 stocks | 10 | 10.39% | 18.66% | 21.25% | 12.2% | 0.316 |
| **29 VN30 (full)** | **29** | **7.25%** | **15.62%** | **21.08%** | **25.9%** | **0.176** |

📊 **Reproduce these numbers:** Run [`notebooks/09_final_benchmark_results.ipynb`](./notebooks/09_final_benchmark_results.ipynb) or see [`reports/benchmark_results_20260821.csv`](./reports/benchmark_results_20260821.csv).
## License

MIT
