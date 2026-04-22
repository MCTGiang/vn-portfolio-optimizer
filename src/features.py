"""
features.py
Calculates financial features from OHLCV price data.
Used as input for portfolio optimization in portfolio_metrics.py.

Key outputs:
    - Daily simple returns (used for Covariance Matrix and MPT)
    - Daily log returns (used for statistical analysis)
    - Annualized return and volatility per ticker
    - Returns matrix for all tickers (N days x M tickers)
"""

import numpy as np
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from data_loader import load_from_db, VN30_TICKERS, get_db_summary

# ── Constants ──────────────────────────────────────────────────────────────────

TRADING_DAYS = 252    # approximate VN market trading days per year


# ── Single ticker functions ────────────────────────────────────────────────────

def calc_returns(df: pd.DataFrame,
                 price_col: str = 'Close') -> pd.Series:
    """
    Calculate daily simple returns from price series.

    Formula: r_t = (P_t - P_{t-1}) / P_{t-1}

    Used for: Covariance Matrix, portfolio_stats(), MPT optimization.
    NOT suitable for: multi-period compounding across time.

    Args:
        df        : DataFrame with DatetimeIndex and price column
        price_col : Column name to use (default: 'Close')

    Returns:
        Series of daily simple returns, first row is NaN (dropped by callers)
    """
    return df[price_col].pct_change()


def calc_log_returns(df: pd.DataFrame,
                     price_col: str = 'Close') -> pd.Series:
    """
    Calculate daily log returns from price series.

    Formula: r_t = ln(P_t / P_{t-1})

    Used for: statistical analysis, normality testing, descriptive stats.
    NOT used for: portfolio weights calculation in MPT.

    Args:
        df        : DataFrame with DatetimeIndex and price column
        price_col : Column name to use (default: 'Close')

    Returns:
        Series of daily log returns, first row is NaN
    """
    return np.log(df[price_col] / df[price_col].shift(1))


def annualized_return(returns: pd.Series) -> float:
    """
    Annualize mean daily simple return.

    Formula: E[r] * 252

    Args:
        returns: Series of daily simple returns (NaN dropped internally)

    Returns:
        Float — annualized return, e.g. 0.089 means 8.9% per year
    """
    return returns.dropna().mean() * TRADING_DAYS


def annualized_volatility(returns: pd.Series) -> float:
    """
    Annualize daily return volatility (standard deviation).

    Formula: std(r) * sqrt(252)

    Volatility scales with square root of time — based on
    Brownian Motion assumption underlying MPT.

    Args:
        returns: Series of daily simple returns

    Returns:
        Float — annualized volatility, e.g. 0.256 means 25.6% per year
    """
    return returns.dropna().std() * np.sqrt(TRADING_DAYS)


def ticker_stats(ticker: str,
                 start: str,
                 end: str) -> dict:
    """
    Compute annualized return and volatility for one ticker.

    Args:
        ticker : Stock ticker symbol (e.g. 'VCB')
        start  : Start date 'YYYY-MM-DD'
        end    : End date 'YYYY-MM-DD'

    Returns:
        dict with keys: ticker, ann_return, ann_volatility, n_days
    """
    df = load_from_db(ticker, start, end)
    ret = calc_returns(df).dropna()
    return {
        'ticker'        : ticker,
        'ann_return'    : annualized_return(ret),
        'ann_volatility': annualized_volatility(ret),
        'n_days'        : len(ret),
    }


# ── Multi-ticker matrix ────────────────────────────────────────────────────────

def build_returns_matrix(tickers: list,
                         start: str,
                         end: str,
                         method: str = 'simple') -> pd.DataFrame:
    """
    Build a returns matrix for multiple tickers.

    Shape: (N trading days) x (M tickers)
    First row dropped (NaN from pct_change).
    Only dates present in ALL tickers are kept (inner join).

    Args:
        tickers : List of ticker symbols
        start   : Start date 'YYYY-MM-DD'
        end     : End date 'YYYY-MM-DD'
        method  : 'simple' (default, for MPT) or 'log' (for analysis)

    Returns:
        DataFrame — rows = dates, columns = tickers, values = daily returns
    """
    frames = {}
    for ticker in tickers:
        df = load_from_db(ticker, start, end)
        if method == 'log':
            frames[ticker] = calc_log_returns(df)
        else:
            frames[ticker] = calc_returns(df)

    matrix = pd.DataFrame(frames)
    matrix.dropna(inplace=True)   # drop first row (NaN) + any misaligned dates
    return matrix


def all_ticker_stats(tickers: list,
                     start: str,
                     end: str) -> pd.DataFrame:
    """
    Compute annualized return and volatility for all tickers.

    Args:
        tickers : List of ticker symbols
        start   : Start date 'YYYY-MM-DD'
        end     : End date 'YYYY-MM-DD'

    Returns:
        DataFrame sorted by annualized return descending
    """
    rows = [ticker_stats(t, start, end) for t in tickers]
    df = pd.DataFrame(rows)
    df['ann_return_pct']    = (df['ann_return']     * 100).round(2)
    df['ann_volatility_pct'] = (df['ann_volatility'] * 100).round(2)
    return df.sort_values('ann_return', ascending=False).reset_index(drop=True)


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    from data_loader import get_db_summary
    START = '2021-01-01'
    END   = get_db_summary()['end_date'].max()

    print("Building returns matrix for VN30 tickers...")
    matrix = build_returns_matrix(VN30_TICKERS, START, END)
    print(f"Returns matrix shape: {matrix.shape}")
    print(f"Date range: {matrix.index[0].date()} → {matrix.index[-1].date()}")
    print(matrix.head(3).round(4))

    print("\nComputing annualized stats...")
    stats = all_ticker_stats(VN30_TICKERS, START, END)
    print(stats[['ticker', 'ann_return_pct',
                 'ann_volatility_pct', 'n_days']].to_string(index=False))