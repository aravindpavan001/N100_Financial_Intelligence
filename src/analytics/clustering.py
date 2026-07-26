import sqlite3
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"

REPORT_DIR = BASE_DIR / "reports"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ==========================================================
# DATABASE
# ==========================================================

conn = sqlite3.connect(DB_PATH)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

financial_ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

sectors = pd.read_sql(
    "SELECT * FROM sectors",
    conn
)

conn.close()

# ==========================================================
# LOAD LATEST YEAR
# ==========================================================

latest_ratios = (

    financial_ratios

    .sort_values("year")

    .groupby("company_id")

    .tail(1)

    .reset_index(drop=True)

)

print()

print("=" * 60)
print("LATEST COMPANY RECORDS")
print("=" * 60)

print(len(latest_ratios))

# ==========================================================
# MERGE TABLES
# ==========================================================

cluster_df = latest_ratios.merge(

    sectors[
        [
            "company_id",
            "broad_sector",
            "sub_sector"
        ]
    ],

    on="company_id",

    how="left"

)

cluster_df = cluster_df.merge(

    companies[
        [
            "id",
            "company_name"
        ]
    ],

    left_on="company_id",

    right_on="id",

    how="left"

)

print()

print("=" * 60)
print("MERGED DATA")
print("=" * 60)

print(cluster_df.head())

# ==========================================================
# FEATURES
# ==========================================================

FEATURES = [

    "return_on_equity_pct",

    "debt_to_equity",

    "revenue_cagr_5yr",

    "free_cash_flow_cr",

    "operating_profit_margin_pct"

]

print()

print("=" * 60)
print("FEATURE CHECK")
print("=" * 60)

for feature in FEATURES:

    if feature in cluster_df.columns:

        print(feature, "✓")

    else:

        print(feature, "MISSING")

# ==========================================================
# KEEP ONLY REQUIRED COLUMNS
# ==========================================================

feature_df = cluster_df[

    [
        "company_id",
        "company_name",
        "broad_sector"
    ]

    +

    FEATURES

].copy()

feature_df["company_name"] = (

    feature_df["company_name"]

    .astype(str)

    .str.replace("\n", " ", regex=False)

    .str.strip()

)

# ==========================================================
# BEFORE IMPUTATION
# ==========================================================

print()

print("=" * 60)
print("MISSING VALUES BEFORE")
print("=" * 60)

print(

    feature_df[FEATURES]

    .isna()

    .sum()

)

# ==========================================================
# SECTOR MEDIAN IMPUTATION
# ==========================================================

for feature in FEATURES:

    feature_df[feature] = (

        feature_df

        .groupby("broad_sector")[feature]

        .transform(

            lambda x:

            x.fillna(

                x.median()

            )

        )

    )

# ==========================================================
# GLOBAL MEDIAN (ONLY IF ENTIRE SECTOR IS NaN)
# ==========================================================

for feature in FEATURES:

    feature_df[feature] = (

        feature_df[feature]

        .fillna(

            feature_df[feature].median()

        )

    )

# ==========================================================
# VERIFY
# ==========================================================

print()

print("=" * 60)
print("MISSING VALUES AFTER")
print("=" * 60)

print(

    feature_df[FEATURES]

    .isna()

    .sum()

)

print()

print("=" * 60)
print("READY FOR SCALING")
print("=" * 60)
print(feature_df.head())

# ==========================================================
# STANDARDIZE FEATURES
# ==========================================================

X = feature_df[FEATURES].copy()

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

print()

print("=" * 60)
print("FEATURES STANDARDIZED")
print("=" * 60)

print(pd.DataFrame(X_scaled, columns=FEATURES).head())

# ==========================================================
# ELBOW METHOD
# ==========================================================

inertia = []

k_values = range(2, 11)

for k in k_values:

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(X_scaled)

    inertia.append(model.inertia_)

plt.figure(figsize=(8, 5))

plt.plot(
    list(k_values),
    inertia,
    marker="o",
    linewidth=2
)

plt.title("KMeans Elbow Plot")

plt.xlabel("Number of Clusters")

plt.ylabel("Inertia")

plt.grid(True)

plt.tight_layout()

elbow_path = REPORT_DIR / "elbow_plot.png"

plt.savefig(
    elbow_path,
    dpi=200
)

plt.close()

print()

print("=" * 60)
print("ELBOW PLOT SAVED")
print("=" * 60)

print(elbow_path)

# ==========================================================
# FINAL KMEANS MODEL
# ==========================================================

kmeans = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)

cluster_ids = kmeans.fit_predict(X_scaled)

# ==========================================================
# DISTANCE FROM CENTROID
# ==========================================================

distances = kmeans.transform(X_scaled)

distance_from_centroid = []

for i in range(len(cluster_ids)):

    distance_from_centroid.append(

        distances[i][cluster_ids[i]]

    )

# ==========================================================
# BUILD OUTPUT
# ==========================================================

cluster_names = {

    0: "Cluster 0",

    1: "Cluster 1",

    2: "Cluster 2",

    3: "Cluster 3",

    4: "Cluster 4"

}

cluster_labels = pd.DataFrame({

    "company_id": feature_df["company_id"],

    "company_name": feature_df["company_name"],

    "sector": feature_df["broad_sector"],

    "cluster_id": cluster_ids,

    "cluster_name": [

        cluster_names[x]

        for x in cluster_ids

    ],

    "distance_from_centroid": distance_from_centroid

})

# ==========================================================
# SORT OUTPUT
# ==========================================================

cluster_labels = cluster_labels.sort_values(

    "company_id"

).reset_index(drop=True)

# ==========================================================
# SAVE CSV
# ==========================================================

csv_path = OUTPUT_DIR / "cluster_labels.csv"

cluster_labels.to_csv(

    csv_path,

    index=False

)

print()

print("=" * 60)
print("CLUSTER LABELS CREATED")
print("=" * 60)

print(csv_path)

# ==========================================================
# VALIDATION
# ==========================================================

print()

print("=" * 60)
print("VALIDATION")
print("=" * 60)

print()

print("Companies")

print(len(cluster_labels))

print()

print("Cluster Counts")

print(

    cluster_labels["cluster_id"]

    .value_counts()

    .sort_index()

)

print()

print("Missing Values")

print(

    cluster_labels

    .isna()

    .sum()

)

print()

print("Unique Clusters")

print(

    sorted(

        cluster_labels["cluster_id"].unique()

    )

)

print()

print("Companies Per Cluster")

print(

    cluster_labels["cluster_id"]

    .value_counts()

)

print()

print("=" * 60)
print("SAMPLE OUTPUT")
print("=" * 60)

print(

    cluster_labels.head(10)

)

# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    print()

    print("=" * 60)
    print("DAY 36 COMPLETED")
    print("=" * 60)

    print()

    print("Generated Files")

    print("-------------------------")

    print(elbow_path)

    print(csv_path)    