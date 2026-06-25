import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE = BASE_DIR / "nifty100.db"

conn = sqlite3.connect(DATABASE)

conn.execute("PRAGMA foreign_keys = ON")

print("Database connection established.")