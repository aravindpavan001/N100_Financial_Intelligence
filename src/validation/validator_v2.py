"""
validator_v2.py
Day 03 - Schema Validator (DQ-01 to DQ-16)

NOTE:
Some DQ rules (DQ-04, DQ-05, DQ-13, etc.) are implemented using the
best interpretation of the sprint specification because the assignment
does not define the exact formulas.
"""

import re
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

failures = []


def add_failure(rule_id, severity, table_name, message):
    failures.append({
        "rule_id": rule_id,
        "severity": severity,
        "table_name": table_name,
        "message": message,
    })


def valid_url(url):
    if pd.isna(url):
        return False
    return bool(re.match(r"^https?://", str(url)))


companies = pd.read_excel(DATA_DIR / "companies.xlsx", header=1)
analysis = pd.read_excel(DATA_DIR / "analysis.xlsx", header=1)
balancesheet = pd.read_excel(DATA_DIR / "balancesheet.xlsx", header=1)
cashflow = pd.read_excel(DATA_DIR / "cashflow.xlsx", header=1)
profitandloss = pd.read_excel(DATA_DIR / "profitandloss.xlsx", header=1)
financial_ratios = pd.read_excel(DATA_DIR / "financial_ratios.xlsx", header=0)
market_cap = pd.read_excel(DATA_DIR / "market_cap.xlsx", header=0)
peer_groups = pd.read_excel(DATA_DIR / "peer_groups.xlsx", header=0)
sectors = pd.read_excel(DATA_DIR / "sectors.xlsx", header=0)
stock_prices = pd.read_excel(DATA_DIR / "stock_prices.xlsx", header=0)


# DQ-01
dup = companies[companies["id"].duplicated()]
if not dup.empty:
    add_failure("DQ-01","CRITICAL","companies",f"{len(dup)} duplicate company ids")

# DQ-02
for name, df in {
    "balancesheet": balancesheet,
    "cashflow": cashflow,
    "financial_ratios": financial_ratios,
    "market_cap": market_cap,
    "profitandloss": profitandloss,
}.items():
    dup = df[df.duplicated(subset=["company_id","year"])]
    if not dup.empty:
        add_failure("DQ-02","CRITICAL",name,f"{len(dup)} duplicate company-year rows")

# DQ-03
valid_ids = set(companies["id"])
for name, df in {
    "analysis": analysis,
    "balancesheet": balancesheet,
    "cashflow": cashflow,
    "financial_ratios": financial_ratios,
    "market_cap": market_cap,
    "peer_groups": peer_groups,
    "sectors": sectors,
    "stock_prices": stock_prices,
    "profitandloss": profitandloss,
}.items():
    col = "company_id"
    if col in df.columns:
        bad = df[~df[col].isin(valid_ids)]
        if not bad.empty:
            add_failure("DQ-03","CRITICAL",name,f"{len(bad)} invalid company ids")

# DQ-04 Balance Sheet
diff = (balancesheet["total_liabilities"]-balancesheet["total_assets"]).abs()
bad = balancesheet[diff > (balancesheet["total_assets"].abs()*0.01)]
if not bad.empty:
    add_failure("DQ-04","WARNING","balancesheet",f"{len(bad)} balance sheet mismatch")

# DQ-05 OPM cross check
calc = (profitandloss["operating_profit"]/profitandloss["sales"])*100
bad = profitandloss[(profitandloss["sales"]>0) & ((calc-profitandloss["opm_percentage"]).abs()>1)]
if not bad.empty:
    add_failure("DQ-05","WARNING","profitandloss",f"{len(bad)} OPM mismatch")

# DQ-06
bad = profitandloss[profitandloss["sales"]<=0]
if not bad.empty:
    add_failure("DQ-06","WARNING","profitandloss",f"{len(bad)} non-positive sales")

# DQ-07
bad = profitandloss[(profitandloss["tax_percentage"]<0)|(profitandloss["tax_percentage"]>100)]
if not bad.empty:
    add_failure("DQ-07","WARNING","profitandloss",f"{len(bad)} invalid tax rates")

# DQ-08
bad = profitandloss[profitandloss["eps"].isna()]
if not bad.empty:
    add_failure("DQ-08","WARNING","profitandloss",f"{len(bad)} missing EPS")

# DQ-09
bad = stock_prices[stock_prices["close_price"]<=0]
if not bad.empty:
    add_failure("DQ-09","WARNING","stock_prices",f"{len(bad)} invalid close price")

# DQ-10
bad = market_cap[market_cap["dividend_yield_pct"]<0]
if not bad.empty:
    add_failure("DQ-10","WARNING","market_cap",f"{len(bad)} negative dividend yield")

# DQ-11
bad = financial_ratios[financial_ratios["return_on_equity_pct"].isna()]
if not bad.empty:
    add_failure("DQ-11","WARNING","financial_ratios",f"{len(bad)} missing ROE")

# DQ-12
bad = companies[~companies["website"].apply(valid_url)]
if not bad.empty:
    add_failure("DQ-12","WARNING","companies",f"{len(bad)} invalid website URLs")

# DQ-13
bad = cashflow[cashflow["net_cash_flow"].isna()]
if not bad.empty:
    add_failure("DQ-13","WARNING","cashflow",f"{len(bad)} missing net cash flow")

# DQ-14
bad = balancesheet[balancesheet["borrowings"]<0]
if not bad.empty:
    add_failure("DQ-14","WARNING","balancesheet",f"{len(bad)} negative borrowings")

# DQ-15
bad = companies[companies["book_value"]<=0]
if not bad.empty:
    add_failure("DQ-15","WARNING","companies",f"{len(bad)} invalid book value")

# DQ-16
bad = sectors[sectors["broad_sector"].isna()]
if not bad.empty:
    add_failure("DQ-16","WARNING","sectors",f"{len(bad)} missing sector")

results = pd.DataFrame(failures)
results.to_csv(OUTPUT_DIR/"validation_failures.csv",index=False)

print(results)
print("\\nSaved:", OUTPUT_DIR/"validation_failures.csv")
