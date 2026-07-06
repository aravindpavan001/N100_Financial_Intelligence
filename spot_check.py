import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

company = "ABB"

query = """
SELECT
    p.company_id,
    p.year,
    p.net_profit,
    b.equity_capital,
    b.reserves
FROM profitandloss p
JOIN balancesheet b
ON p.company_id=b.company_id
AND p.year=b.year
WHERE p.company_id='ABB'
LIMIT 5
"""

df = pd.read_sql(query, conn)

df["Manual_ROE"] = (
    df["net_profit"] /
    (df["equity_capital"] + df["reserves"])
) * 100

print(df)

conn.close()