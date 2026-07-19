import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

companies = pd.read_sql("SELECT * FROM companies", conn)

ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)

market_cap = pd.read_sql("SELECT * FROM market_cap", conn)

peer_groups = pd.read_sql("SELECT * FROM peer_groups", conn)

print("Companies")
print(companies.columns.tolist())

print()

print("Ratios")
print(ratios.columns.tolist())

print()

print("Market Cap")
print(market_cap.columns.tolist())

print()

print("Peer Groups")
print(peer_groups.columns.tolist())

# Latest market cap record for each company
market_latest = (
    market_cap.sort_values("year")
    .groupby("company_id", as_index=False)
    .last()
)

# Latest financial ratios for each company
ratios_latest = (
    ratios.sort_values("year")
    .groupby("company_id", as_index=False)
    .last()
)

# Start with companies
valuation = companies.copy()

# Add peer group
valuation = valuation.merge(
    peer_groups[["company_id", "peer_group_name"]],
    left_on="id",
    right_on="company_id",
    how="left"
).drop(columns=["company_id"])

# Add market cap
valuation = valuation.merge(
    market_latest,
    left_on="id",
    right_on="company_id",
    how="left",
    suffixes=("", "_market")
).drop(columns=["company_id"])

# Add financial ratios
valuation = valuation.merge(
    ratios_latest,
    left_on="id",
    right_on="company_id",
    how="left",
    suffixes=("", "_ratio")
).drop(columns=["company_id"])

print("Rows:", len(valuation))

print(
    valuation[
        [
            "company_name",
            "peer_group_name",
            "market_cap_crore",
            "pe_ratio",
            "pb_ratio",
            "ev_ebitda",
            "free_cash_flow_cr"
        ]
    ].head()
)

# ----------------------------
# Valuation Metrics
# ----------------------------

valuation["fcf_yield_pct"] = (
    valuation["free_cash_flow_cr"] /
    valuation["market_cap_crore"]
) * 100

peer_pe = (
    valuation.groupby("peer_group_name")["pe_ratio"]
    .median()
    .reset_index()
    .rename(columns={"pe_ratio": "peer_median_pe"})
)

valuation = valuation.merge(
    peer_pe,
    on="peer_group_name",
    how="left"
)

valuation["pe_vs_peer_pct"] = (
    (valuation["pe_ratio"] - valuation["peer_median_pe"])
    / valuation["peer_median_pe"]
) * 100

def valuation_flag(x):
    if pd.isna(x):
        return "Unknown"

    if x >= 20:
        return "Premium"

    elif x <= -20:
        return "Discount"

    else:
        return "Fair"


valuation["valuation_flag"] = valuation["pe_vs_peer_pct"].apply(
    valuation_flag
)

print()

print(
    valuation[
        [
            "company_name",
            "pe_ratio",
            "peer_median_pe",
            "pe_vs_peer_pct",
            "valuation_flag",
            "fcf_yield_pct",
        ]
    ].head(10)
)

output = valuation[
    [
        "company_name",
        "peer_group_name",
        "market_cap_crore",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "free_cash_flow_cr",
        "fcf_yield_pct",
        "peer_median_pe",
        "pe_vs_peer_pct",
        "valuation_flag",
    ]
]

output.to_excel(
    OUTPUT_DIR / "valuation_summary.xlsx",
    index=False
)

output.to_csv(
    OUTPUT_DIR / "valuation_flags.csv",
    index=False
)

print()

print("Valuation Summary exported successfully.")

print(OUTPUT_DIR / "valuation_summary.xlsx")

print(OUTPUT_DIR / "valuation_flags.csv")