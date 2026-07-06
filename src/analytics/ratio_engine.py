import os
import sqlite3
import pandas as pd

from src.analytics.ratios import (
    calculate_net_profit_margin,
    calculate_operating_profit_margin,
    calculate_roe,
    calculate_roce,
    calculate_roa,
    calculate_debt_to_equity,
    calculate_interest_coverage,
    calculate_asset_turnover,
)

from src.analytics.cagr import (
    calculate_growth_metrics,
)

from src.analytics.cashflow_kpis import (
    calculate_free_cash_flow,
    calculate_capex_intensity,
    classify_capital_allocation,
    get_cashflow_sign,
)

DB_PATH = "nifty100.db"
OUTPUT_FOLDER = "output"
CSV_FILE = os.path.join(OUTPUT_FOLDER, "capital_allocation.csv")

def connect_db():
    return sqlite3.connect(DB_PATH)


def load_tables(conn):

    companies = pd.read_sql(
        "SELECT * FROM companies",
        conn,
    )

    profit = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn,
    )

    balance = pd.read_sql(
        "SELECT * FROM balancesheet",
        conn,
    )

    cashflow = pd.read_sql(
        "SELECT * FROM cashflow",
        conn,
    )

    ratios = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn,
    )

    return companies, profit, balance, cashflow, ratios

def merge_tables(companies, profit, balance, cashflow):

    df = profit.merge(
        balance,
        on=["company_id", "year"],
    )

    df = df.merge(
        cashflow,
        on=["company_id", "year"],
    )

    companies = companies.rename(columns={"id": "company_master_id"})

    df = df.merge(
    companies,
    left_on="company_id",
    right_on="company_master_id",
    how="left",
)

    df = df[df["year"] != "TTM"].copy()

    df["year_number"] = (
        df["year"]
        .str.extract(r"(\d{4})")
        .astype(int)
    )

    df.sort_values(
        ["company_id", "year_number"],
        inplace=True,
    )

    df.reset_index(
        drop=True,
        inplace=True,
    )

    return df

def create_output_folder():

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

def build_company_history(df):
    """
    Build historical data for each company.
    Used for CAGR calculations.
    """

    history = {}

    for company in df["company_id"].unique():

        company_df = (
            df[df["company_id"] == company]
            .sort_values("year_number")
            .copy()
        )

        history[company] = {
            "sales": company_df["sales"].tolist(),
            "profit": company_df["net_profit"].tolist(),
            "eps": company_df["eps"].tolist(),
        }

    return history


def calculate_company_cagr(history):

    cagr_results = {}

    for company, values in history.items():

        revenue_cagr, _ = calculate_growth_metrics(
            values["sales"],
            5,
        )

        pat_cagr, _ = calculate_growth_metrics(
            values["profit"],
            5,
        )

        eps_cagr, _ = calculate_growth_metrics(
            values["eps"],
            5,
        )

        cagr_results[company] = {
            "revenue": revenue_cagr,
            "pat": pat_cagr,
            "eps": eps_cagr,
        }

    return cagr_results        

def calculate_kpis(row, cagr_results):

    company = row.company_id

    net_profit_margin = calculate_net_profit_margin(
        row.net_profit,
        row.sales,
    )

    operating_profit_margin = calculate_operating_profit_margin(
        row.operating_profit,
        row.sales,
    )

    roe = calculate_roe(
        row.net_profit,
        row.equity_capital,
        row.reserves,
    )

    roce = calculate_roce(
        row.operating_profit,
        row.equity_capital,
        row.reserves,
        row.borrowings,
        "General",
    )

    roa = calculate_roa(
        row.net_profit,
        row.total_assets,
    )

    debt_to_equity = calculate_debt_to_equity(
        row.borrowings,
        row.equity_capital,
        row.reserves,
    )

    interest_coverage = calculate_interest_coverage(
        row.operating_profit,
        row.other_income,
        row.interest,
    )

    asset_turnover = calculate_asset_turnover(
        row.sales,
        row.total_assets,
    )

    free_cash_flow = calculate_free_cash_flow(
        row.operating_activity,
        row.investing_activity,
    )

    capex_value, _ = calculate_capex_intensity(
        row.investing_activity,
        row.sales,
    )

    return {
        "company_id": row.company_id,
        "year": row.year,
        "net_profit_margin_pct": net_profit_margin,
        "operating_profit_margin_pct": operating_profit_margin,
        "return_on_equity_pct": roe,
        "debt_to_equity": debt_to_equity,
        "interest_coverage": interest_coverage,
        "asset_turnover": asset_turnover,
        "free_cash_flow_cr": free_cash_flow,
        "capex_cr": capex_value,
        "earnings_per_share": row.eps,
        "book_value_per_share": row.book_value,
        "dividend_payout_ratio_pct": row.dividend_payout,
        "total_debt_cr": row.borrowings,
        "cash_from_operations_cr": row.operating_activity,
        "revenue_cagr_5yr": cagr_results[company]["revenue"],
        "pat_cagr_5yr": cagr_results[company]["pat"],
        "eps_cagr_5yr": cagr_results[company]["eps"],
        "composite_quality_score": None,
    }

def build_capital_allocation(row):

    return {
        "company_id": row.company_id,
        "year": row.year,
        "cfo_sign": get_cashflow_sign(
            row.operating_activity,
        ),
        "cfi_sign": get_cashflow_sign(
            row.investing_activity,
        ),
        "cff_sign": get_cashflow_sign(
            row.financing_activity,
        ),
        "pattern_label": classify_capital_allocation(
            row.operating_activity,
            row.investing_activity,
            row.financing_activity,
        ),
    }

def save_results(conn, ratio_rows):

    cursor = conn.cursor()

    for row in ratio_rows:

        cursor.execute(
            """
            UPDATE financial_ratios
            SET
                net_profit_margin_pct=?,
                operating_profit_margin_pct=?,
                return_on_equity_pct=?,
                debt_to_equity=?,
                interest_coverage=?,
                asset_turnover=?,
                free_cash_flow_cr=?,
                capex_cr=?,
                earnings_per_share=?,
                book_value_per_share=?,
                dividend_payout_ratio_pct=?,
                total_debt_cr=?,
                cash_from_operations_cr=?,
                revenue_cagr_5yr=?,
                pat_cagr_5yr=?,
                eps_cagr_5yr=?,
                composite_quality_score=?
            WHERE company_id=?
            AND year=?
            """,
            (
                row["net_profit_margin_pct"],
                row["operating_profit_margin_pct"],
                row["return_on_equity_pct"],
                row["debt_to_equity"],
                row["interest_coverage"],
                row["asset_turnover"],
                row["free_cash_flow_cr"],
                row["capex_cr"],
                row["earnings_per_share"],
                row["book_value_per_share"],
                row["dividend_payout_ratio_pct"],
                row["total_debt_cr"],
                row["cash_from_operations_cr"],
                row["revenue_cagr_5yr"],
                row["pat_cagr_5yr"],
                row["eps_cagr_5yr"],
                row["composite_quality_score"],
                row["company_id"],
                row["year"],
            ),
        )

    conn.commit()


def save_capital_csv(capital_rows):

    df = pd.DataFrame(capital_rows)

    df.to_csv(
        CSV_FILE,
        index=False,
    )

def main():

    print("=" * 70)
    print("DAY 12 RATIO ENGINE")
    print("=" * 70)

    conn = connect_db()

    (
        companies,
        profit,
        balance,
        cashflow,
        ratios,
    ) = load_tables(conn)

    merged_df = merge_tables(
        companies,
        profit,
        balance,
        cashflow,
    )

    create_output_folder()

    history = build_company_history(
        merged_df,
    )

    cagr_results = calculate_company_cagr(
        history,
    )

    ratio_rows = []

    capital_rows = []

    for row in merged_df.itertuples(index=False):

        ratio_rows.append(
            calculate_kpis(
                row,
                cagr_results,
            )
        )

        capital_rows.append(
            build_capital_allocation(
                row,
            )
        )

    save_results(
        conn,
        ratio_rows,
    )

    save_capital_csv(
        capital_rows,
    )

    conn.close()

    print()

    print("Rows Processed :", len(ratio_rows))

    print("CSV Generated  :", CSV_FILE)

    print("Database Updated")

if __name__ == "__main__":
    main()        