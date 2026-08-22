"""
Shared pytest fixtures for VN Portfolio Optimizer tests.

Fixtures defined here are automatically available to all test files
in the tests/ directory without explicit import.
"""

import sys
import pytest
from pathlib import Path

# Add project root to Python path so we can import src.* modules
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.data_loader import (
    create_table,
    get_connection,
    get_all_tickers,
    get_db_summary,
    load_from_db,
)


# ═══════════════════════════════════════════════════════════════════
# Database fixtures
# ═══════════════════════════════════════════════════════════════════


@pytest.fixture(scope="session")
def db_initialized():
    """
    Ensure database is initialized before running tests.
    
    Session scope: runs once per test session (not per test).
    """
    create_table()
    return True


@pytest.fixture(scope="session")
def db_connection(db_initialized):
    """
    Provide a database connection for tests that need direct DB access.
    
    Session scope: shared connection across all tests.
    Automatically closed after all tests complete.
    """
    conn = get_connection()
    yield conn
    conn.close()


@pytest.fixture(scope="session")
def db_summary(db_initialized):
    """
    Provide DB summary DataFrame for tests that check DB state.
    """
    return get_db_summary()


@pytest.fixture(scope="session")
def all_tickers(db_initialized):
    """
    Provide list of all tickers currently in the database.
    """
    return get_all_tickers()


# ═══════════════════════════════════════════════════════════════════
# Standard portfolio fixtures
# ═══════════════════════════════════════════════════════════════════


@pytest.fixture(scope="session")
def sample_tickers_diverse():
    """5 diverse VN30 stocks across different sectors."""
    return ["VCB", "VNM", "HPG", "FPT", "MWG"]

@pytest.fixture(scope="session")
def sample_tickers_banks():
    """5 banks - same sector, high correlation."""
    return ["VCB", "BID", "CTG", "ACB", "MBB"]


@pytest.fixture(scope="session")
def sample_tickers_pair_correlated():
    """2 highly correlated stocks (both banks)."""
    return ["VCB", "BID"]


@pytest.fixture(scope="session")
def vn30_tickers_full():
    """Full 29 VN30 tickers (excluding VPL which was listed in 05/2025)."""
    return [
        "ACB", "BID", "CTG", "DGC", "FPT", "GAS", "GVR", "HDB", "HPG",
        "LPB", "MBB", "MSN", "MWG", "PLX", "SAB", "SHB", "SSB", "SSI",
        "STB", "TCB", "TPB", "VCB", "VHM", "VIB", "VIC", "VJC", "VNM",
        "VPB", "VRE",
    ]


# ═══════════════════════════════════════════════════════════════════
# Date range fixtures
# ═══════════════════════════════════════════════════════════════════


@pytest.fixture(scope="session")
def date_range_full():
    """Full backtest date range for Project 1."""
    return {"start": "2021-01-01", "end": "2026-08-20"}


@pytest.fixture(scope="session")
def date_range_short():
    """Short date range for quick tests (1 month)."""
    return {"start": "2026-01-01", "end": "2026-01-31"}


# ═══════════════════════════════════════════════════════════════════
# Constants fixtures
# ═══════════════════════════════════════════════════════════════════


@pytest.fixture(scope="session")
def risk_free_rate():
    """SBV operating rate used as risk-free rate."""
    return 0.045


# ═══════════════════════════════════════════════════════════════════
# Reusable data fixtures
# ═══════════════════════════════════════════════════════════════════


@pytest.fixture
def vcb_price_data(date_range_full):
    """
    Load VCB price data from DB for use across multiple tests.
    Prevents redundant DB queries in each test.
    """
    return load_from_db("VCB", date_range_full["start"], date_range_full["end"])

# ═══════════════════════════════════════════════════════════════════
# Features fixtures - returns matrix and computed statistics
# ═══════════════════════════════════════════════════════════════════


@pytest.fixture(scope="session")
def returns_matrix_5_diverse(sample_tickers_diverse, date_range_full):
    """
    Returns matrix for 5 diverse VN30 stocks.
    
    Session scope: computed once, reused across multiple tests.
    """
    from src.features import build_returns_matrix
    return build_returns_matrix(
        sample_tickers_diverse,
        date_range_full["start"],
        date_range_full["end"],
    )


@pytest.fixture(scope="session")
def returns_matrix_29_full(vn30_tickers_full, date_range_full):
    """
    Returns matrix for full VN30 (29 stocks).
    
    Session scope: this is the largest and most expensive matrix,
    so we compute once and reuse across many tests.
    """
    from src.features import build_returns_matrix
    return build_returns_matrix(
        vn30_tickers_full,
        date_range_full["start"],
        date_range_full["end"],
    )


@pytest.fixture(scope="session")
def returns_matrix_pair(sample_tickers_pair_correlated, date_range_full):
    """Returns matrix for 2 correlated stocks (VCB + BID)."""
    from src.features import build_returns_matrix
    return build_returns_matrix(
        sample_tickers_pair_correlated,
        date_range_full["start"],
        date_range_full["end"],
    )


# ═══════════════════════════════════════════════════════════════════
# Portfolio metrics fixtures - μ, Σ pre-computed
# ═══════════════════════════════════════════════════════════════════
#
# Note: Functions in src/portfolio_metrics.py take (tickers, start, end)
# and load data internally. They do NOT accept a pre-computed returns 
# matrix as input.
#
# Signatures verified:
#   expected_returns(tickers, start, end) -> pd.Series
#   covariance_matrix(tickers, start, end) -> pd.DataFrame


@pytest.fixture(scope="session")
def expected_returns_5_diverse(sample_tickers_diverse, date_range_full):
    """Expected returns (μ) for 5 diverse stocks, annualized."""
    from src.portfolio_metrics import expected_returns
    return expected_returns(
        sample_tickers_diverse,
        date_range_full["start"],
        date_range_full["end"],
    )


@pytest.fixture(scope="session")
def cov_matrix_5_diverse(sample_tickers_diverse, date_range_full):
    """Covariance matrix (Σ) for 5 diverse stocks, annualized."""
    from src.portfolio_metrics import covariance_matrix
    return covariance_matrix(
        sample_tickers_diverse,
        date_range_full["start"],
        date_range_full["end"],
    )


@pytest.fixture(scope="session")
def expected_returns_29_full(vn30_tickers_full, date_range_full):
    """Expected returns for full VN30, annualized."""
    from src.portfolio_metrics import expected_returns
    return expected_returns(
        vn30_tickers_full,
        date_range_full["start"],
        date_range_full["end"],
    )


@pytest.fixture(scope="session")
def cov_matrix_29_full(vn30_tickers_full, date_range_full):
    """Covariance matrix for full VN30, annualized."""
    from src.portfolio_metrics import covariance_matrix
    return covariance_matrix(
        vn30_tickers_full,
        date_range_full["start"],
        date_range_full["end"],
    )