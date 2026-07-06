import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

print(pd.read_sql(
    "SELECT COUNT(*) AS rows FROM financial_ratios",
    conn,
))

print(pd.read_sql(
    """
    SELECT
        COUNT(return_on_equity_pct) roe,
        COUNT(debt_to_equity) de,
        COUNT(asset_turnover) asset_turnover,
        COUNT(free_cash_flow_cr) fcf,
        COUNT(revenue_cagr_5yr) revenue_cagr
    FROM financial_ratios
    """,
    conn,
))

conn.close()