import pandas as pd
from fastapi import APIRouter, HTTPException

from src.api.database import get_db_connection

router = APIRouter(tags=["Valuation"])

# ==========================================================
# LOAD TABLES
# ==========================================================


def load_table(table_name):

    conn = get_db_connection()

    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

    conn.close()

    return df


market_cap = load_table("market_cap")

companies = load_table("companies")


# ==========================================================
# MARKET CAP HISTORY
# ==========================================================


@router.get("/market-cap/{ticker}")
def get_market_cap(ticker: str):

    ticker = ticker.upper()

    company = companies[companies["id"] == ticker]

    if company.empty:

        raise HTTPException(status_code=404, detail="Company not found.")

    history = market_cap[market_cap["company_id"] == ticker].copy()

    if history.empty:

        raise HTTPException(status_code=404, detail="Market cap history not found.")

    history = history.sort_values("year")

    output = history[
        [
            "year",
            "market_cap_crore",
            "enterprise_value_crore",
            "pe_ratio",
            "pb_ratio",
            "ev_ebitda",
            "dividend_yield_pct",
        ]
    ]

    output = output.astype(object)

    output = output.where(pd.notnull(output), None)

    return {
        "ticker": ticker,
        "company_name": company.iloc[0]["company_name"],
        "history": output.to_dict(orient="records"),
    }
