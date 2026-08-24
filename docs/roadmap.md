# Roadmap

This project is Phase 1 of a **4-phase incremental research project** on 
quantitative investment for Vietnamese equities. Each phase builds on the 
previous one, culminating in a production-ready platform for retail investors.

## Phase Overview

| Phase | Timeline | Status | Focus |
|-------|----------|--------|-------|
| ✅ **Project 1** | 2026 Q2 | **Complete** | MPT + MVP dashboard for VN30 — *this repo* |
| 🚧 **Project 2** | 2026 Q4 | Planning | Efficient Frontier + Auto-Rebalancing + NLP Sentiment |
| 📅 **Project 3** | 2027 Q1 | Planned | Ensemble ML forecasting (LSTM/XGBoost/RF) + VaR/CVaR + Backtesting |
| 📅 **Thesis** | 2027 Q1–2027 Q2 | Planned | Production system: microservices, real-time data, trading API integration |

---

## Project 1 — VN Portfolio Optimizer ✅ (Complete)

**Repository:** [`vn-portfolio-optimizer`](https://github.com/MCTGiang/vn-portfolio-optimizer) 
(this repo)

**Delivered:**
- Modern Portfolio Theory (MPT) implementation for VN30 stocks
- Minimum Variance Portfolio (MVP) optimization via SLSQP
- Interactive Streamlit dashboard with Plotly visualizations
- 46-test pytest suite with GitHub Actions CI
- Full VN30 portfolio achieves **25.9% volatility reduction** vs equal-weighted baseline

**Key learnings:** Foundation of MPT theory, scipy optimization, Streamlit deployment,
pytest infrastructure, CI/CD automation.

---

## Project 2 — Efficient Frontier + Sentiment 🚧 (Planning)

**Repository:** `vn-portfolio-frontier` (starting September 2026)

**Planned features:**
- Select portfolios across the full **Efficient Frontier** (multiple risk levels)
- **Auto-rebalancing** with transaction costs and turnover constraints
- **NLP sentiment analysis** from Vietnamese financial news:
  - Sources: VnExpress, CafeF, VietStock
  - Model: PhoBERT (Vietnamese BERT) fine-tuned on financial text
  - Value: Structured extraction (ticker, event type, sentiment, magnitude)

**Technical additions:**
- PostgreSQL (upgrade from SQLite)
- Docker containerization
- Prefect for workflow orchestration
- dbt for data transformations
- pytest + GitHub Actions (already in place)

**Key decisions pending:**
- Prefect vs Airflow (target: commit by Sep 15, 2026)
- PhoBERT sentiment vs RAG for information extraction (target: Nov 15, 2026)

---

## Project 3 — Ensemble ML Forecasting 📅 (Planned)

**Timeline:** December 2026 – February 2027

**Planned features:**
- **Ensemble machine learning** for stock price forecasting:
  - LSTM (long short-term memory) for time-series patterns
  - XGBoost for feature-based prediction
  - Random Forest for robustness
- **Advanced risk management:**
  - Historical VaR (Value at Risk)
  - Parametric VaR
  - Monte Carlo simulation
  - CVaR (Conditional VaR / Expected Shortfall)
- **Walk-forward backtesting** engine:
  - Transaction cost modeling
  - Look-ahead bias prevention
  - Multiple rebalancing frequencies

---

## Thesis — Integrated Investment Platform 📅 (Planned)

**Timeline:** March – June 2027 (Bachelor's thesis)

**Final deliverable:** End-to-end investment platform integrating all three 
projects into a production-ready system.

**5 core components:**

1. **Integration layer** — Unified API across MPT, ML forecasting, sentiment
2. **Walk-forward backtesting engine** — With transaction costs, look-ahead prevention
3. **Risk metrics dashboard** — VaR + Monte Carlo + 3 stress scenarios (2008, 2020, 2022)
4. **Single-cloud deployment** — AWS or GCP (decision by Jan 31, 2027)
5. **Grafana monitoring** — Real-time system health, model drift detection

**Real-world integration:**
- **SSI FastConnect API** for actual trade execution
- Microservices architecture (FastAPI + Docker + Kubernetes)
- Real-time market data streaming

**Out of scope for thesis:**
- A/B testing framework
- Complex authentication (OAuth, SSO)
- Multi-user support beyond single account

---

## Skills Development Timeline

Aligned with the phase roadmap:

| Phase | Skills Focus |
|-------|--------------|
| Project 1 | Python, pandas, scipy, Streamlit, pytest, Git, CI/CD |
| Project 2 | PostgreSQL, Docker, Prefect, dbt, NLP (PhoBERT), fine-tuning |
| Project 3 | PyTorch/TensorFlow, LSTM, XGBoost, risk modeling, backtesting |
| Thesis | System design, microservices, cloud deployment, monitoring, trading APIs |

## Certifications Planned

- **AWS Cloud Practitioner** — Q2 2027 (aligned with cloud deployment decision)

---

## Vision Statement

Deliver an end-to-end investment platform for the Vietnamese market that 
democratizes access to quantitative finance tools traditionally reserved 
for institutional investors. The system will integrate:

- **Ensemble ML price forecasting** (Project 3)
- **Portfolio optimization** (Projects 1 & 2)  
- **Advanced risk management** (VaR/CVaR/Stress Testing)
- **NLP sentiment signals** (Project 2)
- **Real-time trade execution** (Thesis via SSI FastConnect)

Target end-user: Vietnamese retail investors currently underserved by 
existing platforms that lack transparent optimization, robust backtesting, 
and integrated risk analysis.