import sqlite3
from pathlib import Path
import textwrap

import pandas as pd
import matplotlib.pyplot as plt

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"

REPORT_DIR = BASE_DIR / "reports"

SAMPLE_DIR = REPORT_DIR / "sample"

CHART_DIR = REPORT_DIR / "charts"

SAMPLE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

CHART_DIR.mkdir(
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
BOTTOM = 35

HEADER_HEIGHT = 70

CARD_WIDTH = 155
CARD_HEIGHT = 60

CARD_GAP_X = 18
CARD_GAP_Y = 18

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

profitandloss = pd.read_sql(
    "SELECT * FROM profitandloss",
    conn
)

balancesheet = pd.read_sql(
    "SELECT * FROM balancesheet",
    conn
)

cashflow = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

conn.close()

# ==========================================================
# LOAD OUTPUT FILES
# ==========================================================

cashflow_intelligence = pd.read_excel(
    OUTPUT_DIR / "cashflow_intelligence.xlsx"
)

pros_cons = pd.read_csv(
    OUTPUT_DIR / "pros_cons_generated.csv"
)

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

    profit = (
        profitandloss[
            profitandloss["company_id"] == company_id
        ]
        .sort_values("year")
        .reset_index(drop=True)
    )

    balance = (
        balancesheet[
            balancesheet["company_id"] == company_id
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

    capital = (
        cashflow_intelligence[
            cashflow_intelligence["company_id"] == company_id
        ]
        .reset_index(drop=True)
    )

    company_pc = pros_cons[
        pros_cons["company_id"] == company_id
    ]

    pros = (
        company_pc[
            company_pc["type"] == "Pro"
        ]
        .reset_index(drop=True)
    )

    cons = (
        company_pc[
            company_pc["type"] == "Con"
        ]
        .reset_index(drop=True)
    )

    return {
        "company": company,
        "ratios": ratios,
        "profit": profit,
        "balance": balance,
        "cash": cash,
        "capital": capital,
        "pros": pros,
        "cons": cons
    }

# ==========================================================
# PDF HELPER FUNCTIONS
# ==========================================================

def draw_title(pdf, text, y):

    pdf.setFont(
        "Helvetica-Bold",
        16
    )

    pdf.setFillColor(colors.black)

    pdf.drawString(
        LEFT,
        y,
        text
    )


def draw_divider(pdf, y):

    pdf.line(
        LEFT,
        y,
        RIGHT,
        y
    )


def wrap_text(text, width=70):

    return textwrap.wrap(
        str(text),
        width=width
    )


# ==========================================================
# CHART FUNCTIONS
# ==========================================================

def create_revenue_chart(profit, company_id):

    chart_path = CHART_DIR / f"{company_id}_revenue.png"

    chart = profit.copy()

    plt.figure(figsize=(5, 3))

    plt.bar(
        chart["year"],
        chart["sales"]
    )

    plt.title("Revenue (10 Years)")
    plt.ylabel("₹ Crores")
    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        chart_path,
        dpi=200
    )

    plt.close()

    return chart_path


# ==========================================================

def create_profit_chart(profit, company_id):

    chart_path = CHART_DIR / f"{company_id}_profit.png"

    chart = profit.copy()

    plt.figure(figsize=(5,3))

    plt.bar(
        chart["year"],
        chart["net_profit"]
    )

    plt.title("Net Profit (10 Years)")
    plt.ylabel("₹ Crores")
    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        chart_path,
        dpi=200
    )

    plt.close()

    return chart_path


# ==========================================================

def create_roe_roce_chart(ratios, company, company_id):

    chart_path = CHART_DIR / f"{company_id}_roe_roce.png"

    chart = ratios.copy()

    # ROCE is not available year-wise in financial_ratios.
    # Use the latest company ROCE as a constant line.
    roce = company["roce_percentage"]

    roce_values = [roce] * len(chart)

    plt.figure(figsize=(8, 3.5))

    plt.plot(
        chart["year"],
        chart["return_on_equity_pct"],
        marker="o",
        linewidth=2,
        label="ROE"
    )

    plt.plot(
        chart["year"],
        roce_values,
        marker="s",
        linewidth=2,
        linestyle="--",
        label="ROCE"
    )

    plt.title("ROE vs ROCE")

    plt.legend()

    plt.grid(True)

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        chart_path,
        dpi=200
    )

    plt.close()

    return chart_path

# ==========================================================

def create_balance_chart(balance, company_id):

    chart_path = CHART_DIR / f"{company_id}_balance.png"

    chart = balance.copy()

    chart["equity"] = (
        chart["equity_capital"]
        +
        chart["reserves"]
    )

    plt.figure(figsize=(8,3.5))

    plt.bar(
        chart["year"],
        chart["equity"],
        label="Equity"
    )

    plt.bar(
        chart["year"],
        chart["borrowings"],
        bottom=chart["equity"],
        label="Borrowings"
    )

    chart["other_liabilities"] = (
    chart["total_liabilities"]
    -
    chart["equity"]
    -
    chart["borrowings"]
)

    plt.bar(
        chart["year"],
        chart["other_liabilities"],
        bottom=
        chart["equity"]
        +
        chart["borrowings"],
    label="Other Liabilities"
    )

    plt.title("Balance Sheet Composition")

    plt.legend()

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        chart_path,
        dpi=200
    )

    plt.close()

    return chart_path


# ==========================================================

def create_cashflow_chart(cash, company_id):

    chart_path = CHART_DIR / f"{company_id}_cashflow.png"

    latest = cash.iloc[-1]

    labels = [
        "CFO",
        "CFI",
        "CFF",
        "Net Cash"
    ]

    values = [

        latest["operating_activity"],

        latest["investing_activity"],

        latest["financing_activity"],

        latest["net_cash_flow"]

    ]

    plt.figure(figsize=(6,3.5))

    bars = plt.bar(
        labels,
        values
    )

    for value, bar in zip(values, bars):

        plt.text(
            bar.get_x() + bar.get_width()/2,
            value,
            f"{value:,.0f}",
            ha="center",
            va="bottom",
            fontsize=8
        )

    plt.title("Latest Cash Flow")

    plt.grid(axis="y")

    plt.tight_layout()

    plt.savefig(
        chart_path,
        dpi=200
    )

    plt.close()

    return chart_path


# ==========================================================
# TEST CHARTS
# ==========================================================

if __name__ == "__main__":

    data = load_company("TCS")

    create_revenue_chart(
        data["profit"],
        "TCS"
    )

    create_profit_chart(
        data["profit"],
        "TCS"
    )

    create_roe_roce_chart(
    data["ratios"],
    data["company"],
    "TCS"
    )

    create_balance_chart(
        data["balance"],
        "TCS"
    )

    create_cashflow_chart(
        data["cash"],
        "TCS"
    )

    print()
    print("=" * 60)
    print("ALL CHARTS CREATED")
    print("=" * 60)

    # ==========================================================
# GENERATE TEARSHEET
# ==========================================================

def generate_tearsheet(company_id):

    data = load_company(company_id)

    company = data["company"]
    ratios = data["ratios"]
    profit = data["profit"]
    balance = data["balance"]
    cash = data["cash"]
    capital = data["capital"]
    pros = data["pros"]
    cons = data["cons"]

    pdf_path = SAMPLE_DIR / f"{company_id}_tearsheet.pdf"

    pdf = canvas.Canvas(
        str(pdf_path),
        pagesize=A4
    )

    # ======================================================
    # PAGE 1 HEADER
    # ======================================================

    sector = capital.iloc[0]["sector"]

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

    pdf.setFont("Helvetica-Bold",22)

    pdf.drawString(
        LEFT,
        PAGE_HEIGHT-35,
        company["company_name"]
    )

    pdf.setFont("Helvetica",12)

    pdf.drawString(
        LEFT,
        PAGE_HEIGHT-55,
        f"Ticker : {company_id}"
    )

    pdf.drawRightString(
        RIGHT,
        PAGE_HEIGHT-55,
        f"Sector : {sector}"
    )

    pdf.setFillColor(colors.black)

    # ======================================================
    # KPI CARDS
    # ======================================================

    latest = ratios.iloc[-1]

    cards = [

        ("ROE",
         f"{company['roe_percentage']:.2f}%"),

        ("ROCE",
         f"{company['roce_percentage']:.2f}%"),

        ("Revenue CAGR",
         f"{latest['revenue_cagr_5yr']:.2f}%"),

        ("PAT CAGR",
         f"{latest['pat_cagr_5yr']:.2f}%"),

        ("Debt / Equity",
         f"{latest['debt_to_equity']:.2f}"),

        ("Quality",
         f"{latest['composite_quality_score']:.2f}")

    ]

    start_y = PAGE_HEIGHT-150

    for i,(title,value) in enumerate(cards):

        row=i//3
        col=i%3

        x=LEFT+col*(CARD_WIDTH+CARD_GAP_X)

        y=start_y-row*(CARD_HEIGHT+CARD_GAP_Y)

        pdf.roundRect(
            x,
            y,
            CARD_WIDTH,
            CARD_HEIGHT,
            6
        )

        pdf.setFont("Helvetica-Bold",10)

        pdf.drawString(
            x+10,
            y+40,
            title
        )

        pdf.setFont("Helvetica-Bold",16)

        pdf.drawString(
            x+10,
            y+18,
            str(value)
        )

    # ======================================================
    # CHARTS
    # ======================================================

    revenue_chart = create_revenue_chart(
        profit,
        company_id
    )

    profit_chart = create_profit_chart(
        profit,
        company_id
    )

    roe_chart = create_roe_roce_chart(
        ratios,
        company,
        company_id
    )

    pdf.setFont(
        "Helvetica-Bold",
        15
    )

    pdf.drawString(
        LEFT,
        430,
        "Revenue Trend"
    )

    pdf.drawImage(
        str(revenue_chart),
        LEFT,
        250,
        width=240,
        height=150
    )

    pdf.drawString(
        310,
        430,
        "Net Profit Trend"
    )

    pdf.drawImage(
        str(profit_chart),
        300,
        250,
        width=240,
        height=150
    )

    pdf.drawString(
        LEFT,
        220,
        "ROE vs ROCE"
    )

    pdf.drawImage(
        str(roe_chart),
        LEFT,
        10,
        width=500,
        height=180
    )

    pdf.setFont(
        "Helvetica",
        9
    )

    pdf.drawString(
        LEFT,
        20,
        "Page 1"
    )

    pdf.drawRightString(
        RIGHT,
        20,
        "Generated by N100 Financial Intelligence"
    )

    # ======================================================
    # START PAGE 2
    # ======================================================

    pdf.showPage()

        # ======================================================
    # PAGE 2 HEADER
    # ======================================================

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
        "Financial Summary"
    )

    pdf.setFillColor(colors.black)

    # ======================================================
    # BALANCE SHEET CHART
    # ======================================================

    balance_chart = create_balance_chart(
        balance,
        company_id
    )

    pdf.setFont(
        "Helvetica-Bold",
        15
    )

    pdf.drawString(
        LEFT,
        735,
        "Balance Sheet Composition"
    )

    pdf.drawImage(
        str(balance_chart),
        LEFT,
        520,
        width=250,
        height=180
    )

    # ======================================================
    # CASH FLOW CHART
    # ======================================================

    cash_chart = create_cashflow_chart(
        cash,
        company_id
    )

    pdf.drawString(
        310,
        735,
        "Cash Flow"
    )

    pdf.drawImage(
        str(cash_chart),
        300,
        520,
        width=250,
        height=180
    )

    # ======================================================
    # PROS
    # ======================================================

    pdf.setFillColor(colors.green)

    pdf.setFont(
        "Helvetica-Bold",
        15
    )

    pdf.drawString(
        LEFT,
        480,
        "Pros"
    )

    pdf.setFont(
        "Helvetica",
        10
    )

    y = 460

    for _, row in pros.iterrows():

        lines = wrap_text(
            row["text"],
            width=40
        )

        for line in lines:

            pdf.drawString(
                LEFT,
                y,
                "• " + line
            )

            y -= 14

        y -= 8

    # ======================================================
    # CONS
    # ======================================================

    pdf.setFillColor(colors.red)

    pdf.setFont(
        "Helvetica-Bold",
        15
    )

    pdf.drawString(
        300,
        480,
        "Cons"
    )

    pdf.setFont(
        "Helvetica",
        10
    )

    y = 460

    for _, row in cons.iterrows():

        lines = wrap_text(
            row["text"],
            width=40
        )

        for line in lines:

            pdf.drawString(
                300,
                y,
                "• " + line
            )

            y -= 14

        y -= 8

    pdf.setFillColor(colors.black)

    # ======================================================
    # CAPITAL ALLOCATION
    # ======================================================

    badge = capital.iloc[0]["capital_allocation_label"]

    pdf.setFillColor(
        colors.HexColor("#1E3A8A")
    )

    pdf.roundRect(
    LEFT,
    240,
    260,
    45,
    8,
    fill=True
    )

    pdf.setFillColor(colors.white)

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawCentredString(
        LEFT + 130,
        256,
        badge
    )

    pdf.setFillColor(colors.black)

    pdf.setFont(
    "Helvetica-Bold",
    15
)

    pdf.drawString(
    LEFT,
    190,
    "About Company"
)

    pdf.setFont(
    "Helvetica",
    10
    )

    # ======================================================
# ABOUT COMPANY
# ======================================================

    pdf.setFont(
    "Helvetica-Bold",
    15
    )

    pdf.setFillColor(colors.black)

    pdf.drawString(
    LEFT,
    190,
    "About Company"
    )

    pdf.setFont(
    "Helvetica",
    10
    )

    about = str(company["about_company"])

    wrapped = textwrap.fill(
    about,
    width=85
    )

    text = pdf.beginText()

    text.setTextOrigin(
    LEFT,
    170
    )

    text.setLeading(14)

    text.textLines(wrapped)

    pdf.drawText(text)

    pdf.setFont(
            "Helvetica",
            9
        )
    
    pdf.drawString(
            LEFT,
            20,
            "Page 2"
        )
    
    pdf.drawRightString(
            RIGHT,
            20,
            "Generated by N100 Financial Intelligence"
        )

    # ======================================================
    # SAVE PDF
    # ======================================================

    pdf.save()

    print()

    print("=" * 60)
    print("PDF CREATED SUCCESSFULLY")
    print("=" * 60)
    print(pdf_path)

# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    test_companies = [
    "TCS",
    "HDFCBANK",
    "RELIANCE",
    "SUNPHARMA",
    "TATASTEEL"
]

for company_id in test_companies:
    print(f"\nGenerating {company_id}...")
    generate_tearsheet(company_id)