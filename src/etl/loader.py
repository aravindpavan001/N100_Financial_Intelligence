import sqlite3
import pandas as pd
from pathlib import Path

# ==========================================
# Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data" / "raw"

OUTPUT_DIR = BASE_DIR / "output"

DATABASE = BASE_DIR / "nifty100.db"

print(DATABASE)

# ==========================================
# Database Connection
# ==========================================

conn = sqlite3.connect(DATABASE)

conn.execute("PRAGMA foreign_keys = ON")

print("Connected to SQLite database.")

# ==========================================
# Load Audit
# ==========================================

audit = []

def add_audit(table_name, rows_loaded, rejected_rows, status):

    audit.append({
        "table_name": table_name,
        "rows_loaded": rows_loaded,
        "rejected_rows": rejected_rows,
        "status": status
    })


companies = pd.read_excel(
    DATA_DIR / "companies.xlsx",
    header=1
)

print(companies.head())

# ==========================================
# Insert into SQLite
# ==========================================

companies.to_sql(
    "companies",
    conn,
    if_exists="append",
    index=False
)

print("\nCompanies inserted successfully!")

add_audit(
    "companies",
    len(companies),
    0,
    "Success"
)

# ==========================================
# Load Sectors
# ==========================================

sectors = pd.read_excel(
    DATA_DIR / "sectors.xlsx"
)

print(sectors.head())

sectors.to_sql(
    "sectors",
    conn,
    if_exists="append",
    index=False
)

print("\nSectors inserted successfully!")

add_audit(
    "sectors",
    len(sectors),
    0,
    "Success"
)


analysis = pd.read_excel(
    DATA_DIR / "analysis.xlsx",
    header=1
)

analysis = analysis[
    analysis["company_id"].isin(companies["id"])
]

analysis.to_sql(
    "analysis",
    conn,
    if_exists="append",
    index=False
)

print("Analysis inserted successfully!")

add_audit(
    "analysis",
    len(analysis),
    0,
    "Success"
)


balancesheet = pd.read_excel(
    DATA_DIR / "balancesheet.xlsx",
    header=1
)

# Keep only valid company IDs
balancesheet = balancesheet[
    balancesheet["company_id"].isin(companies["id"])
]

# Remove duplicate company-year records
balancesheet = balancesheet.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)


balancesheet.to_sql(
    "balancesheet",
    conn,
    if_exists="append",
    index=False
)

print("Balance Sheet inserted successfully!")

add_audit("balancesheet", len(balancesheet), 0, "Success")

cashflow = pd.read_excel(
    DATA_DIR / "cashflow.xlsx",
    header=1
)

cashflow = cashflow[
    cashflow["company_id"].isin(companies["id"])
]

cashflow = cashflow.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)


cashflow.to_sql(
    "cashflow",
    conn,
    if_exists="append",
    index=False
)

print("Cash Flow inserted successfully!")

add_audit("cashflow", len(cashflow), 0, "Success")

profitandloss = pd.read_excel(
    DATA_DIR / "profitandloss.xlsx",
    header=1
)

profitandloss = profitandloss[
    profitandloss["company_id"].isin(companies["id"])
]

profitandloss = profitandloss.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)


profitandloss.to_sql(
    "profitandloss",
    conn,
    if_exists="append",
    index=False
)

print("Profit and Loss inserted successfully!")

add_audit("profitandloss", len(profitandloss), 0, "Success")

financial_ratios = pd.read_excel(
    DATA_DIR / "financial_ratios.xlsx"
)

financial_ratios = financial_ratios[
    financial_ratios["company_id"].isin(companies["id"])
]

financial_ratios = financial_ratios.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)

financial_ratios.to_sql(
    "financial_ratios",
    conn,
    if_exists="append",
    index=False
)

print("Financial Ratios inserted successfully!")

add_audit("financial_ratios", len(financial_ratios), 0, "Success")

market_cap = pd.read_excel(
    DATA_DIR / "market_cap.xlsx"
)

market_cap.to_sql(
    "market_cap",
    conn,
    if_exists="append",
    index=False
)

print("Market Cap inserted successfully!")

add_audit("market_cap", len(market_cap), 0, "Success")

peer_groups = pd.read_excel(
    DATA_DIR / "peer_groups.xlsx"
)

peer_groups.to_sql(
    "peer_groups",
    conn,
    if_exists="append",
    index=False
)

print("Peer Groups inserted successfully!")

add_audit("peer_groups", len(peer_groups), 0, "Success")

stock_prices = pd.read_excel(
    DATA_DIR / "stock_prices.xlsx"
)

stock_prices.to_sql(
    "stock_prices",
    conn,
    if_exists="append",
    index=False
)

print("Stock Prices inserted successfully!")

add_audit("stock_prices", len(stock_prices), 0, "Success")

"""documents = pd.read_excel(
    DATA_DIR / "documents.xlsx",
    header=1
)

documents.to_sql(
    "documents",
    conn,
    if_exists="append",
    index=False
)

print("Documents inserted successfully!")

add_audit("documents", len(documents), 0, "Success"))"""

pd.DataFrame(audit).to_csv(
    OUTPUT_DIR / "load_audit.csv",
    index=False
)

print("\nLoad audit saved.")

conn.commit()
conn.close()

print("Database connection closed.")