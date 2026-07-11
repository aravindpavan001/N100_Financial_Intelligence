import sqlite3

conn = sqlite3.connect(
    "nifty100.db",
)

cursor = conn.cursor()

cursor.execute("""
SELECT *
FROM peer_percentiles
WHERE peer_group_name='FMCG'
AND metric='return_on_equity_pct'
ORDER BY percentile_rank DESC
LIMIT 10;
""")

print(cursor.fetchone())

conn.close()