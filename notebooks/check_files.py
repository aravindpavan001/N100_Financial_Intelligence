import pandas as pd

failures = []

def add_failure(rule_id, severity, table_name, message):
    failures.append({
        "rule_id": rule_id,
        "severity": severity,
        "table_name": table_name,
        "message": message
    })

# Files with header in row 2

companies = pd.read_excel(
    "data/raw/companies.xlsx",
    header=1
)

analysis = pd.read_excel(
    "data/raw/analysis.xlsx",
    header=1
)

balancesheet = pd.read_excel(
    "data/raw/balancesheet.xlsx",
    header=1
)

cashflow = pd.read_excel(
    "data/raw/cashflow.xlsx",
    header=1
)

peer_groups = pd.read_excel(
    "data/raw/peer_groups.xlsx",
    header=1
)

profitandloss = pd.read_excel(
    "data/raw/profitandloss.xlsx",
    header=1
)

sectors = pd.read_excel(
    "data/raw/sectors.xlsx",
    header=1
)

stock_prices = pd.read_excel(
    "data/raw/stock_prices.xlsx",
    header=1
)

# Files with header in row 1

financial_ratios = pd.read_excel(
    "data/raw/financial_ratios.xlsx",
    header=0
)

market_cap = pd.read_excel(
    "data/raw/market_cap.xlsx",
    header=0
)

print("\nCOMPANIES")
print(companies.columns.tolist())

print("\nBALANCESHEET")
print(balancesheet.columns.tolist())

print("\nPROFITANDLOSS")
print(profitandloss.columns.tolist())

print("\nFINANCIAL RATIOS")
print(financial_ratios.columns.tolist())

print("\nMARKET CAP")
print(market_cap.columns.tolist())