import sqlite3
from pathlib import Path

# ==========================================
# Project Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "nifty100.db"

SCHEMA_PATH = BASE_DIR / "src" / "database" / "schema.sql"

# ==========================================
# Create Database
# ==========================================

connection = sqlite3.connect(DB_PATH)

cursor = connection.cursor()

# ==========================================
# Run Schema
# ==========================================

with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
    schema = file.read()

cursor.executescript(schema)

connection.commit()

print("Database created successfully!")

connection.close()