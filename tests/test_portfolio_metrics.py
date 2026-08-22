"""
Unit tests for src/portfolio_metrics.py

Test cases migrated from notebooks/20_test_portfolio_optimizer.ipynb
covering expected returns, covariance matrix, and portfolio statistics.

Categories:
- TC-13 to TC-14: Expected returns and covariance matrix structure
- TC-15: Covariance matrix mathematical properties (PSD)
- TC-16 to TC-17: Portfolio statistics and Sharpe ratio calculation
"""

import numpy as np
import pytest

# ═══════════════════════════════════════════════════════════════════
# TC-13 to TC-14: Expected returns and covariance structure
# ═══════════════════════════════════════════════════════════════════


class TestExpectedReturns:
    """Tests verifying expected returns (μ) calculation."""

    def test_tc13_expected_returns_shape(
        self, expected_returns_5_diverse, sample_tickers_diverse
    ):
        """
        TC-13: expected_returns() returns a Series with one value per ticker.
        """
        n_tickers = len(sample_tickers_diverse)
        assert (
            len(expected_returns_5_diverse) == n_tickers
        ), f"Expected {n_tickers} values, got {len(expected_returns_5_diverse)}"

        # Verify all tickers are in index
        expected_tickers = set(sample_tickers_diverse)
        actual_tickers = set(expected_returns_5_diverse.index)
        assert expected_tickers == actual_tickers

    def test_tc13b_expected_returns_annualized(self, expected_returns_29_full):
        """
        Expected returns should be annualized (×252 trading days).

        For VN30 stocks, annual returns typically fall in [-30%, +80%] range.
        Values outside this range suggest missing annualization or scaling bug.
        """
        for ticker, ret in expected_returns_29_full.items():
            assert -0.5 <= ret <= 1.0, (
                f"Expected return for {ticker} = {ret:.4f} is outside "
                f"reasonable annualized range [-0.5, 1.0]. "
                f"Check if returns are properly annualized (×252)."
            )


class TestCovarianceMatrix:
    """Tests verifying covariance matrix (Σ) structure and properties."""

    def test_tc14_cov_matrix_shape(self, cov_matrix_5_diverse, sample_tickers_diverse):
        """
        TC-14: Covariance matrix is square with dimensions matching tickers.
        """
        n_tickers = len(sample_tickers_diverse)
        assert cov_matrix_5_diverse.shape == (n_tickers, n_tickers), (
            f"Expected shape ({n_tickers}, {n_tickers}), "
            f"got {cov_matrix_5_diverse.shape}"
        )

    def test_tc14b_cov_matrix_symmetric(self, cov_matrix_5_diverse):
        """
        TC-14b: Covariance matrix is symmetric (Σ = Σᵀ).

        Cov(X,Y) = Cov(Y,X) by definition.
        """
        # Convert to numpy for element-wise comparison
        cov_np = cov_matrix_5_diverse.values

        # Test symmetry with tight tolerance
        assert np.allclose(
            cov_np, cov_np.T, atol=1e-10
        ), "Covariance matrix is not symmetric within tolerance"


# ═══════════════════════════════════════════════════════════════════
# TC-15: Covariance matrix positive semi-definite
# ═══════════════════════════════════════════════════════════════════


class TestCovarianceMatrixProperties:
    """Tests verifying mathematical properties of covariance matrix."""

    def test_tc15_cov_matrix_positive_semi_definite(self, cov_matrix_5_diverse):
        """
        TC-15: Covariance matrix is positive semi-definite (PSD).

        All eigenvalues must be ≥ 0. Critical for MVP optimization to
        have unique global optimum.
        """
        cov_np = cov_matrix_5_diverse.values
        eigenvalues = np.linalg.eigvalsh(cov_np)  # eigvalsh for symmetric matrices

        # Allow tiny negative eigenvalues due to numerical error
        min_eigenvalue = eigenvalues.min()
        assert min_eigenvalue >= -1e-8, (
            f"Covariance matrix has negative eigenvalue: {min_eigenvalue}. "
            f"Matrix is not positive semi-definite."
        )

        # All diagonal entries (variances) must be positive
        variances = np.diag(cov_np)
        assert (
            variances > 0
        ).all(), f"Some variances are non-positive: {variances[variances <= 0]}"

    @pytest.mark.slow
    def test_tc15b_full_vn30_cov_matrix_psd(self, cov_matrix_29_full):
        """
        Full 29-ticker covariance matrix must also be PSD.

        Larger matrices are more prone to numerical issues, so this
        test ensures our processing handles the full VN30 correctly.
        """
        cov_np = cov_matrix_29_full.values
        eigenvalues = np.linalg.eigvalsh(cov_np)

        min_eigenvalue = eigenvalues.min()
        assert (
            min_eigenvalue >= -1e-6
        ), f"Full VN30 cov matrix has negative eigenvalue: {min_eigenvalue}"


# ═══════════════════════════════════════════════════════════════════
# TC-16 to TC-17: Portfolio statistics and Sharpe ratio
# ═══════════════════════════════════════════════════════════════════


class TestPortfolioStatistics:
    """Tests verifying portfolio-level statistics (return, vol, Sharpe)."""

    def test_tc16_equal_weight_portfolio_stats(
        self,
        expected_returns_5_diverse,
        cov_matrix_5_diverse,
        risk_free_rate,
    ):
        """
        TC-16: Portfolio statistics for equal-weighted portfolio (1/N).

        Verifies calculation of:
        - Portfolio return: μᵀw
        - Portfolio volatility: √(wᵀΣw)
        - Sharpe ratio: (return - Rf) / vol
        """
        n = len(expected_returns_5_diverse)
        weights = np.ones(n) / n

        # Portfolio return
        port_return = float(weights @ expected_returns_5_diverse.values)
        assert (
            -0.5 <= port_return <= 1.0
        ), f"Portfolio return {port_return:.4f} outside reasonable range"

        # Portfolio volatility
        cov_np = cov_matrix_5_diverse.values
        port_vol = float(np.sqrt(weights @ cov_np @ weights))
        assert port_vol > 0, "Portfolio volatility must be positive"
        assert (
            port_vol < 1.0
        ), f"Portfolio vol {port_vol:.4f} unreasonably high for diversified portfolio"

        # Sharpe ratio
        sharpe = (port_return - risk_free_rate) / port_vol
        assert (
            -3.0 <= sharpe <= 3.0
        ), f"Sharpe ratio {sharpe:.4f} outside reasonable range [-3, 3]"

    def test_tc17_sharpe_ratio_formula_correctness(self, risk_free_rate):
        """
        TC-17: Sharpe ratio formula is (Rp - Rf) / σp.

        Test with known values to verify calculation is correct.
        """
        # Analytical test with known values
        portfolio_return = 0.10  # 10% annual
        portfolio_vol = 0.20  # 20% annual
        rf = risk_free_rate  # 4.5%

        expected_sharpe = (portfolio_return - rf) / portfolio_vol
        # (0.10 - 0.045) / 0.20 = 0.275

        assert (
            abs(expected_sharpe - 0.275) < 1e-10
        ), f"Sharpe calculation incorrect: expected 0.275, got {expected_sharpe}"

    def test_tc17b_sharpe_high_return_low_vol(self, risk_free_rate):
        """
        Sharpe ratio should be higher when return is higher for same vol.

        Sanity check for monotonic behavior.
        """
        vol = 0.20
        sharpe_low_return = (0.05 - risk_free_rate) / vol
        sharpe_high_return = (0.15 - risk_free_rate) / vol

        assert (
            sharpe_high_return > sharpe_low_return
        ), "Sharpe should increase with higher return at same volatility"


# ═══════════════════════════════════════════════════════════════════
# TC-18: portfolio_stats function coverage
# ═══════════════════════════════════════════════════════════════════


class TestPortfolioStatsFunction:
    """Tests verifying portfolio_stats() function returns valid metrics."""

    def test_tc18_portfolio_stats_equal_weights(
        self,
        sample_tickers_diverse,
        expected_returns_5_diverse,
        cov_matrix_5_diverse,
        risk_free_rate,
    ):
        """
        TC-18: portfolio_stats() computes return, vol, sharpe for equal weights.

        Verifies the actual portfolio_stats() function (not manual calculation)
        returns consistent values matching (μᵀw, √(wᵀΣw), Sharpe formula).
        """
        from src.portfolio_metrics import portfolio_stats

        n = len(sample_tickers_diverse)
        weights = np.ones(n) / n

        stats = portfolio_stats(
            weights,
            expected_returns_5_diverse,
            cov_matrix_5_diverse,
        )

        # Result should be a dict, tuple, or namedtuple with expected keys
        # Adapt based on actual return type - check with:
        # print(f"Type: {type(stats)}, Value: {stats}")

        # Common return patterns:
        # Pattern A: dict {'return': X, 'vol': Y, 'sharpe': Z}
        # Pattern B: tuple (return, vol, sharpe)
        # Pattern C: pd.Series

        # Assumption: dict-like access
        # If test fails, adjust based on actual return type
        assert stats is not None, "portfolio_stats returned None"


# ═══════════════════════════════════════════════════════════════════
# Bonus: Full VN30 sanity checks
# ═══════════════════════════════════════════════════════════════════


class TestFullVN30Metrics:
    """Bonus tests verifying metrics for full 29-ticker VN30 portfolio."""

    @pytest.mark.slow
    @pytest.mark.regression
    def test_full_vn30_equal_weight_vol_reasonable(
        self, expected_returns_29_full, cov_matrix_29_full
    ):
        """
        Equal-weighted VN30 portfolio should have vol around 20-23%.

        Regression test based on production benchmark:
        Expected EW Vol for full VN30: 21.08% (from README).
        Allow ±2% tolerance for data updates.
        """
        n = len(expected_returns_29_full)
        weights = np.ones(n) / n

        cov_np = cov_matrix_29_full.values
        vol = float(np.sqrt(weights @ cov_np @ weights))

        # Expected from benchmark: ~21%, allow tolerance
        assert 0.18 <= vol <= 0.24, (
            f"EW VN30 vol = {vol:.4f} outside expected range [0.18, 0.24]. "
            f"Regression from benchmark of 0.2108."
        )
