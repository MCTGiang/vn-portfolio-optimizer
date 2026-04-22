"""
data_loader.py
ETL pipeline for VN stock market data.
Primary source : vnstock KBSQuote (accurate VND prices, exact date range)
Fallback source: yfinance
"""

import sqlite3
import os
import time
import pandas as pd
from datetime import datetime

# ── Configuration ──────────────────────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'portfolio.db')

# Update VN30 21/04/2026 - Remove VPL due to new listed date 13-May-2025 can cause Cov matrix error in optimizer
VN30_TICKERS = [
    'ACB', 'BID', 'CTG', 'DGC', 'FPT',
    'GAS', 'GVR', 'HDB', 'HPG', 'LPB',
    'MBB', 'MSN', 'MWG', 'PLX', 'SAB',
    'SHB', 'SSB', 'SSI', 'STB', 'TCB',
    'TPB', 'VCB', 'VHM', 'VIB', 'VIC',
    'VJC', 'VNM', 'VPB', 'VPL', 'VRE',
]

# ── Database helpers ───────────────────────────────────────────────────────────

def get_connection() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_table() -> None:
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


# ── Fetch: vnstock KBS (primary) ─────────────────────────────────────────────

def fetch_ticker_kbs(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    Fetch OHLCV from KBS via vnstock.
    """
    try:
        from vnstock import Vnstock
        stock = Vnstock().stock(symbol=ticker, source='KBS')
        df = stock.quote.history(start=start, end=end, interval='1D')
        if df.empty:
            print(f"  ⚠️  vnstock trả về rỗng cho {ticker} (Nguồn: KBS)")
            return pd.DataFrame()

        out = pd.DataFrame({
            'Ticker': ticker,
            'Date'  : pd.to_datetime(df['time']).dt.strftime('%Y-%m-%d'),
            'Open'  : df['open'].astype(float),
            'High'  : df['high'].astype(float),
            'Low'   : df['low'].astype(float),
            'Close' : df['close'].astype(float),
            'Volume': df['volume'].fillna(0).astype(int),
        })
        time.sleep(4)
        return out

    except Exception as e:
        import traceback
        print(f"  ⚠️  LỖI NGHIÊM TRỌNG TỪ VNSTOCK [{ticker}]:")
        traceback.print_exc()
        return pd.DataFrame()


# ── Fetch: yfinance (fallback) ─────────────────────────────────────────────────

def fetch_ticker_yfinance(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Fallback using yfinance. Prices are adjusted — less accurate."""
    try:
        import yfinance as yf
        df = yf.download(ticker + '.VN', start=start, end=end,
                         auto_adjust=False, progress=False)
        if df.empty:
            return pd.DataFrame()

        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        df.index.name = 'Date'
        df = df.reset_index()

        return pd.DataFrame({
            'Ticker': ticker,
            'Date'  : df['Date'].astype(str),
            'Open'  : df['Open'].astype(float),
            'High'  : df['High'].astype(float),
            'Low'   : df['Low'].astype(float),
            'Close' : df['Close'].astype(float),
            'Volume': df['Volume'].fillna(0).astype(int),
        })
    except Exception as e:
        print(f"  ⚠️  yfinance error [{ticker}]: {type(e).__name__}: {str(e)[:80]}")
        return pd.DataFrame()


# ── Smart fetch with fallback ──────────────────────────────────────────────────

def fetch_ticker(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Try KBS first, fall back to yfinance if KBS returns empty."""
    df = fetch_ticker_kbs(ticker, start, end)
    if df.empty:
        print(f"  → Fallback to yfinance for {ticker}")
        df = fetch_ticker_yfinance(ticker, start, end)
    return df


# ── Insert to DB ───────────────────────────────────────────────────────────────

def insert_to_db(df: pd.DataFrame) -> int:
    """Insert rows, skip duplicates. Returns number of new rows inserted."""
    if df.empty:
        return 0
    conn = get_connection()
    cursor = conn.executemany(
        '''INSERT OR IGNORE INTO Stock_Prices
           (Ticker, Date, Open, High, Low, Close, Volume)
           VALUES (?, ?, ?, ?, ?, ?, ?)''',
        df[['Ticker','Date','Open','High','Low','Close','Volume']].values.tolist()
    )
    inserted = cursor.rowcount
    conn.commit()
    conn.close()
    return inserted


# ── Load from DB ───────────────────────────────────────────────────────────────

def load_from_db(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    Load OHLCV from SQLite for one ticker.
    Returns DataFrame indexed by Date.
    """
    conn  = get_connection()
    query = '''
        SELECT Date, Open, High, Low, Close, Volume
        FROM   Stock_Prices
        WHERE  Ticker = ? AND Date >= ? AND Date <= ?
        ORDER  BY Date
    '''
    df = pd.read_sql_query(query, conn, params=(ticker, start, end))
    conn.close()
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df


def get_all_tickers() -> list:
    conn    = get_connection()
    cursor  = conn.execute('SELECT DISTINCT Ticker FROM Stock_Prices ORDER BY Ticker')
    tickers = [r[0] for r in cursor.fetchall()]
    conn.close()
    return tickers


def get_db_summary() -> pd.DataFrame:
    """Return row count and date range per ticker."""
    conn  = get_connection()
    query = '''
        SELECT Ticker,
               COUNT(*)  AS rows,
               MIN(Date) AS start_date,
               MAX(Date) AS end_date
        FROM   Stock_Prices
        GROUP  BY Ticker
        ORDER  BY Ticker
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    # Total tickets and rows in DB 
    total_tickers = len(df)
    total_rows = df['rows'].sum()
    
    # Hiển thị thông tin ra console
    print("-" * 45)
    print(f"No. Tickers : {total_tickers}")
    print(f"No. Rows    : {total_rows:,}")
    print("-" * 45)
    return df


# ── Full pipeline ──────────────────────────────────────────────────────────────

def update_db(tickers: list = None,
              start: str = '2021-01-01',
              end: str = None,
              replace: bool = False) -> None:
    """
    Fetch and store OHLCV for a list of tickers.

    Args:
        tickers : List of VN tickers. Defaults to VN30_TICKERS.
        start   : Start date 'YYYY-MM-DD'. Default '2021-01-01'.
        end     : End date. Defaults to today.
        replace : If True, delete existing rows before inserting.
    """
    if tickers is None:
        tickers = VN30_TICKERS
    if end is None:
        end = datetime.today().strftime('%Y-%m-%d')

    create_table()

    if replace:
        conn = get_connection()
        placeholders = ','.join('?' * len(tickers))
        conn.execute(
            f'DELETE FROM Stock_Prices WHERE Ticker IN ({placeholders})', tickers
        )
        conn.commit()
        conn.close()
        print(f"🗑️  Cleared existing rows for: {tickers}\n")

    print(f"📥 Fetching {len(tickers)} tickers | {start} → {end}")
    print(f"   Source: vnstock KBS (fallback: yfinance)\n")

    total = 0
    for ticker in tickers:
        df     = fetch_ticker(ticker, start, end)
        n      = insert_to_db(df)
        total += n
        icon   = '✅' if n > 0 else '⚠️ '
        print(f"  {icon} {ticker:5s} → {n:5,} rows")

    print(f"\n✅ Done. Total new rows: {total:,}")
    print("\n📊 DB Summary:")
    print(get_db_summary().to_string(index=False))


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    update_db()