import sqlite3
from pathlib import Path

import pandas as pd

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "nifty100.db"

REPORT_DIR = BASE_DIR / "reports"

SECTOR_DIR = REPORT_DIR / "sector"

SECTOR_DIR.mkdir(
    parents=True,
    exist_ok=True
)

conn = sqlite3.connect(DB_PATH)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

cashflow_intelligence = pd.read_excel(
    BASE_DIR / "output" / "cashflow_intelligence.xlsx"
)



sector_table = pd.read_sql(
    "SELECT * FROM sectors",
    conn
)

conn.close()


sector_names = sorted(
    sector_table["broad_sector"].dropna().unique()
)


def generate_sector_report(sector_name):
    

    pdf_path = SECTOR_DIR / f"{sector_name}_report.pdf"

    pdf = canvas.Canvas(
        str(pdf_path),
        pagesize=A4
    )

    pdf.setFillColor(colors.HexColor("#0B1F3A"))

    pdf.rect(
        0,
        770,
        595,
        72,
        fill=True
    )

    pdf.setFillColor(colors.white)

    pdf.setFont(
        "Helvetica-Bold",
        22
    )

    pdf.drawString(
        40,
        800,
        f"{sector_name} Sector Report"
    )

    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.drawString(
        40,
        780,
        "N100 Financial Intelligence"
    )

    pdf.setFillColor(colors.black)

    # ======================================================
    # GET COMPANIES IN THIS SECTOR
    # ======================================================

    sector_data = sector_table[
    sector_table["broad_sector"] == sector_name
    ]

    company_ids = sector_data["company_id"].tolist()

    # ======================================================
    # GET LATEST FINANCIAL RATIOS
    # ======================================================

    latest = (
    ratios
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
     )

    latest = latest[
    latest["company_id"].isin(company_ids)
    ]

    # ======================================================
    # SUMMARY KPIs
    # ======================================================

    company_count = len(company_ids)

    median_roe = latest["return_on_equity_pct"].median()

    median_de = latest["debt_to_equity"].median()

    median_revenue = latest["revenue_cagr_5yr"].median()

    median_pat = latest["pat_cagr_5yr"].median()

        # ======================================================
    # COMPANY TABLE DATA
    # ======================================================

    company_table = latest.merge(
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

    company_table = company_table.sort_values(
        "company_name"
    )

    # ======================================================
    # SUMMARY SECTION
    # ======================================================

    pdf.setFont(
        "Helvetica-Bold",
        16
    )

    pdf.drawString(
        40,
        730,
        "Sector Summary"
    )

    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.drawString(
        40,
        700,
        f"Total Companies : {company_count}"
    )

    pdf.drawString(
        40,
        675,
        f"Median ROE : {median_roe:.2f}%"
    )

    pdf.drawString(
        40,
        650,
        f"Median Debt/Equity : {median_de:.2f}"
    )

    pdf.drawString(
        40,
        625,
        f"Median Revenue CAGR : {median_revenue:.2f}%"
    )

    pdf.drawString(
        40,
        600,
        f"Median PAT CAGR : {median_pat:.2f}%"
    )

        # ======================================================
    # COMPANY COMPARISON TABLE
    # ======================================================

    pdf.setFont(
        "Helvetica-Bold",
        15
    )

    pdf.drawString(
        40,
        560,
        "Company Comparison"
    )

    pdf.setFont(
        "Helvetica-Bold",
        9
    )

    y = 540

    pdf.drawString(40, y, "Company")
    pdf.drawString(210, y, "ROE")
    pdf.drawString(260, y, "D/E")
    pdf.drawString(320, y, "Rev CAGR")
    pdf.drawString(420, y, "PAT CAGR")
    pdf.line(
    40,
    y - 5,
    540,
    y - 5
    )

    pdf.setFont(
        "Helvetica",
        8
    )

    y = 520

    for _, row in company_table.iterrows():

        pdf.drawString(
            40,
            y,
            str(row["company_name"])[:28]
        )

        pdf.drawRightString(
            240,
            y,
            f"{row['return_on_equity_pct']:.1f}"
        )

        pdf.drawRightString(
            290,
            y,
            f"{row['debt_to_equity']:.2f}"
        )

        pdf.drawRightString(
            390,
            y,
            f"{row['revenue_cagr_5yr']:.1f}%"
        )

        pdf.drawRightString(
            520,
            y,
            f"{row['pat_cagr_5yr']:.1f}%"
        )

        y -= 18

        if y < 40:
            break



    pdf.save()

    print(f"{sector_name} report generated")


if __name__ == "__main__":

    for sector in sector_names:

        print(f"Generating {sector}...")

        generate_sector_report(sector)

    print()

    print("=" * 60)
    print("ALL SECTOR REPORTS GENERATED")
    print("=" * 60)