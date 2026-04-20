"""
optimizer.py
Minimum Variance Portfolio optimizer using scipy.optimize.minimize.

Theory:
    Minimize:   w^T × Σ × w          (portfolio variance)
    Subject to: sum(weights) = 1      (fully invested)
                weight_i >= 0         (long-only, no short selling)

Solver: SLSQP — Sequential Least Squares Programming
    Works because the problem is convex (positive semi-definite Σ),
    guaranteeing that any local minimum found is also the global minimum.

Reference: Markowitz, H.M. (1952). Portfolio Selection. Journal of Finance.
"""

import numpy as np
import pandas as pd
import os
import sys
from scipy.optimize import minimize

sys.path.insert(0, os.path.dirname(__file__))
from data_loader import load_from_db, VN30_TICKERS
from features import build_returns_matrix
from portfolio_metrics import (
    expected_returns, covariance_matrix, portfolio_stats
)

TRADING_DAYS   = 252
RISK_FREE_RATE = 0.045   # Vietnam SBV reference rate ~4.5%


# ── Core objective function ───────────────────────────────────────────────────

def portfolio_variance(weights: np.ndarray,
                       cov_mat: np.ndarray) -> float:
    """
    Compute portfolio variance: w^T × Σ × w

    This is the objective function minimized by scipy.

    Args:
        weights : 1-D array of portfolio weights, shape (N,)
        cov_mat : Annualized covariance matrix, shape (N, N)

    Returns:
        Float — portfolio variance (NOT volatility)
    """
    return float(weights @ cov_mat @ weights) #Forced convert to float due to scipy expect objective function returns scalar, not numpy scalar

# ── Main optimizer ────────────────────────────────────────────────────────────

def min_variance_portfolio(tickers: list,
                           start: str = '2021-01-01',
                           end: str   = None) -> dict:
    """
    Find the Minimum Variance Portfolio for a list of tickers.

    Solves:
        min  w^T Σ w
        s.t. sum(w) = 1
             0 <= w_i <= 1

    Args:
        tickers : List of ticker symbols (min 2)
        start   : Start date 'YYYY-MM-DD'
        end     : End date 'YYYY-MM-DD'

    Returns:
        dict with keys:
            tickers          : list of tickers
            weights          : np.ndarray — optimal weights
            port_return      : float — annualized portfolio return
            port_volatility  : float — annualized portfolio volatility
            sharpe_ratio     : float — Sharpe Ratio (Rf = 4.5%)
            success          : bool — optimizer convergence
            message          : str — optimizer status message
            equal_weights_vol: float — equal weights baseline volatility
            improvement_pct  : float — volatility reduction vs equal weights
    """
    # Lấy end date từ DB nếu không truyền vào
    if end is None:
        from data_loader import get_db_summary
        summary = get_db_summary()
        end = summary['end_date'].max()
        
    N = len(tickers)
    if N < 2:
        raise ValueError("Need at least 2 tickers for portfolio optimization")

    # ── Lấy end date từ DB nếu không truyền vào ──────────────────────────────
    from data_loader import get_db_summary
    summary = get_db_summary()

    if end is None:
        end = summary['end_date'].max()

    # ── Kiểm tra mã có trong DB không ────────────────────────────────────────
    db_tickers = set(summary['Ticker'].tolist())
    missing = [t for t in tickers if t not in db_tickers]
    if missing:
        raise ValueError(
            f"Tickers not in DB: {missing}. Run update_db() first."
        )

    # ── Kiểm tra mã có đủ data không ─────────────────────────────────────────
    ticker_rows = summary[summary['Ticker'].isin(tickers)].set_index('Ticker')
    short = ticker_rows[ticker_rows['rows'] < 252].index.tolist()
    if short:
        print(f"⚠️  Warning: {short} có < 252 ngày — kết quả kém ổn định")
        
    # ── Inputs ──────────────────────────────────────────────────────────────
    mu  = expected_returns(tickers, start, end)   # Series N
    cov = covariance_matrix(tickers, start, end)  # DataFrame N×N

    cov_np = cov.values   # convert to numpy for scipy

    # ── Optimization setup ──────────────────────────────────────────────────
    w0 = np.array([1.0 / N] * N)   # warm start: equal weights

    constraints = [
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0}
    ]
    bounds = [(0.0, 1.0)] * N      # long-only

    # ── Run optimizer ────────────────────────────────────────────────────────
    result = minimize(
        fun     = portfolio_variance,
        x0      = w0,
        args    = (cov_np,),        # extra arg passed to objective function
        method  = 'SLSQP',
        bounds  = bounds,
        constraints = constraints,
        options = {'ftol': 1e-12, 'maxiter': 1000}
    )

    optimal_weights = result.x

    # ── Clean up tiny weights (numerical noise) ──────────────────────────────
    optimal_weights[optimal_weights < 1e-6] = 0.0
    # Re-normalize after zeroing out noise
    optimal_weights = optimal_weights / optimal_weights.sum()

    # ── Compute portfolio stats at optimal weights ───────────────────────────
    stats = portfolio_stats(optimal_weights, mu, cov, RISK_FREE_RATE)

    # ── Baseline: equal weights ──────────────────────────────────────────────
    eq_stats = portfolio_stats(w0, mu, cov, RISK_FREE_RATE)
    improvement = (eq_stats['port_volatility'] - stats['port_volatility']) \
                  / eq_stats['port_volatility'] * 100

    return {
        'tickers'          : tickers,
        'weights'          : optimal_weights,
        'port_return'      : stats['port_return'],
        'port_volatility'  : stats['port_volatility'],
        'sharpe_ratio'     : stats['sharpe_ratio'],
        'success'          : result.success,
        'message'          : result.message,
        'equal_weights_vol': eq_stats['port_volatility'],
        'improvement_pct'  : improvement,
        'mu'               : mu,
        'cov'              : cov,
    }


# ── Display helper ────────────────────────────────────────────────────────────

def display_portfolio(result: dict,
                      label: str = 'Minimum Variance Portfolio') -> pd.DataFrame:
    """
    Print formatted portfolio allocation table and metrics.

    Args:
        result : dict returned by min_variance_portfolio()
        label  : Display label

    Returns:
        DataFrame of allocation table (ticker, weight, return)
    """
    if not result['success']:
        print(f"⚠️  Optimizer did not converge: {result['message']}")

    print(f"\n{'='*55}")
    print(f"  {label}")
    print(f"{'='*55}")
    print(f"  Portfolio Return    : {result['port_return']:>8.2%}")
    print(f"  Portfolio Volatility: {result['port_volatility']:>8.2%}")
    print(f"  Sharpe Ratio        : {result['sharpe_ratio']:>8.3f}")
    print(f"{'─'*55}")
    print(f"  Equal Weights Vol   : {result['equal_weights_vol']:>8.2%}  (baseline)")
    print(f"  Volatility Reduction: {result['improvement_pct']:>7.1f}%")
    print(f"{'='*55}")

    # Allocation table — only show non-zero weights
    alloc = pd.DataFrame({
        'Ticker' : result['tickers'],
        'Weight' : result['weights'],
        'Exp Ret': result['mu'].values,
    })
    alloc = alloc[alloc['Weight'] > 0.001].copy()
    alloc = alloc.sort_values('Weight', ascending=False).reset_index(drop=True)
    alloc['Weight%']  = alloc['Weight'].apply(lambda x: f"{x:.1%}")
    alloc['Exp Ret%'] = alloc['Exp Ret'].apply(lambda x: f"{x:.1%}")

    print(f"\n  Allocation ({len(alloc)} active positions):")
    print(f"  {'Ticker':<8} {'Weight':>8} {'Exp Return':>12}")
    print(f"  {'─'*30}")
    for _, row in alloc.iterrows():
        print(f"  {row['Ticker']:<8} {row['Weight%']:>8} {row['Exp Ret%']:>12}")
    print(f"  {'─'*30}")
    print(f"  {'TOTAL':<8} {alloc['Weight'].sum():>8.1%}")

    return alloc[['Ticker', 'Weight%', 'Exp Ret%']]


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(
        description='Find Minimum Variance Portfolio for VN30 stocks'
    )
    parser.add_argument('--tickers', nargs='+',
                        default=['VCB','VNM','HPG','FPT','MWG'],
                        help='Tickers to optimize (default: 5 diverse stocks)')
    parser.add_argument('--start', default='2021-01-01',
                        help='Start date YYYY-MM-DD')
    parser.add_argument('--end',
                        default=datetime.today().strftime('%Y-%m-%d'),
                        help='End date YYYY-MM-DD (default: today)')
    args = parser.parse_args()

    print(f"Optimizing: {args.tickers}")
    result = min_variance_portfolio(args.tickers, args.start, args.end)
    display_portfolio(result)