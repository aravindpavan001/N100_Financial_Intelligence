import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

companies = pd.read_sql("SELECT * FROM companies", conn)
ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
market = pd.read_sql("SELECT * FROM market_cap", conn)

conn.close()

print("Companies:", len(companies))
print("Financial Ratios:", len(ratios))
print("Market Cap:", len(market))