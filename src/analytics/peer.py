import sqlite3
import pandas as pd

DB_PATH = "nifty100.db"


def load_peer_groups(db_path):

    conn = sqlite3.connect(db_path)

    df = pd.read_sql(
        "SELECT * FROM peer_groups",
        conn,
    )

    conn.close()

    return df


def load_financial_ratios(db_path):

    conn = sqlite3.connect(db_path)

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn,
    )

    conn.close()

    return df


def merge_peer_data(
    peer_df,
    ratio_df,
):

    merged = peer_df.merge(
        ratio_df,
        on="company_id",
        how="left",
    )

    return merged


def calculate_percentile_rank(
    df,
    metric,
    higher_is_better=True,
):
    """
    Returns percentile rank (0-100).
    """

    if higher_is_better:

        rank = df[metric].rank(
            method="average",
            pct=True,
            ascending=True,
        )

    else:

        rank = df[metric].rank(
            method="average",
            pct=True,
            ascending=False,
        )

    return rank * 100


METRICS = {

    "return_on_equity_pct": True,

    "operating_profit_margin_pct": True,

    "net_profit_margin_pct": True,

    "debt_to_equity": False,

    "free_cash_flow_cr": True,

    "revenue_cagr_5yr": True,

    "pat_cagr_5yr": True,

    "eps_cagr_5yr": True,

    "interest_coverage": True,

    "asset_turnover": True,

}


def calculate_all_percentiles(
    merged,
):

    results = []

    for peer_group in merged["peer_group_name"].dropna().unique():

        peer_df = merged[
            merged["peer_group_name"] == peer_group
        ]

        for year in peer_df["year"].dropna().unique():

            year_df = peer_df[
                peer_df["year"] == year
            ]

            for metric, higher_is_better in METRICS.items():

                if metric not in year_df.columns:
                    continue

                temp = year_df.copy()

                temp["percentile_rank"] = calculate_percentile_rank(
                    temp,
                    metric,
                    higher_is_better,
                )

                temp["metric"] = metric

                temp["metric_value"] = temp[metric]

                results.append(

                    temp[
                        [
                            "company_id",
                            "peer_group_name",
                            "year",
                            "metric",
                            "metric_value",
                            "percentile_rank",
                        ]
                    ]

                )

    final_df = pd.concat(
        results,
        ignore_index=True,
    )

    return final_df

def save_peer_percentiles(
    df,
    db_path,
):

    conn = sqlite3.connect(
        db_path,
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        DROP TABLE IF EXISTS peer_percentiles
        """
    )

    cursor.execute(
        """
        CREATE TABLE peer_percentiles (

            company_id TEXT,

            peer_group_name TEXT,

            year TEXT,

            metric TEXT,

            metric_value REAL,

            percentile_rank REAL

        )
        """
    )

    df.to_sql(

        "peer_percentiles",

        conn,

        if_exists="append",

        index=False,

    )

    conn.commit()

    conn.close()


if __name__ == "__main__":

    peer_df = load_peer_groups(
        DB_PATH,
    )

    print("PEER GROUPS")
    print(peer_df.head())

    print()

    ratio_df = load_financial_ratios(
        DB_PATH,
    )

    print("FINANCIAL RATIOS")
    print(ratio_df.head())

    print()

    merged = merge_peer_data(
        peer_df,
        ratio_df,
    )

    print("MERGED DATA")
    print(merged.head())

    print()

    print("ROE TEST")

    sample = pd.DataFrame(
        {
            "roe": [
                10,
                15,
                20,
                25,
                30,
            ]
        }
    )

    sample["percentile"] = calculate_percentile_rank(
        sample,
        "roe",
        True,
    )

    print(sample)

    print()

    print("DEBT TO EQUITY TEST")

    sample = pd.DataFrame(
        {
            "de": [
                0.2,
                0.5,
                1,
                2,
                5,
            ]
        }
    )

    sample["percentile"] = calculate_percentile_rank(
        sample,
        "de",
        False,
    )

    print(sample)

    print()

    percentile_df = calculate_all_percentiles(
        merged,
    )
    

    print("PEER PERCENTILES")

    print(
        percentile_df.head(20)
    )

    print()

    print("Total Rows:")

    print(
        len(percentile_df)
    )

    save_peer_percentiles(

    percentile_df,

    DB_PATH,

)

print()

print("Saved to SQLite.")