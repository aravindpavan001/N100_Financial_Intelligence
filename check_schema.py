import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

print(pd.read_sql(
    "SELECT * FROM peer_groups LIMIT 10",
    conn
))

conn.close()