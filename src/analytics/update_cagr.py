import sqlite3
import pandas as pd
from pathlib import Path

from cagr import calculate_cagr

# ------------------------------------
# Database
# ------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "nifty100.db"

conn = sqlite3.connect(DB_PATH)

# ------------------------------------
# Load Tables
# ------------------------------------

pl = pd.read_sql("SELECT * FROM profitandloss", conn)

ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)

# ------------------------------------
# Convert year to sortable integer
# ------------------------------------

pl["year_num"] = pd.to_numeric(
    pl["year"].str.extract(r"(\d{4})")[0],
    errors="coerce"
)

pl = pl.dropna(subset=["year_num"])

pl["year_num"] = pl["year_num"].astype(int)
pl = pl.sort_values(["company_id", "year_num"])

# ------------------------------------
# Create new columns
# ------------------------------------

ratios["revenue_cagr_5yr"] = None
ratios["pat_cagr_5yr"] = None

# ------------------------------------
# Calculate CAGR company-wise
# ------------------------------------

for company in pl["company_id"].unique():

    company_df = pl[
        pl["company_id"] == company
    ].sort_values("year_num")

    if len(company_df) < 5:
        continue

    start_sales = company_df.iloc[0]["sales"]
    end_sales = company_df.iloc[-1]["sales"]

    start_pat = company_df.iloc[0]["net_profit"]
    end_pat = company_df.iloc[-1]["net_profit"]

    revenue_cagr, revenue_flag = calculate_cagr(
    start_sales,
    end_sales,
    len(company_df) - 1
)

    pat_cagr, pat_flag = calculate_cagr(
    start_pat,
    end_pat,
    len(company_df) - 1
     )

    latest_year = company_df.iloc[-1]["year"]

    print("=" * 60)
    print(company)

    print("Start Sales :", start_sales)
    print("End Sales   :", end_sales)

    print("Start PAT   :", start_pat)
    print("End PAT     :", end_pat)

    print("Revenue CAGR :", revenue_cagr)
    print("Revenue Flag :", revenue_flag)

    print("PAT CAGR     :", pat_cagr)
    print("PAT Flag     :", pat_flag)

    print("Latest Year  :", latest_year)

    mask = (
        (ratios["company_id"] == company)
        &
        (ratios["year"] == latest_year)
        )
    
    print("Rows Matched :", mask.sum())

    ratios.loc[mask, "revenue_cagr_5yr"] = revenue_cagr
    ratios.loc[mask, "pat_cagr_5yr"] = pat_cagr

# ------------------------------------
# Save back to SQLite
# ------------------------------------

ratios.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("=" * 50)
print("CAGR UPDATED")
print("=" * 50)

print(
    ratios.loc[
        ratios["company_id"] == "ABB",
        [
            "company_id",
            "year",
            "revenue_cagr_5yr",
            "pat_cagr_5yr"
        ]
    ]
)