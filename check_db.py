import sqlite3

conn = sqlite3.connect("nifty100.db")

cursor = conn.cursor()

print("=" * 70)
print("SECTORS TABLE")
print("=" * 70)

cursor.execute("PRAGMA table_info(sectors)")

for row in cursor.fetchall():
    print(row)

conn.close()