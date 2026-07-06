import sqlite3

conn = sqlite3.connect("nifty100.db")
cursor = conn.cursor()

new_columns = [
    ("revenue_cagr_5yr", "REAL"),
    ("pat_cagr_5yr", "REAL"),
    ("eps_cagr_5yr", "REAL"),
    ("composite_quality_score", "REAL"),
]

cursor.execute("PRAGMA table_info(financial_ratios)")
existing_columns = [row[1] for row in cursor.fetchall()]

for column_name, column_type in new_columns:
    if column_name not in existing_columns:
        cursor.execute(
            f"ALTER TABLE financial_ratios ADD COLUMN {column_name} {column_type}"
        )
        print(f"Added column: {column_name}")
    else:
        print(f"Column already exists: {column_name}")

conn.commit()
conn.close()

print("\nfinancial_ratios schema updated successfully.")