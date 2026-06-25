import pandas as pd

peer_groups = pd.read_excel(
    "data/raw/peer_groups.xlsx",
    header=None
)

sectors = pd.read_excel(
    "data/raw/sectors.xlsx",
    header=None
)

stock_prices = pd.read_excel(
    "data/raw/stock_prices.xlsx",
    header=None
)

print("\nPEER GROUPS")
print(peer_groups.head(10))

print("\nSECTORS")
print(sectors.head(10))

print("\nSTOCK PRICES")
print(stock_prices.head(10))