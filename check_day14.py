import pandas as pd

df = pd.read_csv("output/screener_dataset.csv")

print(df["revenue_cagr_5yr"].notna().sum())
print(df["pat_cagr_5yr"].notna().sum())