import pandas as pd
from pathlib import Path

import utils.db as db


def get_recommendation(row):

    quality = row["composite_quality_score"]
    pe = row["pe_ratio"]
    debt = row["debt_to_equity"]

    if pd.isna(quality):
     quality = 0

    if pd.isna(pe):
     pe = 999

    if pd.isna(debt):
     debt = 999

    score = quality

    if pe <= 20:
        score += 10
    elif pe > 40:
        score -= 10

    if debt <= 0.5:
        score += 10
    elif debt > 1:
        score -= 10

    score = max(0, min(100, score))

    if score >= 80:
        recommendation = "BUY"
    elif score >= 60:
        recommendation = "HOLD"
    else:
        recommendation = "AVOID"

    return recommendation, score


companies = db.get_companies()

results = []

for company in companies["company_name"]:

    kpis = db.get_company_kpis(company)

    if kpis.empty:
        continue

    row = kpis.iloc[0]

    if pd.isna(row["composite_quality_score"]):
     continue

    recommendation, score = get_recommendation(row)

    results.append({
        "Company": company,
        "Quality Score": row["composite_quality_score"],
        "PE Ratio": row["pe_ratio"],
        "Debt to Equity": row["debt_to_equity"],
        "Recommendation": recommendation,
        "Valuation Score": score,
    })

df = pd.DataFrame(results)

BASE_DIR = Path(__file__).resolve().parents[2]

output_folder = BASE_DIR / "output"

output_folder.mkdir(exist_ok=True)

output_file = output_folder / "valuation_summary.xlsx"

df.to_excel(output_file, index=False)

print("Export completed!")
print(output_file)