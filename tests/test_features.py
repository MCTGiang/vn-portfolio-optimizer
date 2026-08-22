"""
Unit tests for src/features.py

Test cases migrated from notebooks/20_test_portfolio_optimizer.ipynb
covering returns matrix construction, winsorization, and data joining.

Categories:
- TC-07 to TC-09: Returns matrix structure and shape
- TC-10 to TC-12: Data quality (no NaN, winsorization, edge cases)
"""

import numpy as np
import pandas as pd
import pytest

# ═══════════════════════════════════════════════════════════════════
# TC-07 to TC-09: Returns matrix structure
# ═══════════════════════════════════════════════════════════════════


class TestReturnsMatrixStructure:
    """Tests verifying build_returns_matrix() output structure."""

    def test_tc07_returns_matrix_returns_dataframe(self, returns_matrix_5_diverse):
        """
        TC-07: build_returns_matrix() returns a pandas DataFrame.
        """
        assert isinstance(returns_matrix_5_diverse, pd.DataFrame)
        assert not returns_matrix_5_diverse.empty, "Returns matrix should not be empty"

    def test_tc08_returns_matrix_has_datetime_index(self, returns_matrix_5_diverse):
        """
        TC-08: Returns matrix has DatetimeIndex.

        Verified for time-series alignment across tickers.
        """
        assert isinstance(
            returns_matrix_5_diverse.index, pd.DatetimeIndex
        ), f"Expected DatetimeIndex, got {type(returns_matrix_5_diverse.index).__name__}"

        # Verify chronological order (monotonic increasing)
        assert (
            returns_matrix_5_diverse.index.is_monotonic_increasing
        ), "Index should be sorted chronologically"

    def test_tc09_returns_matrix_shape_matches_tickers(
        self, returns_matrix_5_diverse, sample_tickers_diverse
    ):
        """
        TC-09: Returns matrix has one column per input ticker.
        """
        n_tickers = len(sample_tickers_diverse)
        assert (
            returns_matrix_5_diverse.shape[1] == n_tickers
        ), f"Expected {n_tickers} columns, got {returns_matrix_5_diverse.shape[1]}"

        # Verify all requested tickers are in columns
        expected_cols = set(sample_tickers_diverse)
        actual_cols = set(returns_matrix_5_diverse.columns)
        assert (
            expected_cols == actual_cols
        ), f"Column mismatch. Expected {expected_cols}, got {actual_cols}"


# ═══════════════════════════════════════════════════════════════════
# TC-10 to TC-12: Data quality
# ═══════════════════════════════════════════════════════════════════


class TestReturnsMatrixDataQuality:
    """Tests verifying data quality of returns matrix."""

    def test_tc10_no_nan_values(self, returns_matrix_5_diverse):
        """
        TC-10: Returns matrix has no NaN values.

        NaN values would indicate:
        - Missing data for some ticker on a given date
        - Inner join not properly applied
        - First-day return not properly handled
        """
        nan_count = returns_matrix_5_diverse.isna().sum().sum()
        assert nan_count == 0, (
            f"Returns matrix contains {nan_count} NaN values. "
            f"Inner join across tickers should remove all NaN."
        )

    def test_tc11_winsorization_within_bounds(self, returns_matrix_5_diverse):
        """
        TC-11: Winsorization at ±15% is applied correctly.

        No return should exceed the ±0.15 threshold (per ADR-002).
        """
        max_return = returns_matrix_5_diverse.max().max()
        min_return = returns_matrix_5_diverse.min().min()

        # Allow tiny floating-point tolerance
        assert (
            max_return <= 0.15 + 1e-9
        ), f"Max return {max_return:.4f} exceeds winsorization bound +0.15"
        assert (
            min_return >= -0.15 - 1e-9
        ), f"Min return {min_return:.4f} below winsorization bound -0.15"

    def test_tc12_returns_are_numeric(self, returns_matrix_5_diverse):
        """
        TC-12: All returns are numeric (float), not object/string.

        Verifies proper type conversion during pipeline processing.
        """
        for col in returns_matrix_5_diverse.columns:
            dtype = returns_matrix_5_diverse[col].dtype
            assert np.issubdtype(
                dtype, np.floating
            ), f"Column {col} has non-float dtype: {dtype}"


# ═══════════════════════════════════════════════════════════════════
# Bonus: Additional feature tests
# ═══════════════════════════════════════════════════════════════════


class TestReturnsMatrixEdgeCases:
    """Edge cases and error handling for features module."""

    @pytest.mark.edge_case
    def test_returns_matrix_pair_correlated(self, returns_matrix_pair):
        """
        Returns matrix for 2 highly correlated stocks (VCB + BID)
        should have same structure as larger portfolios.
        """
        assert isinstance(returns_matrix_pair, pd.DataFrame)
        assert returns_matrix_pair.shape[1] == 2
        assert returns_matrix_pair.isna().sum().sum() == 0

    @pytest.mark.edge_case
    def test_returns_matrix_full_vn30_shape(self, returns_matrix_29_full):
        """
        Returns matrix for full VN30 should have 29 columns.

        Also verifies large-scale processing works without OOM.
        """
        assert returns_matrix_29_full.shape[1] == 29
        assert (
            returns_matrix_29_full.shape[0] > 1000
        ), "Expected at least 1000 trading days across 5+ years"

    @pytest.mark.slow
    def test_returns_matrix_reasonable_variance(self, returns_matrix_29_full):
        """
        Daily return variance should be in reasonable range for equities.

        Typical daily std for Vietnamese stocks: 1-3% (0.01-0.03).
        Annualized: 15-45%.
        """
        daily_stds = returns_matrix_29_full.std()

        # No stock should have suspiciously low variance
        assert (daily_stds > 0.005).all(), (
            f"Some stocks have suspiciously low daily std: "
            f"{daily_stds[daily_stds <= 0.005].to_dict()}"
        )

        # No stock should have suspiciously high variance (winsorization active)
        assert (daily_stds < 0.05).all(), (
            f"Some stocks have suspiciously high daily std (winsorization may not be applied): "
            f"{daily_stds[daily_stds >= 0.05].to_dict()}"
        )
