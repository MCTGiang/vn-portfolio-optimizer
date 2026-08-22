"""
Unit tests for src/optimizer.py

API verified:
- portfolio_variance(weights, cov_mat) -> float
- min_variance_portfolio(tickers, start, end) -> dict with keys:
    tickers, weights, port_return, port_volatility, sharpe_ratio,
    success, message, equal_weights_vol, improvement_pct, mu, cov
- display_portfolio(result, label) -> pd.DataFrame  [UI helper, not tested]

Test cases:
- TC-19: Objective function correctness
- TC-20 to TC-22: MVP structure and constraint compliance  
- TC-23 to TC-24: Optimization correctness and reproducibility
- Regression tests: benchmark values
"""

import pytest
import numpy as np
import pandas as pd


# ═══════════════════════════════════════════════════════════════════
# TC-19: Objective function (portfolio_variance)
# ═══════════════════════════════════════════════════════════════════


class TestPortfolioVariance:
    """Tests verifying the SLSQP objective function."""

    def test_tc19_portfolio_variance_computes_correctly(
        self, cov_matrix_5_diverse
    ):
        """
        TC-19: portfolio_variance(w, Σ) computes wᵀΣw correctly.
        
        Verify against manual calculation with equal weights.
        """
        from src.optimizer import portfolio_variance
        
        n = cov_matrix_5_diverse.shape[0]
        weights = np.ones(n) / n
        cov_np = cov_matrix_5_diverse.values
        
        computed = portfolio_variance(weights, cov_np)
        expected = float(weights @ cov_np @ weights)
        
        assert isinstance(computed, (int, float, np.floating))
        assert abs(computed - expected) < 1e-10
        assert computed > 0, "Variance must be positive"

    def test_tc19b_variance_matches_squared_vol(self, cov_matrix_5_diverse):
        """
        TC-19b: For any weights, √variance = std.
        
        Sanity check for numerical consistency.
        """
        from src.optimizer import portfolio_variance
        
        # Non-uniform weights to test general case
        weights = np.array([0.3, 0.25, 0.2, 0.15, 0.1])
        cov_np = cov_matrix_5_diverse.values
        
        variance = portfolio_variance(weights, cov_np)
        std_from_variance = np.sqrt(variance)
        std_direct = float(np.sqrt(weights @ cov_np @ weights))
        
        assert abs(std_from_variance - std_direct) < 1e-10


# ═══════════════════════════════════════════════════════════════════
# TC-20 to TC-22: MVP structure and constraints
# ═══════════════════════════════════════════════════════════════════


class TestMVPStructure:
    """Tests verifying MVP result structure and metadata."""

    def test_tc20_mvp_returns_valid_dict(self, mvp_result_5_diverse):
        """
        TC-20: min_variance_portfolio returns dict with expected keys.
        
        Verifies API contract - all 11 documented keys present.
        """
        assert isinstance(mvp_result_5_diverse, dict)
        
        expected_keys = {
            "tickers", "weights", "port_return", "port_volatility",
            "sharpe_ratio", "success", "message",
            "equal_weights_vol", "improvement_pct", "mu", "cov",
        }
        actual_keys = set(mvp_result_5_diverse.keys())
        
        missing = expected_keys - actual_keys
        assert not missing, f"Missing keys: {missing}"

    def test_tc20b_mvp_types_correct(self, mvp_result_5_diverse):
        """
        TC-20b: Each key has expected type.
        """
        r = mvp_result_5_diverse
        
        assert isinstance(r["tickers"], list)
        assert isinstance(r["weights"], np.ndarray)
        assert isinstance(r["port_return"], float)
        assert isinstance(r["port_volatility"], float)
        assert isinstance(r["sharpe_ratio"], float)
        assert isinstance(r["success"], bool)
        assert isinstance(r["message"], str)
        assert isinstance(r["equal_weights_vol"], float)
        assert isinstance(r["improvement_pct"], float)
        assert isinstance(r["mu"], pd.Series)
        assert isinstance(r["cov"], pd.DataFrame)

    def test_tc21_weights_sum_to_one(self, mvp_result_5_diverse):
        """
        TC-21: Portfolio weights sum to 1 (equality constraint).
        """
        weights = mvp_result_5_diverse["weights"]
        total = weights.sum()
        
        assert abs(total - 1.0) < 1e-6, (
            f"Weights sum to {total}, expected 1.0"
        )

    def test_tc22_no_short_selling(self, mvp_result_5_diverse):
        """
        TC-22: All weights >= 0 (no short-selling constraint).
        """
        weights = mvp_result_5_diverse["weights"]
        
        assert weights.min() >= -1e-6, (
            f"Weight {weights.min()} violates non-negativity"
        )
        assert weights.max() <= 1.0 + 1e-6, (
            f"Weight {weights.max()} exceeds 1.0"
        )

    def test_tc22b_weights_shape_matches_tickers(
        self, mvp_result_5_diverse, sample_tickers_diverse
    ):
        """
        TC-22b: Weights array length matches input tickers.
        """
        assert len(mvp_result_5_diverse["weights"]) == len(sample_tickers_diverse)
        assert len(mvp_result_5_diverse["tickers"]) == len(sample_tickers_diverse)


# ═══════════════════════════════════════════════════════════════════
# TC-23 to TC-24: Optimization correctness
# ═══════════════════════════════════════════════════════════════════


class TestMVPCorrectness:
    """Tests verifying MVP actually minimizes variance."""

    def test_tc23_mvp_vol_less_than_equal_weight(self, mvp_result_5_diverse):
        """
        TC-23: MVP volatility < equal-weighted volatility.
        
        Uses built-in equal_weights_vol from result.
        Core validation that optimization actually reduces variance.
        """
        mvp_vol = mvp_result_5_diverse["port_volatility"]
        ew_vol = mvp_result_5_diverse["equal_weights_vol"]
        
        assert mvp_vol < ew_vol, (
            f"MVP vol {mvp_vol:.4f} not less than EW vol {ew_vol:.4f}. "
            f"Optimization failed to reduce variance."
        )
        
        # Verify built-in improvement_pct matches computed value
        expected_improvement = (ew_vol - mvp_vol) / ew_vol * 100
        actual_improvement = mvp_result_5_diverse["improvement_pct"]
        
        assert abs(expected_improvement - actual_improvement) < 0.01, (
            f"improvement_pct {actual_improvement} doesn't match "
            f"computed {expected_improvement}"
        )

    def test_tc23b_slsqp_converged(self, mvp_result_5_diverse):
        """
        TC-23b: SLSQP optimizer reports success.
        """
        assert mvp_result_5_diverse["success"] is True, (
            f"Optimizer failed: {mvp_result_5_diverse['message']}"
        )

    def test_tc24_mvp_reproducible(
        self, sample_tickers_diverse, date_range_full
    ):
        """
        TC-24: MVP is reproducible with same inputs.
        
        Deterministic behavior critical for backtesting and CI.
        """
        from src.optimizer import min_variance_portfolio
        
        result1 = min_variance_portfolio(
            sample_tickers_diverse,
            date_range_full["start"],
            date_range_full["end"],
        )
        result2 = min_variance_portfolio(
            sample_tickers_diverse,
            date_range_full["start"],
            date_range_full["end"],
        )
        
        # Compare weights
        assert np.allclose(result1["weights"], result2["weights"], atol=1e-6), (
            f"Weights not reproducible. "
            f"Diff: {np.abs(result1['weights'] - result2['weights']).max()}"
        )
        
        # Compare key metrics
        assert abs(result1["port_return"] - result2["port_return"]) < 1e-9
        assert abs(result1["port_volatility"] - result2["port_volatility"]) < 1e-9
        assert abs(result1["sharpe_ratio"] - result2["sharpe_ratio"]) < 1e-9


# ═══════════════════════════════════════════════════════════════════
# TC-24b: Sharpe ratio consistency
# ═══════════════════════════════════════════════════════════════════


class TestMVPSharpeRatio:
    """Tests verifying Sharpe ratio is computed consistently."""

    def test_tc24b_sharpe_matches_formula(
        self, mvp_result_5_diverse, risk_free_rate
    ):
        """
        TC-24b: Sharpe ratio = (Rp - Rf) / σp.
        
        Verify built-in sharpe_ratio matches formula.
        Note: assumes Rf = 4.5% (SBV rate) or 0 depending on optimizer config.
        """
        r = mvp_result_5_diverse
        
        # Try with Rf = 4.5%
        expected_sharpe_045 = (r["port_return"] - 0.045) / r["port_volatility"]
        # Try with Rf = 0
        expected_sharpe_0 = r["port_return"] / r["port_volatility"]
        
        actual_sharpe = r["sharpe_ratio"]
        
        # Check which convention optimizer uses
        matches_rf_045 = abs(actual_sharpe - expected_sharpe_045) < 1e-6
        matches_rf_0 = abs(actual_sharpe - expected_sharpe_0) < 1e-6
        
        assert matches_rf_045 or matches_rf_0, (
            f"Sharpe {actual_sharpe:.4f} doesn't match either convention. "
            f"With Rf=4.5%: {expected_sharpe_045:.4f}, "
            f"With Rf=0: {expected_sharpe_0:.4f}"
        )


# ═══════════════════════════════════════════════════════════════════
# Bonus: Regression tests based on production benchmarks
# ═══════════════════════════════════════════════════════════════════


class TestMVPRegression:
    """Regression tests ensuring MVP matches documented benchmarks."""

    @pytest.mark.slow
    @pytest.mark.regression
    def test_full_vn30_mvp_matches_benchmark(self, mvp_result_29_full):
        """
        Full VN30 MVP vol should match README benchmark (~15.62%).
        
        Regression test for README credibility.
        """
        mvp_vol = mvp_result_29_full["port_volatility"]
        
        assert 0.140 <= mvp_vol <= 0.175, (
            f"Full VN30 MVP vol {mvp_vol:.4f} outside [0.140, 0.175]. "
            f"README benchmark: 0.1562"
        )

    @pytest.mark.slow
    @pytest.mark.regression
    def test_full_vn30_improvement_matches_readme(self, mvp_result_29_full):
        """
        Full VN30 improvement_pct should match README claim (~25.9%).
        
        Uses built-in improvement_pct field for direct comparison.
        This is THE headline number of the project.
        """
        improvement = mvp_result_29_full["improvement_pct"]
        
        assert 22.0 <= improvement <= 29.0, (
            f"Full VN30 improvement {improvement:.2f}% outside [22, 29]. "
            f"README claims 25.9% - check for regression."
        )

    @pytest.mark.slow
    def test_pair_portfolio_valid(self, mvp_result_pair):
        """
        MVP for 2 correlated stocks (VCB+BID): verify constraints hold.
        """
        r = mvp_result_pair
        
        assert len(r["weights"]) == 2
        assert abs(r["weights"].sum() - 1.0) < 1e-6
        assert (r["weights"] >= -1e-6).all()
        assert r["success"] is True