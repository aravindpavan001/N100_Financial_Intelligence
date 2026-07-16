import sqlite3
import pandas as pd

from composite_score import calculate_quality_score

conn = sqlite3.connect("nifty100.db")

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

df["composite_quality_score"] = df.apply(
    lambda row: calculate_quality_score(
        row["return_on_equity_pct"],
        row["net_profit_margin_pct"],
        row["revenue_cagr_5yr"],
        row["pat_cagr_5yr"],
        row["debt_to_equity"],
    ),
    axis=1,
)

df.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False,
)

conn.close()

print(df[
    [
        "company_id",
        "year",
        "composite_quality_score"
    ]
].head())