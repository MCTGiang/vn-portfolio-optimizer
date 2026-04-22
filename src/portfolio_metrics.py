"""
portfolio_metrics.py
Computes portfolio-level financial metrics using Modern Portfolio Theory.

Key functions:
    - expected_returns()   : annualized mean return per ticker
    - covariance_matrix()  : annualized covariance matrix
    - portfolio_stats()    : return, risk, sharpe for given weights
    - display_metrics()    : formatted summary table
"""

import numpy as np
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from data_loader import load_from_db, VN30_TICKERS
from features import build_returns_matrix, calc_returns

TRADING_DAYS = 252
RISK_FREE_RATE = 0.045   # SBV reference rate ~4.5% Vietnam


# ── Core metrics ───────────────────────────────────────────────────────────────

def expected_returns(tickers: list,
                     start: str,
                     end: str) -> pd.Series:
    """
    Compute annualized expected return for each ticker.

    Formula: mean(daily_simple_returns) × 252

    Args:
        tickers : List of ticker symbols
        start   : Start date 'YYYY-MM-DD'
        end     : End date 'YYYY-MM-DD'

    Returns:
        Series indexed by ticker, values = annualized expected return
    """
    matrix = build_returns_matrix(tickers, start, end)
    return matrix.mean() * TRADING_DAYS


def covariance_matrix(tickers: list,
                      start: str,
                      end: str) -> pd.DataFrame:
    """
    Compute annualized covariance matrix from daily returns.

    Formula: returns_matrix.cov() × 252

    Diagonal = annualized variance of each ticker (= volatility²)
    Off-diagonal = annualized covariance between ticker pairs

    Args:
        tickers : List of ticker symbols
        start   : Start date 'YYYY-MM-DD'
        end     : End date 'YYYY-MM-DD'

    Returns:
        DataFrame (N×N) — annualized covariance matrix
    """
    matrix = build_returns_matrix(tickers, start, end)
    return matrix.cov() * TRADING_DAYS


def correlation_matrix(tickers: list,
                       start: str,
                       end: str) -> pd.DataFrame:
    """
    Compute correlation matrix from daily returns.

    Normalized covariance — values between -1 and +1.
    Used for visualization and understanding co-movement.

    Args:
        tickers : List of ticker symbols
        start   : Start date 'YYYY-MM-DD'
        end     : End date 'YYYY-MM-DD'

    Returns:
        DataFrame (N×N) — correlation matrix
    """
    matrix = build_returns_matrix(tickers, start, end)
    return matrix.corr()


# ── Portfolio statistics ───────────────────────────────────────────────────────

def portfolio_stats(weights: np.ndarray,
                    exp_returns: pd.Series,
                    cov_mat: pd.DataFrame,
                    risk_free: float = RISK_FREE_RATE) -> dict:
    """
    Compute portfolio return, volatility, and Sharpe Ratio.

    Formulas:
        Portfolio return     = w^T × μ
        Portfolio variance   = w^T × Σ × w
        Portfolio volatility = sqrt(portfolio variance)
        Sharpe Ratio         = (return - risk_free) / volatility

    Args:
        weights     : Array of portfolio weights, must sum to 1
        exp_returns : Series of annualized expected returns per ticker
        cov_mat     : DataFrame — annualized covariance matrix (N×N)
        risk_free   : Annual risk-free rate (default: 4.5% Vietnam SBV)

    Returns:
        dict with keys: port_return, port_volatility, sharpe_ratio
    """
    weights = np.array(weights)

    # Portfolio return: weighted sum of individual returns
    port_return = float(weights @ exp_returns.values)

    # Portfolio variance: w^T × Σ × w
    port_variance = float(weights @ cov_mat.values @ weights)

    # Portfolio volatility: square root of variance
    port_volatility = float(np.sqrt(port_variance))

    # Sharpe Ratio: excess return per unit of risk
    sharpe = (port_return - risk_free) / port_volatility

    return {
        'port_return'    : port_return,
        'port_volatility': port_volatility,
        'sharpe_ratio'   : sharpe,
        'port_variance'  : port_variance,
    }


# ── Display helper ─────────────────────────────────────────────────────────────

def display_metrics(tickers: list,
                    weights: np.ndarray,
                    exp_returns: pd.Series,
                    cov_mat: pd.DataFrame,
                    label: str = 'Portfolio') -> pd.DataFrame:
    """
    Print formatted portfolio summary with allocation table.

    Args:
        tickers     : List of ticker symbols
        weights     : Portfolio weights array
        exp_returns : Annualized expected returns
        cov_mat     : Annualized covariance matrix
        label       : Portfolio name for display

    Returns:
        DataFrame of allocation table
    """
    stats = portfolio_stats(weights, exp_returns, cov_mat)

    print(f"\n{'='*45}")
    print(f"  {label}")
    print(f"{'='*45}")
    print(f"  Expected Return    : {stats['port_return']:>8.2%}")
    print(f"  Volatility (Risk)  : {stats['port_volatility']:>8.2%}")
    print(f"  Sharpe Ratio       : {stats['sharpe_ratio']:>8.3f}")
    print(f"{'='*45}")

    alloc = pd.DataFrame({
        'Ticker'    : tickers,
        'Weight'    : [f"{w:.1%}" for w in weights],
        'Exp Return': [f"{r:.1%}" for r in exp_returns.values],
    })
    print(alloc.to_string(index=False))
    return alloc


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    from data_loader import get_db_summary
    START = '2021-01-01'
    END   = get_db_summary()['end_date'].max()
    N     = len(VN30_TICKERS)

    print("Computing expected returns and covariance matrix...")
    mu  = expected_returns(VN30_TICKERS, START, END)
    cov = covariance_matrix(VN30_TICKERS, START, END)

    # Test with equal weights
    w_equal = np.array([1/N] * N)
    display_metrics(VN30_TICKERS, w_equal, mu, cov, label='Equal Weights (1/30 each)')