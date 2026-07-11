from src.screener.engine import load_config
from src.screener.engine import load_financial_ratios

config = load_config(
    "config/screener_config.yaml"
)

print(config)

df = load_financial_ratios(
    "nifty100.db"
)

print(df.head())

print(df.shape)