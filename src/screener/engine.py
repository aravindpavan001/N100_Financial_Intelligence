import sqlite3
import yaml
import pandas as pd


DB_PATH = "nifty100.db"

CONFIG_PATH = "config/screener_config.yaml"


def load_config(path):
    """
    Load YAML configuration.
    """

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:

        config = yaml.safe_load(file)

    return config


def load_financial_ratios(db_path):
    """
    Load financial_ratios table.
    """

    conn = sqlite3.connect(db_path)

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn,
    )

    conn.close()

    return df


def apply_filters(
    df,
    config,
):
    """
    Apply all configured filters.
    """

    filters = config["filters"]

    filter_mapping = {

        "roe_min": (
            "return_on_equity_pct",
            ">=",
        ),

        "debt_to_equity_max": (
            "debt_to_equity",
            "<=",
        ),

        "free_cash_flow_min": (
            "free_cash_flow_cr",
            ">=",
        ),

        "revenue_cagr_5yr_min": (
            "revenue_cagr_5yr",
            ">=",
        ),

        "pat_cagr_5yr_min": (
            "pat_cagr_5yr",
            ">=",
        ),

        "opm_min": (
            "operating_profit_margin_pct",
            ">=",
        ),

        "icr_min": (
            "interest_coverage",
            ">=",
        ),

        "eps_cagr_min": (
            "eps_cagr_5yr",
            ">=",
        ),

        "asset_turnover_min": (
            "asset_turnover",
            ">=",
        ),
    }

    filtered_df = df.copy()

    for yaml_key, (column, operator) in filter_mapping.items():

        value = filters.get(yaml_key)

        if value is None:
            continue

        if column not in filtered_df.columns:
            continue

        if operator == ">=":
            filtered_df = filtered_df[
                filtered_df[column] >= value
            ]

        elif operator == "<=":
            filtered_df = filtered_df[
                filtered_df[column] <= value
            ]

    if "composite_quality_score" in filtered_df.columns:

     filtered_df = filtered_df.sort_values(
        by="composite_quality_score",
        ascending=False,
        na_position="last",
    )

    filtered_df.reset_index(
    drop=True,
    inplace=True,
)

    return filtered_df


def main():

    config = load_config(
        CONFIG_PATH,
    )

    print("=" * 70)
    print("SCREENING CONFIG")
    print("=" * 70)

    print(config)

    print()

    df = load_financial_ratios(
        DB_PATH,
    )

    print("=" * 70)
    print("FINANCIAL RATIOS")
    print("=" * 70)

    print(df.head())

    print()

    print("Rows :", len(df))

    filtered = apply_filters(
        df,
        config,
    )

    print()

    print("Filtered Rows :", len(filtered))
    print()

    print("=" * 70)
    print("SCREENER RESULTS")
    print("=" * 70)

    print(filtered)

    print()

    print("Filtered Rows :", len(filtered))

if __name__ == "__main__":
    main()