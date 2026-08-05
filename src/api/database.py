import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "nifty100.db"


def get_db_connection():

    try:

        conn = sqlite3.connect(DB_PATH)

        conn.row_factory = sqlite3.Row

        return conn

    except sqlite3.Error as e:

        print(f"Database Error : {e}")

        raise


def close_connection(conn):

    if conn:

        conn.close()
