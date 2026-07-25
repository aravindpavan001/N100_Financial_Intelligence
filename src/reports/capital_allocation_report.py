import sqlite3
import pandas as pd
from pathlib import Path

# =====================================================
# CAPITAL ALLOCATION CLASSIFICATION
# =====================================================

def get_cashflow_sign(value):
    """
    Returns '+' for positive or zero values,
    '-' for negative values.
    """
    if value >= 0:
        return "+"
    return "-"


def classify_capital_allocation(
    cfo,
    cfi,
    cff,
    cfo_quality=None,
):
    """
    Classify capital allocation pattern.
    """

    cfo_sign = get_cashflow_sign(cfo)
    cfi_sign = get_cashflow_sign(cfi)
    cff_sign = get_cashflow_sign(cff)

    pattern = (cfo_sign, cfi_sign, cff_sign)

    if pattern == ("+", "-", "-"):
        if cfo_quality == "High Quality":
            return "Shareholder Returns"
        return "Reinvestor"

    if pattern == ("+", "+", "-"):
        return "Liquidating Assets"

    if pattern == ("-", "+", "+"):
        return "Distress Signal"

    if pattern == ("-", "-", "+"):
        return "Growth Funded by Debt"

    if pattern == ("+", "+", "+"):
        return "Cash Accumulator"

    if pattern == ("-", "-", "-"):
        return "Pre-Revenue"

    if pattern == ("+", "-", "+"):
        return "Mixed"

    return "Unknown"


# =====================================================
# PROJECT PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"

CASHFLOW_FILE = OUTPUT_DIR / "cashflow_intelligence.xlsx"


# =====================================================
# LOAD DATABASE
# =====================================================

conn = sqlite3.connect(DB_PATH)

cashflow = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

conn.close()


# =====================================================
# LOAD YESTERDAY'S FILE
# =====================================================

cashflow_intelligence = pd.read_excel(
    CASHFLOW_FILE
)


# =====================================================
# MERGE COMPANY NAMES
# =====================================================

cashflow = cashflow.merge(
    companies[["id", "company_name"]],
    left_on="company_id",
    right_on="id",
    how="left"
)


# =====================================================
# BUILD CAPITAL ALLOCATION HISTORY
# =====================================================

history = []

for _, row in cashflow.iterrows():

    label = classify_capital_allocation(
        row["operating_activity"],
        row["investing_activity"],
        row["financing_activity"]
    )

    history.append({
        "company_id": row["company_id"],
        "company_name": row["company_name"],
        "year": row["year"],
        "capital_allocation_label": label
    })


capital_allocation_history = pd.DataFrame(history)


# =====================================================
# PREVIEW
# =====================================================

print("=" * 60)
print("Cashflow")
print("=" * 60)
print(cashflow.head())

print()

print("=" * 60)
print("Cashflow Intelligence")
print("=" * 60)
print(cashflow_intelligence.head())

print()

print("=" * 60)
print("Capital Allocation History")
print("=" * 60)
print(capital_allocation_history.head())

print()

print("Rows :", len(capital_allocation_history))
print("Companies :", capital_allocation_history["company_id"].nunique())

# =====================================================
# DATASET VALIDATION
# =====================================================

print()
print("=" * 60)
print("Dataset Validation")
print("=" * 60)

# =====================================================
# LATEST YEAR PATTERN
# =====================================================

latest_patterns = (
    capital_allocation_history
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
    .reset_index(drop=True)
)

print()
print("=" * 60)
print("Latest Pattern")
print("=" * 60)

print(latest_patterns.head())

print()

print("Rows :", len(latest_patterns))

pattern_distribution = (
    latest_patterns["capital_allocation_label"]
    .value_counts()
    .reset_index()
)

pattern_distribution.columns = [
    "capital_allocation_pattern",
    "company_count"
]

distribution_file = OUTPUT_DIR / "pattern_distribution.csv"

pattern_distribution.to_csv(
    distribution_file,
    index=False
)

print()
print("=" * 60)
print("Pattern Distribution")
print("=" * 60)

print(pattern_distribution)

print()

print("Saved:", distribution_file)


# =====================================================
# PATTERN CHANGES
# =====================================================

pattern_changes = []

for company_id, company_df in capital_allocation_history.groupby("company_id"):

    company_df = company_df.sort_values("year")

    if len(company_df) < 2:
        continue

    previous = company_df.iloc[-2]
    current = company_df.iloc[-1]

    if previous["capital_allocation_label"] != current["capital_allocation_label"]:

        pattern_changes.append({
            "company_id": company_id,
            "company_name": current["company_name"],
            "previous_year": previous["year"],
            "current_year": current["year"],
            "previous_pattern": previous["capital_allocation_label"],
            "current_pattern": current["capital_allocation_label"]
        })

# Convert to DataFrame AFTER the loop finishes
pattern_changes = pd.DataFrame(pattern_changes)

print()
print("=" * 60)
print("Pattern Changes")
print("=" * 60)

print(pattern_changes.head())

print()
print("Companies Changed :", len(pattern_changes))
# =====================================================
# SAVE PATTERN CHANGES
# =====================================================

pattern_changes_file = OUTPUT_DIR / "pattern_changes.csv"

pattern_changes.to_csv(
    pattern_changes_file,
    index=False
)

print()
print("Saved:", pattern_changes_file)

# =====================================================
# CAPITAL ALLOCATION SUMMARY
# =====================================================

summary = pd.DataFrame({
    "Metric": [
        "Total Companies",
        "Total Company-Year Records",
        "Pattern Changes",
        "Most Common Pattern",
        "Least Common Pattern"
    ],
    "Value": [
        latest_patterns["company_id"].nunique(),
        len(capital_allocation_history),
        len(pattern_changes),
        pattern_distribution.iloc[0]["capital_allocation_pattern"],
        pattern_distribution.iloc[-1]["capital_allocation_pattern"]
    ]
})

summary_file = OUTPUT_DIR / "capital_allocation_summary.csv"

summary.to_csv(
    summary_file,
    index=False
)

print()
print("=" * 60)
print("Capital Allocation Summary")
print("=" * 60)

print(summary)

print()
print("Saved:", summary_file)


# Duplicate company-year records
duplicates = capital_allocation_history.duplicated(
    subset=["company_id", "year"]
).sum()

print(f"Duplicate Company-Year Records : {duplicates}")

# Missing company IDs
missing_company = capital_allocation_history["company_id"].isna().sum()

print(f"Missing Company IDs : {missing_company}")

# Missing years
missing_year = capital_allocation_history["year"].isna().sum()

print(f"Missing Years : {missing_year}")

# Missing labels
missing_labels = (
    capital_allocation_history["capital_allocation_label"]
    .isna()
    .sum()
)

print(f"Missing Labels : {missing_labels}")