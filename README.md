# VN Portfolio Optimizer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mctgiangproject1.streamlit.app/)

Optimal Portfolio Allocation for VN30: A Minimum Variance Approach Using Modern Portfolio Theory

## 🚀 Live Demo

👉 **[https://mctgiangproject1.streamlit.app/](https://mctgiangproject1.streamlit.app/)**

---

## Roadmap

This is Phase 1 of a 4-phase incremental research project on quantitative investment for Vietnamese equities. Each phase builds on the previous one, culminating in a production-ready platform for retail investors.

| Phase | Timeline | Status | Focus |
|-------|----------|--------|-------|
| ✅ **Project 1** | 2026 Q2 | **Complete** | MPT + MVP dashboard for VN30 — *this repo* |
| 🚧 **Project 2** | 2026 Q4 | Planning | Efficient Frontier + Auto-Rebalancing + NLP Sentiment |
| 📅 **Project 3** | 2027 Q1 | Planned | Ensemble ML forecasting (LSTM/XGBoost/RF) + VaR/CVaR + Backtesting |
| 📅 **Thesis** | 2027 Q1–2027 Q2 | Planned | Production system: microservices, real-time data, trading API integration |

### Project 2 preview (starting September 2026)

Building on the MVP foundation, Project 2 will extend the optimizer to select portfolios across the full Efficient Frontier (multiple risk levels), automate periodic rebalancing with transaction costs, and integrate NLP sentiment analysis from Vietnamese financial news (VnExpress, CafeF) using PhoBERT.

### Long-term vision

The final thesis will deliver an end-to-end investment platform integrating ensemble ML price forecasting, portfolio optimization, and advanced risk management (VaR/CVaR/Stress Testing), deployed as microservices with real-time SSI FastConnect API integration for actual trading execution.

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
