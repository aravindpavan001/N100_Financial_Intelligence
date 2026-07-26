import sqlite3
from pathlib import Path

import pandas as pd

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "nifty100.db"

REPORT_DIR = BASE_DIR / "reports"

PORTFOLIO_DIR = REPORT_DIR / "portfolio"

OUTPUT_DIR = BASE_DIR / "output"

PORTFOLIO_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ==========================================================
# PDF CONSTANTS
# ==========================================================

PAGE_WIDTH, PAGE_HEIGHT = A4

LEFT = 40
RIGHT = PAGE_WIDTH - 40

TOP = PAGE_HEIGHT - 40

BOTTOM = 40

HEADER_HEIGHT = 70

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

cashflow = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

sector_table = pd.read_sql(
    "SELECT * FROM sectors",
    conn
)

conn.close()

# ==========================================================
# LOAD OUTPUT FILES
# ==========================================================

cashflow_intelligence = pd.read_excel(
    OUTPUT_DIR / "cashflow_intelligence.xlsx"
)

# ==========================================================
# SORT COMPANIES
# ==========================================================

companies = companies.sort_values(
    "id"
).reset_index(drop=True)

# ==========================================================
# LOAD COMPANY DATA
# ==========================================================

def load_company(company_id):

    company = companies.loc[
        companies["id"] == company_id
    ].iloc[0]

    ratios = (
        financial_ratios[
            financial_ratios["company_id"] == company_id
        ]
        .sort_values("year")
        .reset_index(drop=True)
    )

    cash = (
        cashflow[
            cashflow["company_id"] == company_id
        ]
        .sort_values("year")
        .reset_index(drop=True)
    )

    sector = (
        sector_table[
            sector_table["company_id"] == company_id
        ]
        .reset_index(drop=True)
    )

    intelligence = (
        cashflow_intelligence[
            cashflow_intelligence["company_id"] == company_id
        ]
        .reset_index(drop=True)
    )

    return {

        "company": company,

        "ratios": ratios,

        "cash": cash,

        "sector": sector,

        "intelligence": intelligence

    }

# ==========================================================
# TREND ARROW
# ==========================================================

def trend_arrow(current, previous):

    if pd.isna(current) or pd.isna(previous):
        return "-"

    if abs(current - previous) <= 2:
        return "→"

    if current > previous:
        return "↑"

    return "↓"


# ==========================================================
# PORTFOLIO SUMMARY PDF
# ==========================================================

def generate_portfolio_summary():

    pdf_path = PORTFOLIO_DIR / "portfolio_summary.pdf"

    pdf = canvas.Canvas(
        str(pdf_path),
        pagesize=A4
    )

    page_no = 1

    for _, row in companies.iterrows():

        company_id = row["id"]

        data = load_company(company_id)

        company = data["company"]

        ratios = data["ratios"]

        sector = data["sector"]

        cash = data["cash"]

        intelligence = data["intelligence"]

        if len(ratios) < 2:
            continue

        latest = ratios.iloc[-1]

        previous = ratios.iloc[-2]

        # ==================================================
        # HEADER
        # ==================================================

        pdf.setFillColor(colors.HexColor("#0B1F3A"))

        pdf.rect(
            0,
            PAGE_HEIGHT - HEADER_HEIGHT,
            PAGE_WIDTH,
            HEADER_HEIGHT,
            fill=True,
            stroke=False
        )

        pdf.setFillColor(colors.white)

        pdf.setFont(
            "Helvetica-Bold",
            22
        )

        pdf.drawString(
            LEFT,
            PAGE_HEIGHT - 35,
            company["company_name"]
        )

        pdf.setFont(
            "Helvetica",
            12
        )

        pdf.drawString(
            LEFT,
            PAGE_HEIGHT - 55,
            f"Ticker : {company_id}"
        )

        if len(sector) > 0:

            pdf.drawRightString(
             RIGHT,
             PAGE_HEIGHT - 55,
            f"Sector : {sector.iloc[0]['broad_sector']}"
            )

            pdf.drawRightString(
            RIGHT,
            PAGE_HEIGHT - 72,
            f"Market Cap : {sector.iloc[0]['market_cap_category']}"
            )

        pdf.setFillColor(colors.black)

        # ==================================================
        # KPI TITLE
        # ==================================================

        pdf.setFont(
            "Helvetica-Bold",
            18
        )

        pdf.drawString(
            LEFT,
            720,
            "Portfolio KPI Summary"
        )

        pdf.line(
          LEFT,
          710,
          RIGHT,
          710
          )

        # ==================================================
        # KPI DATA
        # ==================================================

        fcf = "-"

        if len(cash) > 0:

            fcf = f"Rs. {cash.iloc[-1]['operating_activity']:,.0f} Cr"

        quality = "-"

        if len(intelligence) > 0:

            quality = str(
                intelligence.iloc[0]["capital_allocation_label"]
            )

        kpis = [

            (
                "ROE",
                f"{latest['return_on_equity_pct']:.2f}%",
                trend_arrow(
                    latest["return_on_equity_pct"],
                    previous["return_on_equity_pct"]
                )
            ),

            (
                "Debt / Equity",
                f"{latest['debt_to_equity']:.2f}",
                trend_arrow(
                    latest["debt_to_equity"],
                    previous["debt_to_equity"]
                )
            ),

            (
                "Revenue CAGR",
                f"{latest['revenue_cagr_5yr']:.2f}%",
                trend_arrow(
                    latest["revenue_cagr_5yr"],
                    previous["revenue_cagr_5yr"]
                )
            ),

            (
                "PAT CAGR",
                f"{latest['pat_cagr_5yr']:.2f}%",
                trend_arrow(
                    latest["pat_cagr_5yr"],
                    previous["pat_cagr_5yr"]
                )
            ),

            (
                "Free Cash Flow",
                fcf,
                "-"
            ),

            (
                "Capital Allocation",
                quality,
                "-"
            )

        ]

        # ==================================================
        # DRAW KPI TABLE
        # ==================================================

        y = 670

        pdf.setFont(
            "Helvetica-Bold",
            12
        )

        pdf.drawString(
            50,
            y,
            "KPI"
        )

        pdf.drawString(
            240,
            y,
            "Value"
        )

        pdf.drawString(
            420,
            y,
            "Trend"
        )

        pdf.line(
            40,
            y - 5,
            550,
            y - 5
        )

        y -= 30


        for name, value, arrow in kpis:
            pdf.setFont(
            "Helvetica",
            11
            )


            pdf.drawString(
                50,
                y,
                name
            )

            pdf.setFont(
             "Helvetica",
             11
             )


            pdf.drawString(
                240,
                y,
                str(value)
            )

            if arrow == "↑":

             pdf.setFillColor(colors.green)

            elif arrow == "↓":

             pdf.setFillColor(colors.red)

            elif arrow == "→":

             pdf.setFillColor(colors.orange)

            else:

             pdf.setFillColor(colors.grey)

            pdf.drawString(
             430,
              y,
             arrow
              )

            pdf.setFillColor(colors.black)

            y -= 40

        pdf.setFont(
            "Helvetica",
            9
        )

        pdf.drawString(
             LEFT,
             20,
             f"Page {page_no} of {len(companies)}"
        )

        pdf.drawRightString(
            RIGHT,
            20,
            "N100 Financial Intelligence"
        )

        pdf.showPage()
        page_no += 1

    pdf.save()

    print()

    print("=" * 60)
    print("PORTFOLIO SUMMARY CREATED")
    print("=" * 60)
    print(pdf_path)


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("GENERATING PORTFOLIO SUMMARY")
    print("=" * 60)

    generate_portfolio_summary()

    print()
    print("=" * 60)
    print("PORTFOLIO SUMMARY GENERATED SUCCESSFULLY")
    print("=" * 60)