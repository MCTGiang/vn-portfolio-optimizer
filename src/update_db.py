"""
update_db.py
Standalone script to update SQLite database with latest stock prices.

Usage:
  python src/update_db.py                        # update all VN30 tickers
  python src/update_db.py --tickers VCB BID FPT  # update specific tickers
  python src/update_db.py --replace              # clear and re-fetch all data
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(__file__))
from data_loader import update_db, get_db_summary, VN30_TICKERS


def main():
    parser = argparse.ArgumentParser(
        description='Update VN Portfolio Optimizer stock price database'
    )
    parser.add_argument(
        '--tickers', nargs='+', default=None,
        help='Specific tickers to update (default: all 30 VN30 tickers)'
    )
    parser.add_argument(
        '--start', default='2021-01-01',
        help='Start date YYYY-MM-DD (default: 2021-01-01)'
    )
    parser.add_argument(
        '--replace', action='store_true',
        help='Delete existing data before inserting'
    )
    args = parser.parse_args()

    tickers = args.tickers if args.tickers else VN30_TICKERS

    print("=" * 55)
    print("  VN Portfolio Optimizer — Database Update")
    print("=" * 55)
    print(f"  Tickers : {len(tickers)} stocks")
    print(f"  Start   : {args.start}")
    print(f"  Replace : {args.replace}")
    print("=" * 55 + "\n")

    update_db(tickers=tickers, start=args.start, replace=args.replace)

    print("\n" + "=" * 55)
    print("  Final DB Summary:")
    print("=" * 55)
    print(get_db_summary().to_string(index=False))


if __name__ == '__main__':
    main()