# Setup Guide

Detailed installation and configuration instructions for VN Portfolio Optimizer.

## Prerequisites

- **Python 3.11+** (required due to pandas 3.0+ dependency)
- **Git** for cloning the repository
- **~50MB free disk space** for dependencies + market data

## Local Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/MCTGiang/vn-portfolio-optimizer.git
cd vn-portfolio-optimizer
```

### Step 2: Create virtual environment

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

Main dependencies:
- `streamlit` — web UI framework
- `pandas`, `numpy` — data manipulation
- `scipy` — optimization (SLSQP solver)
- `plotly` — interactive charts
- `vnstock`, `yfinance` — Vietnamese market data
- `pytest` — testing framework

### Step 4: Run the app

```bash
streamlit run app/app.py
```

The app will open automatically at `http://localhost:8501`.

## First-Run Initialization

On first launch, the app auto-downloads OHLCV data for 29 VN30 stocks 
(2021-present). This process:

- Takes **3-5 minutes** depending on network speed
- Creates `data/raw/portfolio.db` (~40MB SQLite file)
- Uses vnstock as primary source, yfinance as fallback

**Note:** If you cloned the repo, the DB is already included (~3.4MB compressed 
in git). First launch will only update to latest sessions.

## Optional: Update Market Data

To fetch latest trading sessions after initial setup:

```python
from src.data_loader import update_db

# Fetch all sessions since last update
update_db(start='2021-01-01')

# Or specify date range
update_db(start='2026-08-01', end='2026-08-20')
```

## Running Tests

The project includes 46 pytest tests across 5 modules:

```bash
# Run all tests
pytest -v

# Run only fast tests (skip slow integration tests)
pytest -m "not slow" -v

# Run only integration tests
pytest -m integration -v

# Generate coverage report
pytest --cov=src --cov-report=html
```

Open `htmlcov/index.html` to view coverage details.

## Troubleshooting

### `ModuleNotFoundError: No module named 'src'`

Ensure you activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Streamlit port already in use

```bash
streamlit run app/app.py --server.port 8502
```

### Database initialization fails

If auto-download fails due to API rate limits, wait 5-10 minutes and retry:
```bash
python -c "from src.data_loader import update_db; update_db(start='2021-01-01')"
```

### vnstock connection errors

The app automatically falls back to yfinance if vnstock fails. Errors 
in logs are informational — check final DB summary to verify data loaded.

## Development Setup

For contributors developing new features:

```bash
# Install dev dependencies (black, ruff already in requirements.txt)
pip install -r requirements.txt

# Format code before committing
black src/ tests/

# Lint code before committing
ruff check src/ tests/
```

See `pyproject.toml` for tool configuration.

---

**Related documentation:**
- [Architecture Decisions](./architecture.md) — Design rationale
- [Development Log](./development-log.md) — Sprint retrospective
- [Roadmap](./roadmap.md) — Phase 1-4 planning