import time

from fastapi import APIRouter

from src.api.database import get_db_connection

router = APIRouter(tags=["Health"])

START_TIME = time.time()

VERSION = "1.0.0"


@router.get("/health")
def health():

    conn = get_db_connection()

    cursor = conn.cursor()

    tables = [
        "companies",
        "analysis",
        "balancesheet",
        "cashflow",
        "financial_ratios",
        "market_cap",
        "peer_groups",
        "profitandloss",
        "sectors",
        "stock_prices",
    ]

    counts = {}

    for table in tables:

        cursor.execute(f"SELECT COUNT(*) FROM {table}")

        counts[table] = cursor.fetchone()[0]

    conn.close()

    return {
        "status": "ok",
        "db_row_counts": counts,
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "version": VERSION,
    }
