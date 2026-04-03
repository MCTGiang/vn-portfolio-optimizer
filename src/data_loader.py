"""
data_loader.py
ETL pipeline for VN stock market data using yfinance.
Fetches OHLCV data and stores in local SQLite database.
"""

import sqlite3
import os
import pandas as pd
import yfinance as yf
from datetime import datetime

# ── Configuration ────────────────────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'portfolio.db')

VN30_TICKERS = [
    'VCB.VN', 'VNM.VN', 'HPG.VN', 'FPT.VN', 'MWG.VN',
    'VIC.VN', 'GAS.VN', 'BID.VN', 'CTG.VN', 'TCB.VN'
]

# ── Database helpers ──────────────────────────────────────────────────────────

def get_connection() -> sqlite3.Connection:
    """Return a SQLite connection, creating the DB file if needed."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_table() -> None:
    """Create Stock_Prices table if it does not exist."""
    conn = get_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Stock_Prices (
            Ticker  TEXT NOT NULL,
            Date    TEXT NOT NULL,
            Open    REAL,
            High    REAL,
            Low     REAL,
            Close   REAL,
            Volume  INTEGER,
            PRIMARY KEY (Ticker, Date)
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Table Stock_Prices ready")


# ── Fetch & insert ────────────────────────────────────────────────────────────

def fetch_ticker(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    Download OHLCV data from Yahoo Finance.

    Args:
        ticker: Yahoo Finance ticker symbol (e.g. 'VCB.VN')
        start:  Start date 'YYYY-MM-DD'
        end:    End date   'YYYY-MM-DD'

    Returns:
        Cleaned DataFrame with columns [Ticker, Date, Open, High, Low, Close, Volume]
    """
    df = yf.download(ticker, start=start, end=end,
                     auto_adjust=False, progress=False)

    if df.empty:
        print(f"⚠️  No data returned for {ticker}")
        return pd.DataFrame()

    # Flatten multi-level columns
    df.columns = [col[0] if isinstance(col, tuple) else col
                  for col in df.columns]

    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    df.index.name = 'Date'
    df.reset_index(inplace=True)
    df['Date']   = df['Date'].astype(str)
    df['Ticker'] = ticker.replace('.VN', '')   # store as 'VCB', not 'VCB.VN'
    df['Volume'] = df['Volume'].fillna(0).astype(int)

    return df[['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']]


def insert_to_db(df: pd.DataFrame) -> int:
    """
    Insert DataFrame rows into Stock_Prices, skipping duplicates.

    Returns:
        Number of rows inserted.
    """
    if df.empty:
        return 0

    conn = get_connection()
    inserted = 0
    for _, row in df.iterrows():
        try:
            conn.execute('''
                INSERT OR IGNORE INTO Stock_Prices
                (Ticker, Date, Open, High, Low, Close, Volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', tuple(row))
            inserted += 1
        except Exception as e:
            print(f"⚠️  Insert error: {e}")
    conn.commit()
    conn.close()
    return inserted


# ── Load from DB ──────────────────────────────────────────────────────────────

def load_from_db(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    Load historical prices from SQLite.

    Args:
        ticker: Ticker without suffix (e.g. 'VCB')
        start:  Start date 'YYYY-MM-DD'
        end:    End date   'YYYY-MM-DD'

    Returns:
        DataFrame indexed by Date with columns [Open, High, Low, Close, Volume]
    """
    conn = get_connection()
    query = '''
        SELECT Date, Open, High, Low, Close, Volume
        FROM   Stock_Prices
        WHERE  Ticker = ?
          AND  Date  >= ?
          AND  Date  <= ?
        ORDER  BY Date
    '''
    df = pd.read_sql_query(query, conn, params=(ticker, start, end))
    conn.close()

    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df


def get_all_tickers() -> list:
    """Return list of all unique tickers stored in DB."""
    conn = get_connection()
    cursor = conn.execute('SELECT DISTINCT Ticker FROM Stock_Prices ORDER BY Ticker')
    tickers = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tickers


# ── Full pipeline ─────────────────────────────────────────────────────────────

def update_db(tickers: list = VN30_TICKERS,
              start: str = '2021-01-01',
              end: str = None) -> None:
    """
    Fetch and store data for a list of tickers.

    Args:
        tickers: List of Yahoo Finance ticker symbols
        start:   Start date 'YYYY-MM-DD'
        end:     End date (defaults to today)
    """
    if end is None:
        end = datetime.today().strftime('%Y-%m-%d')

    create_table()
    print(f"\n📥 Fetching {len(tickers)} tickers from {start} to {end}\n")

    for ticker in tickers:
        df = fetch_ticker(ticker, start, end)
        n  = insert_to_db(df)
        label = ticker.replace('.VN', '')
        print(f"  {label:6s} → {n:4d} rows inserted")

    print(f"\n✅ Done. Tickers in DB: {get_all_tickers()}")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    update_db()