import re
import sqlite3
import pandas as pd
from pathlib import Path

# ----------------------------
# Paths
# ----------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ----------------------------
# Database
# ----------------------------

conn = sqlite3.connect(DB_PATH)

analysis = pd.read_sql(
    "SELECT * FROM analysis",
    conn
)

print("Analysis Columns:")
print(analysis.columns.tolist())

# ----------------------------
# Regex Pattern
# ----------------------------

PATTERN = re.compile(
    r"(?:(\d+)\s*Years?|Last\s*Year|TTM)\s*:?\s*(-?[\d.]+)%",
    re.IGNORECASE
)

# ----------------------------
# Target Columns
# ----------------------------

METRIC_COLUMNS = {
    "compounded_sales_growth": "Sales CAGR",
    "compounded_profit_growth": "Profit CAGR",
    "stock_price_cagr": "Stock CAGR",
    "roe": "ROE",
}

# ----------------------------
# Parse Data
# ----------------------------

parsed_rows = []
failed_rows = []

for _, row in analysis.iterrows():

    company = row["company_id"]

    for column, metric in METRIC_COLUMNS.items():

        text = str(row[column]).strip()

        match = PATTERN.search(text)

        if match:

            period = match.group(1)

            if period is not None:
             period = int(period)
            elif "Last Year" in text:
             period = 1
            elif "TTM" in text.upper():
             period = 0

            parsed_rows.append({
            "company_id": company,
             "metric_type": metric,
            "period_years": period,
             "value_pct": float(match.group(2))
             })

        else:

            failed_rows.append({
                "company_id": company,
                "metric_name": metric,
                "original_text": text
            })

# ----------------------------
# Create DataFrames
# ----------------------------

parsed_df = pd.DataFrame(parsed_rows)

failed_df = pd.DataFrame(failed_rows)

# ----------------------------
# Save Files
# ----------------------------

parsed_df.to_csv(
    OUTPUT_DIR / "analysis_parsed.csv",
    index=False
)

failed_df.to_csv(
    OUTPUT_DIR / "parse_failures.csv",
    index=False
)

# ----------------------------
# Summary
# ----------------------------

print()
print("Parsed rows :", len(parsed_df))
print("Failed rows :", len(failed_df))
print()

print(parsed_df.head())

print("\nFailed Entries:")

if failed_df.empty:
    print("No parse failures found.")
else:
    print(failed_df)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios LIMIT 5",
    conn
)

print("\nFinancial Ratios Columns:")
print(ratios.columns.tolist())
print()
print(ratios.head())    

conn.close()