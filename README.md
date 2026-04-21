# VN Portfolio Optimizer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mctgiangproject1.streamlit.app/)

Hệ thống tối ưu hóa danh mục đầu tư theo Modern Portfolio Theory — Minimum Variance Portfolio trên thị trường chứng khoán Việt Nam (VN30).

## 🚀 Live Demo

👉 **[https://mctgiangproject1.streamlit.app/](https://mctgiangproject1.streamlit.app/)**

---

## Roadmap

| Phase | Timeline | Scope |
|-------|----------|-------|
| Project 1 | Apr–May 2025 | Minimum Variance Portfolio, SQLite pipeline, Streamlit dashboard |
| Project 2 | Jun–Sep 2025 | Efficient Frontier, Auto-Rebalancing, NLP Sentiment Analysis |
| Thesis | Oct 2025–Mar 2026 | Ensemble ML, VaR/CVaR Risk Management, Backtesting Engine |

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

Streamlit App: *(to be updated in Week 6)*

## Data Source

Stock price data is sourced from the Ho Chi Minh Stock Exchange (HOSE)
and Hanoi Stock Exchange (HNX) via the `vnstock` library (public data, no credentials required).

## Results — Project 1

| Portfolio | Expected Return | Volatility | Sharpe Ratio |
|-----------|----------------|------------|--------------|
| Minimum Variance | TBD | TBD | TBD |
| Equal Weights | TBD | TBD | TBD |

*(Results will be updated upon project completion)*

## License

MIT
