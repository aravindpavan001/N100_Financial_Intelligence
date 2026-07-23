def calculate_free_cash_flow(operating_activity, investing_activity):
    """
    Free Cash Flow (FCF)

    Formula:
        Operating Activity + Investing Activity
    """
    return operating_activity + investing_activity


def calculate_cfo_quality(cfo_values, pat_values):
    """
    Calculate average CFO/PAT ratio over all years.

    Returns:
        (average_ratio, classification)

    Classification:
        >1.0 -> High Quality
        0.5 to 1.0 -> Moderate
        <0.5 -> Accrual Risk

    If any PAT value is zero:
        return (None, None)
    """

    if len(cfo_values) != len(pat_values):
        raise ValueError("CFO and PAT lists must have the same length.")

    ratios = []

    for cfo, pat in zip(cfo_values, pat_values):
        if pat == 0:
            return (None, None)

        ratios.append(cfo / pat)

    average_ratio = sum(ratios) / len(ratios)

    if average_ratio > 1:
        classification = "High Quality"
    elif average_ratio >= 0.5:
        classification = "Moderate"
    else:
        classification = "Accrual Risk"

    return (average_ratio, classification)


def calculate_capex_intensity(investing_activity, sales):
    """
    CapEx Intensity

    Formula:
        abs(Investing Activity) / Sales * 100
    """

    if sales == 0:
        return (None, None)

    value = abs(investing_activity) / sales * 100

    if value < 3:
        classification = "Asset Light"
    elif value <= 8:
        classification = "Moderate"
    else:
        classification = "Capital Intensive"

    return (value, classification)


def calculate_fcf_conversion(free_cash_flow, operating_profit):
    """
    FCF Conversion

    Formula:
        FCF / Operating Profit * 100
    """

    if operating_profit == 0:
        return None

    return (free_cash_flow / operating_profit) * 100


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
# DAY 31 - CASH FLOW INTELLIGENCE ENGINE
# =====================================================

import sqlite3
import pandas as pd
from pathlib import Path
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

cashflow = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

profitloss = pd.read_sql(
    "SELECT * FROM profitandloss",
    conn
)

financial_ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

sectors = pd.read_sql(
    "SELECT * FROM sectors",
    conn
)


print("=" * 60)
print("Cashflow Columns")
print("=" * 60)
print(cashflow.columns.tolist())

print()

print("=" * 60)
print("Profit & Loss Columns")
print("=" * 60)
print(profitloss.columns.tolist())

print()

print("=" * 60)
print("Financial Ratios Columns")
print("=" * 60)
print(financial_ratios.columns.tolist())

print()

print("=" * 60)
print("Companies Columns")
print("=" * 60)
print(companies.columns.tolist())

print()

print("=" * 60)
print("Sectors Columns")
print("=" * 60)
print(sectors.columns.tolist())

conn.close()



# =====================================================
# MERGE DATA
# =====================================================

df = (
    cashflow
    .merge(
        profitloss,
        on=["company_id", "year"],
        how="left",
        suffixes=("_cf", "_pl")
    )
    .merge(
        financial_ratios,
        on=["company_id", "year"],
        how="left",
        suffixes=("", "_ratio")
    )
    .merge(
        companies,
        left_on="company_id",
        right_on="id",
        how="left"
    )
    .merge(
        sectors,
        on="company_id",
        how="left"
    )
)

print("=" * 60)
print("Merged Dataset")
print("=" * 60)

print(df.head())

print()

print("Rows :", len(df))

print("Companies :", df["company_id"].nunique())

# =====================================================
# CREATE CASH FLOW INTELLIGENCE
# =====================================================

results = []

for company_id, company_df in df.groupby("company_id"):

    company_df = company_df.sort_values("year")
    latest = company_df.iloc[-1]

    try:
        cfo_score, cfo_label = calculate_cfo_quality(
            company_df["operating_activity"].tolist(),
            company_df["net_profit"].tolist()
        )
    except Exception:
        cfo_score = None
        cfo_label = None

    try:
        capex_pct, capex_label = calculate_capex_intensity(
            latest["investing_activity"],
            latest["sales"]
        )
    except Exception:
        capex_pct = None
        capex_label = None

    if (
        latest["operating_activity"] < 0
        and
        latest["financing_activity"] > 0
    ):
        distress_flag = "YES"
    else:
        distress_flag = "NO"

    # -----------------------------
    # Deleveraging Flag
    # -----------------------------
    deleveraging_flag = "NO"

    if len(company_df) >= 2:

     previous = company_df.iloc[-2]

    latest_debt = latest["total_debt_cr"]
    previous_debt = previous["total_debt_cr"]

    if (
        pd.notna(latest_debt)
        and pd.notna(previous_debt)
        and latest["financing_activity"] < 0
        and latest_debt < previous_debt
    ):
        deleveraging_flag = "YES"    
    # -----------------------------
    # FCF Conversion
    # -----------------------------
    try:
     fcf_conversion = calculate_fcf_conversion(
        latest["free_cash_flow_cr"],
        latest["operating_profit"]
    )
    except Exception:
     fcf_conversion = None
    
    # -----------------------------
     # Capital Allocation
    # -----------------------------
    capital_allocation = classify_capital_allocation(
    latest["operating_activity"],
    latest["investing_activity"],
    latest["financing_activity"],
    cfo_label
)
    fcf_cagr_5yr = None
    results.append({
    "company_id": company_id,
    "company_name": latest["company_name"],
    "sector": latest["broad_sector"],

    "cfo_quality_score": cfo_score,
    "cfo_quality_label": cfo_label,

    "capex_intensity_pct": capex_pct,
    "capex_label": capex_label,

    "fcf_cagr_5yr": fcf_cagr_5yr,
    "fcf_conversion_pct": fcf_conversion,

    "capital_allocation_label": capital_allocation,

    "distress_flag": distress_flag,
    "deleveraging_flag": deleveraging_flag,
})


cashflow_intelligence = pd.DataFrame(results)

cashflow_intelligence = cashflow_intelligence[
    [
        "company_id",
        "company_name",
        "sector",
        "cfo_quality_score",
        "cfo_quality_label",
        "capex_intensity_pct",
        "capex_label",
        "fcf_cagr_5yr",
        "fcf_conversion_pct",
        "capital_allocation_label",
        "distress_flag",
        "deleveraging_flag",
    ]
]

cashflow_file = OUTPUT_DIR / "cashflow_intelligence.xlsx"

cashflow_intelligence.to_excel(
    cashflow_file,
    index=False
)

distress_alerts = cashflow_intelligence[
    cashflow_intelligence["distress_flag"] == "YES"
][[
    "company_id",
    "company_name",
    "distress_flag"
]]

distress_file = OUTPUT_DIR / "distress_alerts.csv"

distress_alerts.to_csv(
    distress_file,
    index=False
)

print()
print("Saved:", cashflow_file)
print("Saved:", distress_file)

print("=" * 60)
print("Cash Flow Intelligence")
print("=" * 60)

print(cashflow_intelligence.head())

print()
print("Rows :", len(cashflow_intelligence))