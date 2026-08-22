"""
Integration tests for VN Portfolio Optimizer end-to-end pipeline.

Since min_variance_portfolio() encapsulates the full pipeline
(DB -> features -> metrics -> optimizer -> output dict), integration
tests focus on:
- Cross-portfolio consistency
- Regression against README benchmark
- Edge cases (single asset, high correlation)
"""

import pytest
import numpy as np
import pandas as pd


# ═══════════════════════════════════════════════════════════════════
# TC-25 to TC-27: Full pipeline for different portfolio sizes
# ═══════════════════════════════════════════════════════════════════


class TestFullPipelineIntegration:
    """End-to-end tests verifying full flow works for various portfolios."""

    @pytest.mark.integration
    def test_tc25_full_pipeline_5_diverse(self, mvp_result_5_diverse):
        """
        TC-25: Full pipeline for 5 diverse stocks produces valid MVP.
        """
        r = mvp_result_5_diverse
        
        assert r["success"] is True
        assert len(r["weights"]) == 5
        assert abs(r["weights"].sum() - 1.0) < 1e-6
        assert (r["weights"] >= -1e-6).all()
        assert r["port_volatility"] > 0
        assert r["port_volatility"] < r["equal_weights_vol"]
        assert r["improvement_pct"] > 0

    @pytest.mark.integration
    def test_tc26_full_pipeline_banks_high_correlation(
        self, sample_tickers_banks, date_range_full
    ):
        """
        TC-26: Full pipeline handles high-correlation portfolio (5 banks).
        
        Even with high correlation between banks, MVP should converge
        and produce valid weights (may be concentrated).
        """
        from src.optimizer import min_variance_portfolio
        
        r = min_variance_portfolio(
            sample_tickers_banks,
            date_range_full["start"],
            date_range_full["end"],
        )
        
        assert r["success"] is True
        assert len(r["weights"]) == 5
        assert abs(r["weights"].sum() - 1.0) < 1e-6
        assert (r["weights"] >= -1e-6).all()
        # Improvement may be smaller due to high correlation
        assert r["improvement_pct"] >= 0

    @pytest.mark.integration
    @pytest.mark.slow
    def test_tc27_full_pipeline_29_vn30(self, mvp_result_29_full):
        """
        TC-27: Full pipeline handles full 29-ticker VN30.
        
        Largest portfolio - ensures no scaling/memory issues.
        """
        r = mvp_result_29_full
        
        assert r["success"] is True
        assert len(r["weights"]) == 29
        assert abs(r["weights"].sum() - 1.0) < 1e-6
        assert (r["weights"] >= -1e-6).all()
        
        # Full VN30 should have best diversification
        assert r["port_volatility"] < 0.18, (
            f"Full VN30 vol {r['port_volatility']:.4f} unexpectedly high"
        )
        assert r["improvement_pct"] > 15.0, (
            f"Full VN30 improvement {r['improvement_pct']:.2f}% too small"
        )


# ═══════════════════════════════════════════════════════════════════
# TC-28: README benchmark regression
# ═══════════════════════════════════════════════════════════════════


class TestBenchmarkRegression:
    """Regression test protecting README credibility."""

    @pytest.mark.integration
    @pytest.mark.regression
    @pytest.mark.slow
    def test_tc28_full_vn30_matches_readme_headline(self, mvp_result_29_full):
        """
        TC-28: Full VN30 metrics match README documented values.
        
        README benchmark (from Results table):
        - MVP vol: 15.62%
        - EW vol: 21.08%
        - Vol reduction: 25.9%
        - Sharpe: 0.176
        
        If this test fails, either optimizer regressed or README needs update.
        """
        r = mvp_result_29_full
        
        # MVP volatility (benchmark: 0.1562)
        assert 0.140 <= r["port_volatility"] <= 0.175, (
            f"MVP vol {r['port_volatility']:.4f} outside [0.140, 0.175]"
        )
        
        # EW volatility (benchmark: 0.2108)
        assert 0.190 <= r["equal_weights_vol"] <= 0.230, (
            f"EW vol {r['equal_weights_vol']:.4f} outside [0.190, 0.230]"
        )
        
        # Vol reduction (benchmark: 25.9%)
        assert 22.0 <= r["improvement_pct"] <= 29.0, (
            f"Improvement {r['improvement_pct']:.2f}% outside [22, 29]"
        )