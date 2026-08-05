import pandas as pd
from fastapi import APIRouter, HTTPException

from src.api.database import get_db_connection

router = APIRouter(tags=["Peers"])

# ==========================================================
# LOAD TABLE
# ==========================================================


def load_table(table_name):

    conn = get_db_connection()

    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

    conn.close()

    return df


companies = load_table("companies")

peer_groups = load_table("peer_groups")

peer_percentiles = load_table("peer_percentiles")

financial_ratios = load_table("financial_ratios")


# ==========================================================
# LATEST RATIOS
# ==========================================================

latest_ratios = financial_ratios.sort_values("year").groupby("company_id").tail(1)


# ==========================================================
# GET PEER GROUP
# ==========================================================


@router.get("/peers/{group_name}")
def get_peer_group(group_name: str):

    peers = peer_groups[
        peer_groups["peer_group_name"].str.lower() == group_name.lower()
    ]

    if peers.empty:

        raise HTTPException(status_code=404, detail="Peer group not found.")

    df = peers.merge(companies, left_on="company_id", right_on="id", how="left")

    latest_year = peer_percentiles["year"].sort_values().iloc[-1]

    percentile = peer_percentiles[
        (peer_percentiles["peer_group_name"].str.lower() == group_name.lower())
        & (peer_percentiles["year"] == latest_year)
    ]

    result = []

    for _, company in df.iterrows():

        cid = company["company_id"]

        metrics = percentile[percentile["company_id"] == cid]

        metric_dict = {}

        for _, row in metrics.iterrows():

            metric_dict[row["metric"]] = {
                "value": row["metric_value"],
                "percentile": row["percentile_rank"],
            }

        result.append(
            {
                "company_id": cid,
                "company_name": company["company_name"],
                "benchmark": bool(company["is_benchmark"]),
                "metrics": metric_dict,
            }
        )

    return result


# ==========================================================
# COMPANY VS PEERS
# ==========================================================


@router.get("/companies/{ticker}/peers/compare")
def compare_with_peers(ticker: str):

    ticker = ticker.upper()

    peer = peer_groups[peer_groups["company_id"] == ticker]

    if peer.empty:

        raise HTTPException(status_code=404, detail="Company not found.")

    group_name = peer.iloc[0]["peer_group_name"]

    benchmark = peer_groups[
        (peer_groups["peer_group_name"] == group_name)
        & (peer_groups["is_benchmark"] == 1)
    ].iloc[0]["company_id"]

    peer_members = peer_groups[peer_groups["peer_group_name"] == group_name][
        "company_id"
    ]

    ratios = latest_ratios[latest_ratios["company_id"].isin(peer_members)]

    metrics = [
        "return_on_equity_pct",
        "operating_profit_margin_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
    ]

    peer_average = {}

    for metric in metrics:

        peer_average[metric] = round(ratios[metric].mean(), 2)

    company = ratios[ratios["company_id"] == ticker]

    benchmark_company = ratios[ratios["company_id"] == benchmark]

    if company.empty:

        raise HTTPException(status_code=404, detail="Company ratios not found.")

    company_metrics = {}

    benchmark_metrics = {}

    for metric in metrics:

        company_metrics[metric] = company.iloc[0][metric]

        benchmark_metrics[metric] = benchmark_company.iloc[0][metric]

    return {
        "peer_group": group_name,
        "company": {"ticker": ticker, "metrics": company_metrics},
        "peer_average": peer_average,
        "benchmark": {"ticker": benchmark, "metrics": benchmark_metrics},
    }
