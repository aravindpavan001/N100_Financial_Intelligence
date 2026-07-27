import pandas as pd

from fastapi import (
    APIRouter,
    HTTPException
)

from pathlib import Path


router = APIRouter(
    tags=["Portfolio"]
)

BASE_DIR = Path(__file__).resolve().parents[3]

OUTPUT_DIR = BASE_DIR / "output"

PORTFOLIO_FILE = OUTPUT_DIR / "portfolio_stats.csv"


@router.get("/portfolio/stats")
def get_portfolio_stats():

    if not PORTFOLIO_FILE.exists():

        raise HTTPException(

            status_code=404,

            detail="portfolio_stats.csv not found."

        )

    df = pd.read_csv(PORTFOLIO_FILE)

    df = df.astype(object)

    df = df.where(

        pd.notnull(df),

        None

    )

    return df.to_dict(

        orient="records"

    )