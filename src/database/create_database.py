import sqlite3
from pathlib import Path

# ==========================================
# Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "nifty100.db"
SCHEMA_PATH = BASE_DIR / "src" / "database" / "schema.sql"

print("Database Path:", DB_PATH)
print("Schema Path:", SCHEMA_PATH)

# ==========================================
# Delete old database (if it exists)
# ==========================================

if DB_PATH.exists():
    DB_PATH.unlink()
    print("Old database deleted.")

# ==========================================
# Create new database
# ==========================================

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ==========================================
# Read schema
# ==========================================

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    schema = f.read()

# ==========================================
# Execute one statement at a time
# ==========================================

statements = [s.strip() for s in schema.split(";") if s.strip()]

for i, statement in enumerate(statements, start=1):
    try:
        print(f"\nExecuting statement {i}...")
        cursor.execute(statement)
    except Exception as e:
        print("\nERROR FOUND!")
        print("=" * 60)
        print(statement)
        print("=" * 60)
        print(e)
        conn.close()
        raise

conn.commit()
conn.close()

print("\nDatabase created successfully!")