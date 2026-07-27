from fastapi import (
    APIRouter,
    HTTPException,
    Query
)

import pandas as pd

from src.api.database import get_db_connection


router = APIRouter(
    tags=["Screener"]
)

# ==========================================================
# LOAD TABLES
# ==========================================================

def load_table(table_name):

    conn = get_db_connection()

    df = pd.read_sql(

        f"SELECT * FROM {table_name}",

        conn

    )

    conn.close()

    return df


financial_ratios = load_table("financial_ratios")

companies = load_table("companies")

sectors = load_table("sectors")

market_cap = load_table("market_cap")


# ==========================================================
# LATEST YEAR
# ==========================================================

latest_ratios = (

    financial_ratios

    .sort_values("year")

    .groupby("company_id")

    .tail(1)

)

latest_market = (

    market_cap

    .sort_values("year")

    .groupby("company_id")

    .tail(1)

)


# ==========================================================
# SCREENER
# ==========================================================

@router.get("/screener")
def screener(

    min_roe: float | None = Query(None),

    max_de: float | None = Query(None),

    min_fcf: float | None = Query(None),

    sector: str | None = Query(None),

    min_rev_cagr_5yr: float | None = Query(None),

    min_pat_cagr_5yr: float | None = Query(None),

    max_pe: float | None = Query(None)

):

    # ======================================================
    # INPUT VALIDATION
    # ======================================================

    if min_roe is not None and min_roe < 0:

        raise HTTPException(

            status_code=400,

            detail="min_roe cannot be negative"

        )

    if max_de is not None and max_de < 0:

        raise HTTPException(

            status_code=400,

            detail="max_de cannot be negative"

        )

    if max_pe is not None and max_pe < 0:

        raise HTTPException(

            status_code=400,

            detail="max_pe cannot be negative"

        )

    # ======================================================
    # MERGE
    # ======================================================

    df = latest_ratios.merge(

        companies,

        left_on="company_id",

        right_on="id",

        how="left"

    )

    df = df.merge(

        sectors,

        on="company_id",

        how="left"

    )

    df = df.merge(

        latest_market[

            [

                "company_id",

                "pe_ratio"

            ]

        ],

        on="company_id",

        how="left"

    )

    # ======================================================
    # FILTERS
    # ======================================================

    if min_roe is not None:

        df = df[

            df["return_on_equity_pct"]

            >=

            min_roe

        ]

    if max_de is not None:

        df = df[

            df["debt_to_equity"]

            <=

            max_de

        ]

    if min_fcf is not None:

        df = df[

            df["free_cash_flow_cr"]

            >=

            min_fcf

        ]

    if sector:

        df = df[

            df["broad_sector"]

            .str.lower()

            ==

            sector.lower()

        ]

    if min_rev_cagr_5yr is not None:

        df = df[

            df["revenue_cagr_5yr"]

            >=

            min_rev_cagr_5yr

        ]

    if min_pat_cagr_5yr is not None:

        df = df[

            df["pat_cagr_5yr"]

            >=

            min_pat_cagr_5yr

        ]

    if max_pe is not None:

        df = df[

            df["pe_ratio"]

            <=

            max_pe

        ]

    # ======================================================
    # OUTPUT
    # ======================================================

    output = df[

        [

            "company_id",

            "company_name",

            "broad_sector",

            "composite_quality_score",

            "return_on_equity_pct",

            "debt_to_equity",

            "revenue_cagr_5yr",

            "pat_cagr_5yr",

            "pe_ratio",

            "free_cash_flow_cr"

        ]

    ].copy()

    output = output.sort_values(

        "composite_quality_score",

        ascending=False

    )

    output = output.astype(object)

    output = output.where(

        pd.notnull(output),

        None

    )

    return output.to_dict(

        orient="records"

    )