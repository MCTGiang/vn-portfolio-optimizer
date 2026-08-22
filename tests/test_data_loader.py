"""
Unit tests for src/data_loader.py

Test cases migrated from notebooks/20_test_portfolio_optimizer.ipynb
following the TC-XX numbering convention for traceability.

Categories:
- TC-01 to TC-03: Database structure and connection
- TC-04 to TC-06: Data loading and querying
"""

import sqlite3

import pandas as pd
import pytest

# ═══════════════════════════════════════════════════════════════════
# TC-01 to TC-03: Database structure
# ═══════════════════════════════════════════════════════════════════


class TestDatabaseStructure:
    """Tests verifying database schema and connection."""

    def test_tc01_db_connection_valid(self, db_connection):
        """
        TC-01: Database connection is valid and can execute queries.

        Verifies that get_connection() returns a working SQLite connection.
        """
        assert isinstance(db_connection, sqlite3.Connection)

        # Execute simple query to verify connection is live
        cursor = db_connection.execute("SELECT 1")
        result = cursor.fetchone()
        assert result == (1,)

    def test_tc02_stock_prices_table_exists(self, db_connection):
        """
        TC-02: Table Stock_Prices exists in the database.

        Verifies that create_table() ran successfully during setup.
        """
        cursor = db_connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='Stock_Prices'"
        )
        result = cursor.fetchone()
        assert result is not None, "Table 'Stock_Prices' does not exist"
        assert result[0] == "Stock_Prices"

    def test_tc03_stock_prices_schema_correct(self, db_connection):
        """
        TC-03: Stock_Prices table has expected columns and types.

        Expected schema:
        - Ticker (TEXT, NOT NULL)
        - Date (TEXT, NOT NULL)
        - Open, High, Low, Close (REAL)
        - Volume (INTEGER)
        - PRIMARY KEY (Ticker, Date)
        """
        cursor = db_connection.execute("PRAGMA table_info(Stock_Prices)")
        columns = {
            row[1]: {"type": row[2], "notnull": row[3]} for row in cursor.fetchall()
        }

        expected_columns = {"Ticker", "Date", "Open", "High", "Low", "Close", "Volume"}
        actual_columns = set(columns.keys())

        assert expected_columns.issubset(
            actual_columns
        ), f"Missing columns: {expected_columns - actual_columns}"

        # Verify NOT NULL constraints on primary key columns
        assert columns["Ticker"]["notnull"] == 1, "Ticker should be NOT NULL"
        assert columns["Date"]["notnull"] == 1, "Date should be NOT NULL"


# ═══════════════════════════════════════════════════════════════════
# TC-04 to TC-06: Data loading and querying
# ═══════════════════════════════════════════════════════════════════


class TestDataLoading:
    """Tests verifying data loading functions."""

    def test_tc04_load_from_db_returns_dataframe(self, vcb_price_data):
        """
        TC-04: load_from_db() returns a valid DataFrame with expected columns.

        Uses the vcb_price_data fixture to avoid redundant DB queries.
        """
        assert isinstance(vcb_price_data, pd.DataFrame)
        assert len(vcb_price_data) > 0, "DataFrame should not be empty"

        # Verify expected columns exist
        expected_columns = {"Open", "High", "Low", "Close", "Volume"}
        actual_columns = set(vcb_price_data.columns)
        assert expected_columns.issubset(
            actual_columns
        ), f"Missing columns: {expected_columns - actual_columns}"

        # Verify DatetimeIndex
        assert isinstance(
            vcb_price_data.index, pd.DatetimeIndex
        ), "Index should be DatetimeIndex"

    def test_tc05_db_summary_has_29_tickers(self, db_summary):
        """
        TC-05: get_db_summary() returns summary for all 29 VN30 tickers.

        Note: VPL is excluded because it was listed in 05/2025
        (insufficient history for stable covariance estimation).
        """
        assert isinstance(db_summary, pd.DataFrame)
        assert len(db_summary) == 29, f"Expected 29 tickers, got {len(db_summary)}"

    def test_tc06_all_tickers_returns_29_symbols(self, all_tickers, vn30_tickers_full):
        """
        TC-06: get_all_tickers() returns list of 29 VN30 tickers.

        Verifies both count and content match expected VN30 basket.
        """
        assert isinstance(all_tickers, list)
        assert len(all_tickers) == 29

        # Verify all expected tickers are present
        actual_set = set(all_tickers)
        expected_set = set(vn30_tickers_full)

        missing = expected_set - actual_set
        extra = actual_set - expected_set

        assert not missing, f"Missing tickers: {missing}"
        assert not extra, f"Unexpected tickers: {extra}"


# ═══════════════════════════════════════════════════════════════════
# Additional edge case tests (bonus)
# ═══════════════════════════════════════════════════════════════════


class TestDataLoadingEdgeCases:
    """Edge cases and error handling for data loader."""

    @pytest.mark.edge_case
    def test_load_invalid_ticker_returns_empty(self, date_range_short):
        """
        Loading data for invalid ticker should return empty DataFrame,
        not raise an error (graceful handling).
        """
        from src.data_loader import load_from_db

        result = load_from_db(
            "INVALID_TICKER_XYZ",
            date_range_short["start"],
            date_range_short["end"],
        )

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    @pytest.mark.edge_case
    def test_load_date_range_no_data_returns_empty(self):
        """
        Loading data for date range with no trading (e.g., far future)
        should return empty DataFrame.
        """
        from src.data_loader import load_from_db

        result = load_from_db("VCB", "2100-01-01", "2100-01-31")

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
