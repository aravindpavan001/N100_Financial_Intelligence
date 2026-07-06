import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

companies = [
    "TCS",
    "INFY",
    "RELIANCE",
    "HDFCBANK",
    "ITC",
]

for company in companies:

    print("=" * 80)
    print(company)
    print("=" * 80)

    query = f"""
    SELECT
        company_id,
        year,
        net_profit_margin_pct,
        return_on_equity_pct,
        debt_to_equity,
        interest_coverage,
        asset_turnover,
        free_cash_flow_cr,
        revenue_cagr_5yr,
        pat_cagr_5yr,
        eps_cagr_5yr
    FROM financial_ratios
    WHERE company_id='{company}'
    ORDER BY year;
    """

    print(pd.read_sql(query, conn))

conn.close()