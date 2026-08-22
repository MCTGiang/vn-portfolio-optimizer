# Notebooks Guide

Jupyter notebooks organized by development phase and purpose.

## Naming Convention

Sequential numbering reflects development chronology:

- `01-09`: Setup and initial development
- `10-19`: (Reserved for extended analysis - Project 2)
- `20-29`: Testing and validation
- `90-99`: Final canonical notebooks (outputs referenced in docs)

Date suffix format `YYYYMMDD` used for time-sensitive analyses.

## Categories

### Setup & Development (01-08)

Chronological notebooks capturing the Project 1 build journey:

| Notebook | Purpose |
|----------|---------|
| `01_fetch_data.ipynb` | Download VN30 OHLCV data from vnstock/yfinance |
| `02_Clean_data_calc_returns.ipynb` | Data cleaning + returns calculation |
| `03_Spot-check.ipynb` | Data quality verification (VCB spot-check) |
| `04_Covariance-Matrix.ipynb` | Covariance matrix construction |
| `05_MVP.ipynb` | Minimum Variance Portfolio implementation |
| `06_Streamlit.ipynb` | Streamlit UI prototype |
| `07.Test_Streamlit.ipynb` | UI integration testing |
| `08_UpdateAll_27.05.ipynb` | Batch data update script |

### Testing (20-29)

Formal test suites:

| Notebook | Purpose |
|----------|---------|
| `20_test_portfolio_optimizer.ipynb` | 28 unit test cases for optimizer |
| `21_test_all_20260821.ipynb` | Full regression suite for 2026-08-20 data |

### Final Analysis (90-99)

Canonical notebooks whose outputs are referenced in README/reports:

| Notebook | Purpose |
|----------|---------|
| `90_final_benchmark_results.ipynb` | Generate 5-portfolio benchmark table |

## Reading Order for New Contributors

To understand the project from scratch:

1. Read notebooks 01-05 in order to understand the analytical pipeline
2. Look at 06-07 to see UI development approach
3. Reference 20-21 to verify testing approach
4. Run 90 to reproduce headline benchmarks

## Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Ensure database is up to date
python -c "from src.data_loader import update_db; update_db(start='2021-01-01')"

# Launch Jupyter
jupyter notebook notebooks/
```

## Guidelines

- **Never commit `Untitled*.ipynb`** — always rename before staging
- **Clear outputs for heavy compute notebooks** to reduce file size
- **Preserve outputs for final notebooks (90-99)** for direct GitHub viewing