import sqlite3
import pandas as pd
from pathlib import Path

# =====================================================
# PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# =====================================================
# DATABASE
# =====================================================

conn = sqlite3.connect(DB_PATH)

financial_ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

conn.close()

# =====================================================
# LATEST RECORD PER COMPANY
# =====================================================

df = financial_ratios.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left",
    suffixes=("_ratio", "_company")
)

df = (
    df.sort_values("year")
      .groupby("company_id")
      .tail(1)
      .reset_index(drop=True)
)

# =====================================================
# RULE ENGINE
# =====================================================

records = []

for _, row in df.iterrows():

    company = row["company_id"]

    # ----------------------------
    # PRO RULE 1
    # ROE > 20%
    # ----------------------------

    roe = row["return_on_equity_pct"]

    if pd.notna(roe) and roe > 20:

        records.append({
            "company_id": company,
            "type": "Pro",
            "rule_id": "P01",
            "text": "High return on equity demonstrates excellent capital efficiency.",
            "confidence_pct": 90
        })

    # ----------------------------
    # PRO RULE 2
    # Positive Free Cash Flow
    # ----------------------------

    fcf = row["free_cash_flow_cr"]

    if pd.notna(fcf) and fcf > 0:

        records.append({
            "company_id": company,
            "type": "Pro",
            "rule_id": "P02",
            "text": "Positive free cash flow supports healthy business fundamentals.",
            "confidence_pct": 88
        })

    # ----------------------------
    # PRO RULE 3
    # Debt Free
    # ----------------------------

    debt = row["total_debt_cr"]

    if pd.notna(debt) and debt == 0:

        records.append({
            "company_id": company,
            "type": "Pro",
            "rule_id": "P03",
            "text": "Debt-free balance sheet provides financial flexibility.",
            "confidence_pct": 98
        })

    # ----------------------------
    # PRO RULE 4
    # Revenue CAGR
    # ----------------------------

    rev = row["revenue_cagr_5yr"]

    if pd.notna(rev) and rev > 15:

        records.append({
            "company_id": company,
            "type": "Pro",
            "rule_id": "P04",
            "text": "Revenue growing above 15% CAGR reflects strong business momentum.",
            "confidence_pct": 85
        })

    # ----------------------------
    # PRO RULE 5
    # OPM
    # ----------------------------

    opm = row["operating_profit_margin_pct"]

    if pd.notna(opm) and opm > 25:

        records.append({
            "company_id": company,
            "type": "Pro",
            "rule_id": "P05",
            "text": "High operating margins indicate strong pricing power.",
            "confidence_pct": 86
        })

    # ----------------------------
    # PRO RULE 6
    # PAT CAGR
    # ----------------------------

    pat = row["pat_cagr_5yr"]

    if pd.notna(pat) and pat > 20:

        records.append({
            "company_id": company,
            "type": "Pro",
            "rule_id": "P06",
            "text": "Profit growth above 20% creates long-term shareholder value.",
            "confidence_pct": 87
        })

    # ----------------------------
    # PRO RULE 7
    # Interest Coverage
    # ----------------------------

    icr = row["interest_coverage"]

    if (pd.notna(icr) and icr > 10) or (pd.notna(debt) and debt == 0):

        records.append({
            "company_id": company,
            "type": "Pro",
            "rule_id": "P07",
            "text": "High interest coverage reflects low financial stress.",
            "confidence_pct": 92
        })


    # =====================================================
    # CON RULES
    # =====================================================

    # C01 - High Debt to Equity
    de = row["debt_to_equity"]

    if pd.notna(de) and de > 2:
        records.append({
            "company_id": company,
            "type": "Con",
            "rule_id": "C01",
            "text": "High debt-to-equity ratio increases financial risk.",
            "confidence_pct": 90
        })

    # C02 - Negative Free Cash Flow
    if pd.notna(fcf) and fcf < 0:
        records.append({
            "company_id": company,
            "type": "Con",
            "rule_id": "C02",
            "text": "Negative free cash flow indicates cash generation concerns.",
            "confidence_pct": 88
        })

    # C03 - Low Operating Margin
    if pd.notna(opm) and opm < 10:
        records.append({
            "company_id": company,
            "type": "Con",
            "rule_id": "C03",
            "text": "Low operating margin suggests margin pressure.",
            "confidence_pct": 80
        })

    # C04 - Loss Making
    npm = row["net_profit_margin_pct"]

    if pd.notna(npm) and npm < 0:
        records.append({
            "company_id": company,
            "type": "Con",
            "rule_id": "C04",
            "text": "Company is currently loss making.",
            "confidence_pct": 95
        })

    # C05 - Weak Interest Coverage
    if pd.notna(icr) and icr < 1.5:
        records.append({
            "company_id": company,
            "type": "Con",
            "rule_id": "C05",
            "text": "Low interest coverage indicates debt servicing risk.",
            "confidence_pct": 92
        })

    # C06 - Unsustainable Dividend
    payout = row["dividend_payout_ratio_pct"]

    if pd.notna(payout) and payout > 100:
        records.append({
            "company_id": company,
            "type": "Con",
            "rule_id": "C06",
            "text": "Dividend payout above 100% may not be sustainable.",
            "confidence_pct": 84
        })

    # C07 - Weak Revenue CAGR
    if pd.notna(rev) and rev < 5:
        records.append({
            "company_id": company,
            "type": "Con",
            "rule_id": "C07",
            "text": "Revenue CAGR below 5% indicates weak long-term growth.",
            "confidence_pct": 85
        })

    # C08 - Weak ROE
    if pd.notna(roe) and roe < 10:
        records.append({
            "company_id": company,
            "type": "Con",
            "rule_id": "C08",
            "text": "Low return on equity indicates weak capital efficiency.",
            "confidence_pct": 82
        })

    # C09 - High Debt
    if pd.notna(debt) and debt > 10000:
        records.append({
            "company_id": company,
            "type": "Con",
            "rule_id": "C09",
            "text": "Large debt burden may affect future financial flexibility.",
            "confidence_pct": 78
        })


# =====================================================
# CREATE DATAFRAME
# =====================================================

pros_cons = pd.DataFrame(records)

# =====================================================
# KEEP ONLY CONFIDENCE > 60
# =====================================================

pros_cons = pros_cons[
    pros_cons["confidence_pct"] > 60
]

# =====================================================
# ENSURE EVERY COMPANY HAS AT LEAST ONE PRO & ONE CON
# =====================================================

all_companies = df["company_id"].unique()

existing = (
    pros_cons.groupby(["company_id", "type"])
    .size()
    .unstack(fill_value=0)
)

for company in all_companies:

    if company not in existing.index:

        existing.loc[company] = {"Pro": 0, "Con": 0}

    # ---------- Default Pro ----------

    if existing.loc[company].get("Pro", 0) == 0:

        pros_cons.loc[len(pros_cons)] = {
            "company_id": company,
            "type": "Pro",
            "rule_id": "P99",
            "text": "Business demonstrates stable operating performance.",
            "confidence_pct": 65
        }

    # ---------- Default Con ----------

    if existing.loc[company].get("Con", 0) == 0:

        pros_cons.loc[len(pros_cons)] = {
            "company_id": company,
            "type": "Con",
            "rule_id": "C99",
            "text": "Some financial indicators require continued monitoring.",
            "confidence_pct": 65
        }

# =====================================================
# SAVE CSV
# =====================================================

pros_cons.to_csv(
    OUTPUT_DIR / "pros_cons_generated.csv",
    index=False
)

## =====================================================
# VALIDATION
# =====================================================

summary = (
    pros_cons.groupby(["company_id", "type"])
    .size()
    .unstack(fill_value=0)
)

summary["Has_Pro"] = summary["Pro"] > 0
summary["Has_Con"] = summary["Con"] > 0

summary.to_csv(
    OUTPUT_DIR / "pros_cons_validation.csv"
)

print("=" * 60)
print("Rule Engine Summary")
print("=" * 60)

print()

print("Generated Statements :", len(pros_cons))
print("Companies Covered    :", pros_cons["company_id"].nunique())

print()

print("Companies with Pros :", summary["Has_Pro"].sum())
print("Companies with Cons :", summary["Has_Con"].sum())

print()

print("Companies Missing Pros :",
      (~summary["Has_Pro"]).sum())

print("Companies Missing Cons :",
      (~summary["Has_Con"]).sum())