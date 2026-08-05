from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

from src.api.database import get_db_connection

router = APIRouter(tags=["Companies"])

BASE_DIR = Path(__file__).resolve().parents[3]

REPORT_DIR = BASE_DIR / "reports" / "tearsheets"


# ==========================================================
# LOAD TABLE
# ==========================================================


def load_table(table_name):

    conn = get_db_connection()

    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

    conn.close()

    return df


companies = load_table("companies")

sectors = load_table("sectors")

profit_loss = load_table("profitandloss")

balance_sheet = load_table("balancesheet")

cashflow = load_table("cashflow")

ratios = load_table("financial_ratios")

financial_ratios = load_table("financial_ratios")


def get_company(company_id: str):

    company = companies[companies["id"].str.upper() == company_id.upper()]

    if company.empty:

        raise HTTPException(status_code=404, detail="Company not found")

    return company.iloc[0]


# ==========================================================
# GET COMPANY LIST
# ==========================================================


@router.get("/companies")
def get_companies(
    sector: str | None = Query(None),
    market_cap_category: str | None = Query(None),
    search: str | None = Query(None),
):

    df = companies.merge(sectors, left_on="id", right_on="company_id", how="left")

    # -----------------------------
    # Sector Filter
    # -----------------------------
    if sector:

        df = df[df["broad_sector"].fillna("").str.lower() == sector.lower()]

    # -----------------------------
    # Market Cap Filter
    # -----------------------------
    if market_cap_category:

        df = df[
            df["market_cap_category"].fillna("").str.lower()
            == market_cap_category.lower()
        ]

    # -----------------------------
    # Search Filter
    # -----------------------------
    if search:

        text = search.lower()

        df = df[
            df["company_name"].fillna("").str.lower().str.contains(text)
            | df["id_x"].astype(str).str.lower().str.contains(text)
        ]

    # -----------------------------
    # Select Required Columns
    # -----------------------------
    output = df[
        [
            "id_x",
            "company_name",
            "broad_sector",
            "sub_sector",
            "roe_percentage",
            "roce_percentage",
        ]
    ].copy()

    # -----------------------------
    # Rename ID
    # -----------------------------
    output.rename(columns={"id_x": "id"}, inplace=True)

    # -----------------------------
    # Replace NaN with None
    # -----------------------------
    output = output.astype(object)
    output = output.where(pd.notnull(output), None)

    return output.to_dict(orient="records")


@router.get("/companies/{ticker}")
def company_profile(ticker: str):

    company = get_company(ticker)

    sector = sectors[sectors["company_id"] == ticker]

    latest_ratio = ratios[ratios["company_id"] == ticker].sort_values("year").tail(1)

    response = {
        "company": company.to_dict(),
        "sector": (sector.iloc[0].to_dict() if not sector.empty else {}),
        "latest_ratios": (
            latest_ratio.iloc[0].to_dict() if not latest_ratio.empty else {}
        ),
    }

    return response


# ==========================================================
# COMPANY PROFIT & LOSS
# ==========================================================


@router.get("/companies/{ticker}/pl")
def company_profit_loss(
    ticker: str, from_year: str | None = Query(None), to_year: str | None = Query(None)
):

    df = profit_loss[profit_loss["company_id"].str.upper() == ticker.upper()].copy()

    if df.empty:

        raise HTTPException(status_code=404, detail="Profit & Loss data not found")

    if from_year:

        df = df[df["year"] >= from_year]

    if to_year:

        df = df[df["year"] <= to_year]

    df = df.sort_values("year")

    df = df.astype(object)

    df = df.where(pd.notnull(df), None)

    return df.to_dict(orient="records")


# ==========================================================
# COMPANY BALANCE SHEET
# ==========================================================


@router.get("/companies/{ticker}/bs")
def company_balance_sheet(
    ticker: str, from_year: str | None = Query(None), to_year: str | None = Query(None)
):

    df = balance_sheet[balance_sheet["company_id"].str.upper() == ticker.upper()].copy()

    if df.empty:

        raise HTTPException(status_code=404, detail="Balance Sheet data not found")

    if from_year:

        df = df[df["year"] >= from_year]

    if to_year:

        df = df[df["year"] <= to_year]

    df = df.sort_values("year")

    df = df.astype(object)

    df = df.where(pd.notnull(df), None)

    return df.to_dict(orient="records")


# ==========================================================
# COMPANY CASH FLOW
# ==========================================================


@router.get("/companies/{ticker}/cashflow")
def company_cashflow(
    ticker: str, from_year: str | None = Query(None), to_year: str | None = Query(None)
):

    df = cashflow[cashflow["company_id"].str.upper() == ticker.upper()].copy()

    if df.empty:

        raise HTTPException(status_code=404, detail="Cash Flow data not found")

    if from_year:

        df = df[df["year"] >= from_year]

    if to_year:

        df = df[df["year"] <= to_year]

    df = df.sort_values("year")

    df = df.astype(object)

    df = df.where(pd.notnull(df), None)

    return df.to_dict(orient="records")


# ==========================================================
# COMPANY RATIOS
# ==========================================================


@router.get("/companies/{ticker}/ratios")
def company_ratios(ticker: str, year: str | None = Query(None)):

    df = financial_ratios[
        financial_ratios["company_id"].str.upper() == ticker.upper()
    ].copy()

    if df.empty:

        raise HTTPException(status_code=404, detail="Financial Ratios not found")

    print(df["year"].unique())

    if year:

        df = df[df["year"] == year]

        if df.empty:

            raise HTTPException(status_code=404, detail="Requested year not found")

    df = df.sort_values("year")

    df = df.astype(object)

    df = df.where(pd.notnull(df), None)

    return df.to_dict(orient="records")


# ==========================================================
# COMPANY TEARSHEET PDF
# ==========================================================


@router.get("/companies/{ticker}/tearsheet")
def company_tearsheet(ticker: str):

    possible_files = [
        REPORT_DIR / f"{ticker.upper()}.pdf",
        REPORT_DIR / f"{ticker.upper()}_tearsheet.pdf",
        REPORT_DIR / f"{ticker.upper()}_Tearsheet.pdf",
        REPORT_DIR / f"{ticker.upper()} Tearsheet.pdf",
    ]

    pdf_file = None

    for file in possible_files:

        if file.exists():

            pdf_file = file

            break

    if pdf_file is None:

        raise HTTPException(status_code=404, detail="Tearsheet PDF not found")

    return FileResponse(
        path=str(pdf_file), media_type="application/pdf", filename=pdf_file.name
    )
