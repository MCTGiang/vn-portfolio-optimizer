# Architecture Decisions

This document captures the key technical decisions made during Project 1 
development, along with the reasoning behind them. Each decision follows 
a lightweight ADR (Architecture Decision Record) format.

## Table of Contents

1. [ADR-001: SQLite for Persistence](#adr-001-sqlite-for-persistence)
2. [ADR-002: Winsorization at ±15%](#adr-002-winsorization-at-15)
3. [ADR-003: SLSQP for Optimization](#adr-003-slsqp-for-optimization)
4. [ADR-004: vnstock Primary + yfinance Fallback](#adr-004-vnstock-primary--yfinance-fallback)
5. [ADR-005: No Pre-Computed Returns in DB](#adr-005-no-pre-computed-returns-in-db)
6. [ADR-006: Streamlit for Frontend](#adr-006-streamlit-for-frontend)

---

## ADR-001: SQLite for Persistence

### Context

Need to persist ~40,000 OHLCV records (29 VN30 stocks × ~1,425 trading days). 
Data is accessed frequently during optimization, but writes are infrequent 
(daily updates only). Application is deployed on Streamlit Community Cloud 
with limited setup capabilities.

### Decision

Use **SQLite** as embedded database, single file `data/raw/portfolio.db`.

### Alternatives Considered

- **PostgreSQL**: Overkill for read-heavy workload of this size. Adds deployment complexity, requires external service on Streamlit Cloud.
- **CSV files**: No SQL query capability, slower for filtering by date range, no ACID guarantees.
- **Parquet files**: Better for analytics workloads but no random access, harder to update incrementally, requires PyArrow dependency.

### Rationale

1. **Zero setup overhead** — SQLite is bundled with Python's stdlib (`sqlite3`), no external service needed
2. **Sufficient performance** — ~40K rows fits easily in memory, queries complete in <100ms
3. **Simpler deployment** — Streamlit Cloud requires no external DB configuration
4. **Native `INSERT OR IGNORE`** — handles idempotent updates elegantly for daily data refresh
5. **File-based** — easy to backup, share, or replace (not committed to git due to size)

### Trade-offs

- **Cannot scale beyond single writer** — acceptable for single-user tool with periodic batch updates
- **Not suitable for concurrent multi-user access** — Project 3+ will migrate to PostgreSQL when multi-user features are added

### Related Code

- `src/data_loader.py::create_table()`
- `src/data_loader.py::get_connection()`
- `src/data_loader.py::insert_to_db()`

---

## ADR-002: Winsorization at ±15%

### Context

Vietnamese stock market has daily price limits (±7% for HOSE), but returns 
computed from close-to-close prices can exceed this due to:

- Gap opens (news released after close)
- Stock splits and dividend adjustments (Vietnamese market ex-date handling)
- Data source discrepancies between vnstock and yfinance
- Extreme events like SHB Q1/2021 showing ~10% daily moves

Untreated outliers significantly bias the covariance matrix Σ used in MVP 
optimization, leading to unstable and unpredictable weight allocations.

### Decision

Apply **winsorization at ±15%** to daily returns before computing statistics:

```python
returns = returns.clip(lower=-0.15, upper=0.15)
```

### Alternatives Considered

- **±7% (match HOSE daily limit)**: Too tight — filters out legitimate gap opens and dividend adjustments
- **±20% or wider**: Doesn't protect against split-adjusted outliers or data errors
- **Interquartile range (IQR) method**: More complex, doesn't leverage domain knowledge of VN market limits
- **Remove observations entirely**: Loses information; problematic when outliers concentrate in specific tickers
- **No outlier treatment**: Covariance matrix becomes unstable, MVP weights unpredictable across different data windows

### Rationale

1. **Domain knowledge** — 15% represents "extreme but plausible" in Vietnamese market context
2. **Simple and interpretable** — easy to explain to project reviewers and end users
3. **Preserves data** — doesn't remove observations, just caps magnitudes
4. **Empirically validated** — tested across 5 portfolio configurations without loss of signal
5. **Reproducible** — deterministic threshold, no dependence on data distribution

### Trade-offs

- **Slight bias toward moderate returns** — acceptable for MPT applications focused on variance minimization
- **Not appropriate for tail risk analysis** — Project 3's VaR/CVaR calculations will use raw (non-winsorized) returns to preserve tail information

### Related Code

- `src/features.py::build_returns_matrix()`
- `notebooks/02_Clean_data_calc_returns.ipynb` — original exploration of outlier patterns

---

## ADR-003: SLSQP for Optimization

### Context

The Minimum Variance Portfolio optimization is a **quadratic programming (QP) problem** with:

- **Objective**: `min wᵀΣw` (quadratic in w)
- **Equality constraint**: `Σwᵢ = 1` (fully invested)
- **Inequality constraints**: `wᵢ ≥ 0` for all i (no short-selling per Vietnamese market regulations)

Need a solver that handles this problem shape efficiently within a Python 
scientific stack.

### Decision

Use **`scipy.optimize.minimize` with `method='SLSQP'`** (Sequential Least Squares Programming).

### Alternatives Considered

- **CVXPY**: Cleaner API for convex optimization, but adds external dependency and slower for problems of this size
- **Analytical closed-form solution**: Only works without inequality constraints (short-selling allowed); doesn't match VN regulations
- **Interior-point methods (via cvxopt)**: More sophisticated but overkill for problems with <100 assets
- **Genetic algorithms**: Unnecessary — problem is convex with unique global optimum, no need for stochastic search

### Rationale

1. **Bundled with SciPy** — no extra dependency, part of standard scientific Python stack
2. **Handles both equality and inequality constraints** natively without reformulation
3. **Fast convergence** — <500ms for portfolios up to 29 assets on standard hardware
4. **Well-documented** — extensive scipy examples make it easy for reviewers to verify correctness
5. **Convex problem guarantees** — Σ is Positive Semi-Definite → unique global optimum → SLSQP consistently finds it

### Trade-offs

- **Slower than analytical solution** for constraint-free case — acceptable given we need inequality constraints
- **No warm-start optimization** — retrains from scratch each call, mitigated by Streamlit's `@st.cache_data` caching
- **Limited to smooth objectives** — not an issue for QP but limits extension to non-smooth risk measures like CVaR (will use different solver in Project 3)

### Related Code

- `src/optimizer.py::min_variance_portfolio()`
- `notebooks/05_MVP.ipynb` — original implementation exploration

---

## ADR-004: vnstock Primary + yfinance Fallback

### Context

Vietnamese market data has unique characteristics:

- Not natively supported by international sources like Yahoo Finance (requires `.VN` suffix)
- Yahoo returns delayed/incomplete data for some VN30 tickers
- Native VN sources like `vnstock` provide better data quality but occasionally fail on cloud deployments

Need a data source strategy that balances quality and reliability.

### Decision

Use **`vnstock` (KBSQuote source) as primary**, **`yfinance` with `.VN` suffix as automatic fallback**.

### Alternatives Considered

- **vnstock only**: Occasional deployment failures on Streamlit Cloud (dependency issues with IPython)
- **yfinance only**: Slower response times, less accurate for VN market, doesn't support all VN30 stocks reliably
- **SSI FastConnect API**: Requires broker account registration, unnecessary complexity for open-source tool
- **Web scraping (CafeF, VnExpress)**: Fragile parsers, violates Terms of Service, not sustainable

### Rationale

1. **Resilience** — if vnstock fails (network, rate limit, dependency issues), system continues working
2. **Best-of-both** — native VN data source when possible, universal fallback otherwise
3. **Zero user configuration** — fallback logic is automatic and transparent to end user
4. **Production-thinking signal** — multi-source strategy demonstrates awareness of external dependency risks

### Trade-offs

- **Data consistency risk** — vnstock and yfinance may report slightly different prices (rare, <1% of cases)
- **More code paths to test** — mitigated by comprehensive test cases in `notebooks/20_test_portfolio_optimizer.ipynb`
- **Fallback latency** — when vnstock fails, first-try adds ~2-3s overhead before switching

### Related Code

- `src/data_loader.py::fetch_ticker()` — main dispatcher with try/except logic
- `src/data_loader.py::fetch_ticker_kbs()` — vnstock primary implementation
- `src/data_loader.py::fetch_ticker_yfinance()` — yfinance fallback implementation

---

## ADR-005: No Pre-Computed Returns in DB

### Context

Daily returns and rolling statistics (mean, std, covariance) are computed 
frequently during optimization. A design decision was needed: pre-compute 
these once and store in DB, or recompute from raw OHLCV each time.

### Decision

**Do not pre-compute or store returns in DB**. Recompute from raw OHLCV data 
each time optimization is triggered. Use application-level caching for 
performance.

### Alternatives Considered

- **Store returns table**: Faster but adds sync complexity when new price data arrives
- **Materialized views**: Not supported by SQLite (available in PostgreSQL but overkill)
- **Application-level caching only**: Current approach using Streamlit's `@st.cache_data(ttl=3600)`

### Rationale

1. **Ticker-subset dependency** — returns matrix depends on inner join across selected tickers, so per-ticker pre-computation still requires post-processing
2. **Cheap operation** — `pct_change()` on 1,425 rows takes ~5ms; negligible vs 500ms SLSQP optimization
3. **Single source of truth** — OHLCV is the only "raw" data; everything else is a derived view
4. **No synchronization bugs** — update DB with new prices → returns automatically reflect it without cascade update logic
5. **Winsorization parameter flexibility** — the ±15% threshold can change without requiring DB rebuild

### Trade-offs

- **Slightly more CPU per query** — negligible impact for 29 assets, would need reconsideration at 500+ assets
- **Cannot pre-materialize per-ticker statistics** for cross-portfolio comparison dashboards (not needed in Project 1)

### Related Code

- `src/features.py::build_returns_matrix()` — always recomputes from OHLCV
- `app/app.py` — `@st.cache_data(ttl=3600)` for session-level caching to avoid redundant computation within a user session

---

## ADR-006: Streamlit for Frontend

### Context

Need an interactive dashboard for Vietnamese retail investors (non-technical 
end users). Requirements include:

- Multi-select widget for portfolio composition (choose from 29 VN30 stocks)
- Interactive charts (donut allocation, bar comparison, correlation heatmap)
- Export to Excel and PDF formats
- Bilingual UI (Vietnamese and English)
- Zero installation required (accessible via URL)

### Decision

Use **Streamlit** as web framework with **Plotly** for interactive visualizations.

### Alternatives Considered

- **Flask + Vanilla JS**: More flexible and performant, but requires ~10x more code and separate frontend/backend management
- **React + FastAPI**: Modern production-grade stack, but excessive complexity for solo student project scope
- **Dash by Plotly**: Similar to Streamlit conceptually, but smaller community, more callback boilerplate, harder deployment
- **Jupyter notebook + Voila**: Notebook-based UI, but poor user experience for non-technical end users

### Rationale

1. **Python-native** — no context switching between backend Python and frontend JavaScript
2. **Rapid iteration** — code changes trigger auto-reload, no build step required
3. **Free hosting** — Streamlit Community Cloud provides free public hosting for open-source projects
4. **Built-in widgets** — `st.multiselect`, `st.slider`, `st.dataframe` work out of the box
5. **Plotly integration** — `st.plotly_chart()` handles interactive charts seamlessly with zoom, hover, export
6. **Rapid MVP philosophy** — appropriate for research/prototyping phase; production migration is planned

### Trade-offs

- **Not suitable for high-concurrency** — acceptable for single-user demo, but not production-scale
- **Session state limitations** — solved via `@st.cache_data` for this project's needs
- **Custom UI limitations** — Streamlit's design system is opinionated; heavily custom layouts require workarounds
- **Migration planned for Thesis** — will move to Next.js + FastAPI for production deployment supporting multiple users

### Related Code

- `app/app.py` — main dashboard entry point (~800 lines including UI + PDF export)
- `notebooks/06_Streamlit.ipynb` — original UI prototype exploration

---

## Future Decisions

Decisions planned for upcoming projects:

- **ADR-007** (Project 2): Efficient Frontier solver — CVXPY vs custom SLSQP loop
- **ADR-008** (Project 2): Sentiment analysis model — PhoBERT vs Multilingual BERT for Vietnamese
- **ADR-009** (Project 2): News data source — scraping vs API vs RSS feeds
- **ADR-010** (Project 3): ML ensemble strategy — Stacking vs Weighted Average vs Voting
- **ADR-011** (Project 3): Backtesting framework — vectorbt vs backtrader vs custom
- **ADR-012** (Thesis): Cloud deployment — AWS EKS vs GCP GKE vs self-hosted Kubernetes
- **ADR-013** (Thesis): Authentication — JWT vs OAuth2 vs Firebase Auth

## References

- [Michael Nygard's original ADR blog post](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [ThoughtWorks Technology Radar on ADRs](https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records)
- Markowitz, H. (1952). "Portfolio Selection". *Journal of Finance*, 7(1), 77-91.
- [Streamlit documentation](https://docs.streamlit.io/)
- [SciPy SLSQP reference](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html)