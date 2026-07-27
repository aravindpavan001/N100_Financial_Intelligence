import pandas as pd

from fastapi import (
    APIRouter,
    HTTPException
)

from src.api.database import get_db_connection


router = APIRouter(
    tags=["Sectors"]
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


companies = load_table("companies")

financial_ratios = load_table("financial_ratios")

market_cap = load_table("market_cap")

sectors = load_table("sectors")


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
# GET ALL SECTORS
# ==========================================================

@router.get("/sectors")

def get_sectors():

    df = latest_ratios.merge(

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

    summary = (

        df

        .groupby("broad_sector")

        .agg(

            company_count=("company_id", "count"),

            median_roe=("return_on_equity_pct", "median"),

            median_pe=("pe_ratio", "median"),

            median_de=("debt_to_equity", "median")

        )

        .reset_index()

        .sort_values("broad_sector")

    )

    summary = summary.astype(object)

    summary = summary.where(

        pd.notnull(summary),

        None

    )

    return summary.to_dict(

        orient="records"

    )


# ==========================================================
# GET COMPANIES INSIDE A SECTOR
# ==========================================================

@router.get("/sectors/{sector}/companies")

def get_sector_companies(

    sector: str

):

    df = companies.merge(

        sectors,

        left_on="id",

        right_on="company_id",

        how="left",

        suffixes=("", "_sector")

    )


    df = df.merge(

        latest_ratios[

            [

                "company_id",

                "return_on_equity_pct",

                "debt_to_equity",

                "composite_quality_score"

            ]

        ],

        left_on="id",

        right_on="company_id",

        how="left"

    )

    filtered = df[

        df["broad_sector"]

        .str.lower()

        ==

        sector.lower()

    ]

    if filtered.empty:

        raise HTTPException(

            status_code=404,

            detail="Sector not found."

        )

    output = filtered[

        [

            "id",

            "company_name",

            "broad_sector",

            "sub_sector",

            "return_on_equity_pct",

            "debt_to_equity",

            "composite_quality_score"

        ]

    ].copy()

    output = output.astype(object)

    output = output.where(

        pd.notnull(output),

        None

    )

    return output.to_dict(

        orient="records"

    )