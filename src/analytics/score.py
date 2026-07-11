import numpy as np
import pandas as pd
import sqlite3

def winsorize_series(series):
    """
    Clip values between
    P10 and P90.
    """

    lower = series.quantile(0.10)

    upper = series.quantile(0.90)

    return series.clip(
        lower=lower,
        upper=upper,
    )


def normalize_metric(series):
    """
    Scale metric to 0-100.
    """

    series = winsorize_series(series)

    minimum = series.min()

    maximum = series.max()

    if minimum == maximum:

        return pd.Series(
            50,
            index=series.index,
        )

    return (
        (series - minimum)
        /
        (maximum - minimum)
    ) * 100

def normalize_by_sector(
    df,
    column,
):
    """
    Normalize one metric
    inside each sector.
    """

    result = pd.Series(
        index=df.index,
        dtype=float,
    )

    for sector in df["broad_sector"].dropna().unique():

        mask = (
            df["broad_sector"]
            == sector
        )

        result.loc[mask] = normalize_metric(
            df.loc[
                mask,
                column,
            ]
        )

    return result

def calculate_profitability_score(df):
    """
    Profitability Score
    """

    roe = normalize_by_sector(
    df,
    "return_on_equity_pct",
)

    npm = normalize_by_sector(
    df,
    "net_profit_margin_pct",
)

    opm = normalize_by_sector(
    df,
    "operating_profit_margin_pct",
)

    df["profitability_score"] = (

        roe * 0.50

        + npm * 0.25

        + opm * 0.25

    )

    return df    

def calculate_cash_quality_score(df):
    """
          Cash Quality
    """

    fcf = normalize_by_sector(
    df,
    "free_cash_flow_cr",
    )

    icr = normalize_by_sector(
    df,
    "interest_coverage",
     )

    df["cash_quality_score"] = (

        fcf * 0.70

        + icr * 0.30

    )

    return df

def calculate_growth_score(df):
    """
    Growth
    """

    revenue = normalize_by_sector(
    df,
    "revenue_cagr_5yr",
)

    pat = normalize_by_sector(
    df,
    "pat_cagr_5yr",
)

    eps = normalize_by_sector(
    df,
    "eps_cagr_5yr",
)

    df["growth_score"] = (

        revenue * 0.40

        + pat * 0.30

        + eps * 0.30

    )

    return df

def calculate_leverage_score(df):
    """
    Lower Debt-to-Equity is better.
    """

    debt = normalize_by_sector(
    df,
    "debt_to_equity",
)

    turnover = normalize_by_sector(
    df,
    "asset_turnover",
)  
    df["leverage_score"] = (

        debt * 0.70

        + turnover * 0.30

    )

    return df
def calculate_composite_score(df):
    """
    Final Composite Quality Score
    """

    df["composite_quality_score"] = (

        df["profitability_score"] * 0.35

        + df["cash_quality_score"] * 0.30

        + df["growth_score"] * 0.20

        + df["leverage_score"] * 0.15

    )

    return df

if __name__ == "__main__":

    sample = pd.DataFrame({

        "return_on_equity_pct": [10,20,30],

        "net_profit_margin_pct": [5,15,25],

        "operating_profit_margin_pct": [10,20,30],

        "free_cash_flow_cr": [100,500,1000],

        "interest_coverage": [2,5,10],

        "revenue_cagr_5yr": [5,10,20],

        "pat_cagr_5yr": [5,15,25],

        "eps_cagr_5yr": [8,12,18],

        "debt_to_equity": [2,1,0.2],

        "asset_turnover": [0.5,1,2],

    })

    sample = calculate_profitability_score(sample)

    sample = calculate_cash_quality_score(sample)

    sample = calculate_growth_score(sample)

    sample = calculate_leverage_score(sample)

    sample = calculate_composite_score(sample)

    print()

    print(sample[
    [
        "profitability_score",
        "cash_quality_score",
        "growth_score",
        "leverage_score",
        "composite_quality_score",
    ]
])
    