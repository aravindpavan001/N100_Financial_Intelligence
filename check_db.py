import sqlite3

conn = sqlite3.connect("nifty100.db")

cursor = conn.cursor()

print("=" * 80)
print("FINANCIAL_RATIOS SCHEMA")
print("=" * 80)

cursor.execute("PRAGMA table_info(financial_ratios)")

for row in cursor.fetchall():
    print(row)

conn.close()