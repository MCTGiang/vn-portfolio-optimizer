# VN Portfolio Optimizer

Optimal Portfolio Allocation for VN30: A Minimum Variance Approach Using Modern Portfolio Theory

🚀 **[Try it live at mctgiangproject1.streamlit.app →](https://mctgiangproject1.streamlit.app)**
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mctgiangproject1.streamlit.app)

![Dashboard demo](./docs/images/demo.gif)


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

## Architecture

### Data Flow

The system fetches OHLCV data from Vietnamese market APIs, transforms it into a returns matrix, and applies quadratic optimization to find the minimum variance portfolio.

`````mermaid
flowchart LR
    subgraph Sources ["Data Sources"]
        A1[vnstock KBSQuote]
        A2[yfinance .VN suffix]
    end
    
    subgraph Storage ["Persistent Storage"]
        DB[(SQLite<br/>portfolio.db)]
    end
    
    subgraph Pipeline ["Processing Pipeline"]
        L[data_loader.py<br/>ETL + Fallback]
        F[features.py<br/>Returns + Winsorize]
        M[portfolio_metrics.py<br/>μ, Σ, Sharpe]
        O[optimizer.py<br/>SLSQP Solver]
    end
    
    subgraph UI ["User Interface"]
        S[Streamlit Dashboard<br/>Plotly Charts]
        E[Excel Export]
        P[PDF Export]
    end
    
    A1 -->|primary| L
    A2 -.->|fallback| L
    L -->|INSERT OR IGNORE| DB
    DB --> F
    F --> M
    M --> O
    O --> S
    S --> E
    S --> P
    
    style A1 fill:#e8f5e9,stroke:#146026,stroke-width:2px
    style A2 fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style DB fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style O fill:#146026,color:#fff,stroke:#146026,stroke-width:2px
    style S fill:#80c433,color:#000,stroke:#146026,stroke-width:2px
`````

**Key design decisions:**

- **Multi-source fallback**: vnstock is primary (native VN market data), yfinance is fallback for reliability
- **SQLite over Postgres**: Zero setup overhead, sufficient for VN30's ~40K rows, embedded in the app
- **Layer separation**: Each module has a single responsibility — data_loader knows about APIs, features knows about time series, optimizer knows about SLSQP
- **Cached queries**: Streamlit's `@st.cache_data(ttl=3600)` avoids redundant DB queries during a session

### Code Structure

Module dependencies follow a strict bottom-up hierarchy — no circular dependencies, no cross-layer imports.

`````mermaid
graph TD
    subgraph App ["Application Layer"]
        APP["app/app.py<br/><i>Streamlit UI + Charts</i>"]
    end
    
    subgraph Core ["Analytics Core"]
        OPT["src/optimizer.py<br/><i>SLSQP + MVP solver</i>"]
        MET["src/portfolio_metrics.py<br/><i>Portfolio stats</i>"]
        FEAT["src/features.py<br/><i>Returns + Winsorize</i>"]
    end
    
    subgraph Data ["Data Layer"]
        DL["src/data_loader.py<br/><i>vnstock + yfinance</i>"]
        DB[("SQLite<br/>portfolio.db")]
    end
    
    APP --> OPT
    APP --> MET
    APP --> FEAT
    APP --> DL
    OPT --> MET
    OPT --> FEAT
    MET --> FEAT
    FEAT --> DL
    DL --> DB
    
    style APP fill:#80c433,color:#000,stroke:#146026,stroke-width:2px
    style OPT fill:#146026,color:#fff,stroke:#146026,stroke-width:2px
    style DL fill:#2e7d32,color:#fff,stroke:#146026,stroke-width:2px
    style DB fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
`````

The dependency graph is a directed acyclic graph (DAG) — this is important because:

- **Testable in isolation**: Lower layers can be tested without mocking upper layers
- **Refactoring safety**: Changes in `data_loader.py` propagate up, but not sideways
- **Clear reasoning**: New contributors can understand the codebase top-down or bottom-up

### Optimization Flow

The full flow from user selection to result rendering takes ~1.2 seconds on cold cache, ~50ms on warm cache.

`````mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant UI as Streamlit App
    participant Cache as st.cache_data
    participant DL as data_loader
    participant DB as SQLite
    participant F as features
    participant M as metrics
    participant O as optimizer
    
    U->>UI: Select 5 VN30 stocks
    UI->>Cache: Check cache key
    
    alt Cache hit
        Cache-->>UI: Return cached result
    else Cache miss
        UI->>DL: load_from_db(tickers, dates)
        DL->>DB: SELECT OHLCV
        DB-->>DL: DataFrame per ticker
        DL-->>UI: Combined DataFrame
        
        UI->>F: build_returns_matrix()
        F-->>UI: Returns matrix (N days × M assets)
        
        UI->>M: expected_returns + cov_matrix
        M-->>UI: μ vector + Σ matrix
        
        UI->>O: min_variance_portfolio()
        Note over O: SLSQP iterates until convergence<br/>~500ms for 5 assets
        O-->>UI: Optimal weights
        
        UI->>Cache: Store result (TTL=1h)
    end
    
    UI-->>U: Render KPI + Donut + Bar + Heatmap
`````

## Results — Project 1

| Portfolio | # Assets | MVP Return | MVP Vol | EW Vol | Vol Reduction | Sharpe (MVP) |
|-----------|----------|------------|---------|--------|---------------|--------------|
| VCB + BID (high correlation) | 02 | 8.98% | 24.51% | 25.47% | 3.8% | 0.183 |
| 5 diverse sectors | 05 | 7.10% | 19.64% | 21.46% | 8.5% | 0.132 |
| 5 banks (same sector) | 05 | 12.06% | 22.65% | 24.84% | 8.8% | 0.334 |
| 10 VN30 stocks | 10 | 10.39% | 18.66% | 21.25% | 12.2% | 0.316 |
| **29 VN30 (full)** | **29** | **7.25%** | **15.62%** | **21.08%** | **25.9%** | **0.176** |

📊 **Reproduce these numbers:** Run [`notebooks/09_final_benchmark_results.ipynb`](./notebooks/09_final_benchmark_results.ipynb) or see [`reports/benchmark_results_20260821.csv`](./reports/benchmark_results_20260821.csv).

## Screenshots

<table>
  <tr>
    <td><img src="./docs/images/detail-optimization.png" alt="Optimization panel"/></td>
    <td><img src="./docs/images/detail-heatmap.png" alt="Correlation heatmap"/></td>
  </tr>
  <tr>
    <td align="center"><em>KPI cards and allocation donut chart</em></td>
    <td align="center"><em>Correlation heatmap for portfolio analysis</em></td>
  </tr>
</table>

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

## License

MIT
