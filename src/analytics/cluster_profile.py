import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import zscore

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"

REPORT_DIR = BASE_DIR / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================================
# DATABASE
# ==========================================================

conn = sqlite3.connect(DB_PATH)

financial_ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)

companies = pd.read_sql("SELECT * FROM companies", conn)

sectors = pd.read_sql("SELECT * FROM sectors", conn)

conn.close()

# ==========================================================
# LOAD CLUSTER LABELS
# ==========================================================

cluster_labels = pd.read_csv(OUTPUT_DIR / "cluster_labels.csv")

# ==========================================================
# LOAD LATEST YEAR
# ==========================================================

latest = (
    financial_ratios.sort_values("year")
    .groupby("company_id")
    .tail(1)
    .reset_index(drop=True)
)

print()

print("=" * 60)
print("LATEST FINANCIAL DATA")
print("=" * 60)

print(len(latest))

# ==========================================================
# MERGE TABLES
# ==========================================================

profile_df = latest.merge(
    cluster_labels[["company_id", "cluster_id", "cluster_name"]],
    on="company_id",
    how="left",
)

profile_df = profile_df.merge(
    sectors[["company_id", "broad_sector", "sub_sector"]], on="company_id", how="left"
)

profile_df = profile_df.merge(
    companies[["id", "company_name"]], left_on="company_id", right_on="id", how="left"
)

profile_df["company_name"] = (
    profile_df["company_name"]
    .astype(str)
    .str.replace("\n", " ", regex=False)
    .str.strip()
)

print()

print("=" * 60)
print("MERGED DATA")
print("=" * 60)

print(profile_df.head())

# ==========================================================
# FEATURES
# ==========================================================

FEATURES = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "free_cash_flow_cr",
    "operating_profit_margin_pct",
]

# ==========================================================
# CLUSTER PROFILING
# ==========================================================

cluster_profiles = profile_df.groupby("cluster_id")[FEATURES].agg(["mean", "median"])

cluster_profiles.columns = ["_".join(col) for col in cluster_profiles.columns]

cluster_profiles = cluster_profiles.reset_index()

# ==========================================================
# ADD CLUSTER NAME
# ==========================================================

cluster_names = profile_df[["cluster_id", "cluster_name"]].drop_duplicates()

cluster_profiles = cluster_profiles.merge(cluster_names, on="cluster_id", how="left")

cluster_profiles = cluster_profiles[
    ["cluster_id", "cluster_name"]
    + [c for c in cluster_profiles.columns if c not in ["cluster_id", "cluster_name"]]
]

# ==========================================================
# SAVE
# ==========================================================

profile_path = OUTPUT_DIR / "cluster_profiles.csv"

cluster_profiles.to_csv(profile_path, index=False)

# ==========================================================
# SHOW CLUSTER MEMBERS
# ==========================================================

print()

print("=" * 60)
print("CLUSTER MEMBERS")
print("=" * 60)

for cluster in sorted(profile_df["cluster_id"].dropna().unique()):

    print()

    print("-" * 50)

    print(f"Cluster {int(cluster)}")

    print("-" * 50)

    members = profile_df[profile_df["cluster_id"] == cluster]["company_name"]

    for company in members:

        print(company)

# ==========================================================
# VALIDATION
# ==========================================================

print()

print("=" * 60)
print("CLUSTER PROFILE SUMMARY")
print("=" * 60)

print(cluster_profiles)

print()

print("=" * 60)
print("TOTAL CLUSTERS")
print("=" * 60)

print(len(cluster_profiles))

print()

print("=" * 60)
print("PROFILE SAVED")
print("=" * 60)

print(profile_path)

# ==========================================================
# ASSIGN BUSINESS NAMES
# ==========================================================

business_names = {
    0: "Stable Compounders",
    1: "High Growth Finance",
    2: "Balanced Performers",
    3: "Defense Leaders",
    4: "Banking Institutions",
}

cluster_labels["cluster_name"] = cluster_labels["cluster_id"].map(business_names)

cluster_profiles["cluster_name"] = cluster_profiles["cluster_id"].map(business_names)

# ==========================================================
# SAVE UPDATED FILES
# ==========================================================

cluster_labels.to_csv(OUTPUT_DIR / "cluster_labels.csv", index=False)

cluster_profiles.to_csv(OUTPUT_DIR / "cluster_profiles.csv", index=False)

print()

print("=" * 60)
print("UPDATED CLUSTER NAMES")
print("=" * 60)

print(cluster_profiles[["cluster_id", "cluster_name"]])


# ==========================================================
# CORRELATION HEATMAP
# ==========================================================

HEATMAP_FEATURES = [
    "return_on_equity_pct",
    "operating_profit_margin_pct",
    "debt_to_equity",
    "interest_coverage",
    "asset_turnover",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "free_cash_flow_cr",
    "earnings_per_share",
    "dividend_payout_ratio_pct",
]

corr = profile_df[HEATMAP_FEATURES].corr(method="pearson")

plt.figure(figsize=(10, 8))

sns.heatmap(corr, annot=True, cmap="RdYlBu", center=0, fmt=".2f")

plt.title("Financial KPI Correlation Heatmap")

plt.tight_layout()

heatmap_path = REPORT_DIR / "correlation_heatmap.png"

plt.savefig(heatmap_path, dpi=200)

plt.close()

print()

print("=" * 60)
print("HEATMAP CREATED")
print("=" * 60)

print(heatmap_path)

# ==========================================================
# OUTLIER DETECTION
# ==========================================================

PORTFOLIO_STATS_FEATURES = [
    "return_on_equity_pct",
    "operating_profit_margin_pct",
    "debt_to_equity",
    "interest_coverage",
    "asset_turnover",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "free_cash_flow_cr",
    "earnings_per_share",
    "dividend_payout_ratio_pct",
]

outliers = []

for sector in profile_df["broad_sector"].dropna().unique():

    sector_df = profile_df[profile_df["broad_sector"] == sector].copy()

    for metric in PORTFOLIO_STATS_FEATURES:

        if sector_df[metric].std() == 0:

            continue

        sector_df["z"] = zscore(sector_df[metric], nan_policy="omit")

        flagged = sector_df[sector_df["z"].abs() > 3]

        for _, row in flagged.iterrows():

            outliers.append(
                {
                    "company_id": row["company_id"],
                    "company_name": row["company_name"],
                    "sector": sector,
                    "metric": metric,
                    "value": row[metric],
                    "z_score": row["z"],
                }
            )

outlier_df = pd.DataFrame(outliers)

outlier_path = OUTPUT_DIR / "outlier_report.csv"

outlier_df.to_csv(outlier_path, index=False)

print()

print("=" * 60)
print("OUTLIER REPORT CREATED")
print("=" * 60)

print(outlier_path)

# ==========================================================
# PORTFOLIO STATISTICS
# ==========================================================

stats = []

for metric in PORTFOLIO_STATS_FEATURES:

    values = profile_df[metric].dropna()

    stats.append(
        {
            "metric": metric,
            "P10": values.quantile(0.10),
            "P25": values.quantile(0.25),
            "P50": values.quantile(0.50),
            "P75": values.quantile(0.75),
            "P90": values.quantile(0.90),
            "Mean": values.mean(),
            "Std": values.std(),
        }
    )

portfolio_stats = pd.DataFrame(stats)

stats_path = OUTPUT_DIR / "portfolio_stats.csv"

portfolio_stats.to_csv(stats_path, index=False)

print()

print("=" * 60)
print("PORTFOLIO STATS CREATED")
print("=" * 60)

print(stats_path)

# ==========================================================
# FINAL VALIDATION
# ==========================================================

print()

print("=" * 60)
print("FINAL VALIDATION")
print("=" * 60)

print()

print("Companies")

print(len(cluster_labels))

print()

print("Clusters")

print(cluster_labels["cluster_name"].unique())

print()

print("Cluster Profiles")

print(len(cluster_profiles))

print()

print("Portfolio Statistics")

print(len(portfolio_stats))

print()

print("Outliers")

print(len(outlier_df))

print()

print("=" * 60)
print("GENERATED FILES")
print("=" * 60)

print(heatmap_path)

print(outlier_path)

print(stats_path)

# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    print()

    print("=" * 60)
    print("PART 1 COMPLETED")
    print("=" * 60)
