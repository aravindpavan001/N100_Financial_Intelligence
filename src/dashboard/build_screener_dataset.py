import os
import sqlite3
import pandas as pd

# -----------------------------
# Connect to SQLite
# -----------------------------
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "nifty100.db"

conn = sqlite3.connect(DB_PATH)

companies = pd.read_sql("SELECT * FROM companies", conn)
ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
market = pd.read_sql("SELECT * FROM market_cap", conn)

conn.close()

# -----------------------------
# Convert financial year to numeric
# Example: "Mar 2024" -> 2024
# -----------------------------
ratios["year_num"] = ratios["year"].str[-4:].astype(int)

# -----------------------------
# Keep latest financial ratio per company
# -----------------------------
ratios = (
    ratios.sort_values("year_num")
          .drop_duplicates(subset="company_id", keep="last")
)

# -----------------------------
# Keep latest market data per company
# -----------------------------
market = (
    market.sort_values("year")
          .drop_duplicates(subset="company_id", keep="last")
)

print("Companies:", len(companies))
print("Latest Ratios:", len(ratios))
print("Latest Market:", len(market))

# -----------------------------
# Missing companies
# -----------------------------
missing = set(companies["id"]) - set(ratios["company_id"])

print("\nMissing Companies:")
print(missing)

# -----------------------------
# Merge all datasets
# -----------------------------
df = companies.merge(
    ratios,
    left_on="id",
    right_on="company_id",
    how="left",
    suffixes=("_company", "_ratio")
)

df = df.merge(
    market,
    left_on="id_company",
    right_on="company_id",
    how="left",
    suffixes=("", "_market")
)


print("\nFinal Dataset Shape:")
print(df.shape)

# -----------------------------
# Save dataset
# -----------------------------
os.makedirs("output", exist_ok=True)

output_path = "output/screener_dataset.csv"

df.to_csv(output_path, index=False)

print("\nDataset saved successfully!")
print(f"Saved to: {output_path}")

print("\nFirst 5 rows:")
print(df.head())

print("\nFinal Dataset Shape:")
print(df.shape)

import os

os.makedirs("output", exist_ok=True)

df.to_csv("output/screener_dataset.csv", index=False)

print("\nDataset saved successfully!")
print(df.head())