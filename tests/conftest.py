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


@pytest.fixture
def sample_tickers_diverse():
    """5 diverse VN30 stocks across different sectors."""
    return ["VCB", "VNM", "HPG", "FPT", "MWG"]


@pytest.fixture
def sample_tickers_banks():
    """5 banks - same sector, high correlation."""
    return ["VCB", "BID", "CTG", "ACB", "MBB"]


@pytest.fixture
def sample_tickers_pair_correlated():
    """2 highly correlated stocks (both banks)."""
    return ["VCB", "BID"]


@pytest.fixture
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


@pytest.fixture
def date_range_full():
    """Full backtest date range for Project 1."""
    return {"start": "2021-01-01", "end": "2026-08-20"}


@pytest.fixture
def date_range_short():
    """Short date range for quick tests (1 month)."""
    return {"start": "2026-01-01", "end": "2026-01-31"}


# ═══════════════════════════════════════════════════════════════════
# Constants fixtures
# ═══════════════════════════════════════════════════════════════════


@pytest.fixture
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