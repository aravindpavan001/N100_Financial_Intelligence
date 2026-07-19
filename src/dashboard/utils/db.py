import sqlite3
import pandas as pd
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

DB_PATH = BASE_DIR / "nifty100.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)

    print("=" * 60)
    print("DATABASE:", DB_PATH)
    print(
        conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        ).fetchall()
    )
    print("=" * 60)

    return conn

@st.cache_data(ttl=600)
def get_companies():
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT company_name
        FROM companies
        ORDER BY company_name
        """,
        conn,
    )

    conn.close()
    return df


@st.cache_data(ttl=600)
def get_company_profile(company_name):
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM companies
        WHERE company_name = ?
        """,
        conn,
        params=(company_name,),
    )

    conn.close()
    return df

@st.cache_data(ttl=600)
def get_company_kpis(company_name):
    conn = get_connection()

    query = """
    SELECT
        c.roce_percentage,
        c.roe_percentage,

        fr.net_profit_margin_pct,
        fr.debt_to_equity,
        fr.revenue_cagr_5yr,
        fr.pat_cagr_5yr,
        fr.free_cash_flow_cr,
        fr.composite_quality_score,

        mc.pe_ratio,
        mc.pb_ratio,
        mc.ev_ebitda,
        mc.dividend_yield_pct
    FROM companies c

    JOIN financial_ratios fr
    ON c.id = fr.company_id

    LEFT JOIN market_cap mc
    ON c.id = mc.company_id
    WHERE c.company_name = ?
    ORDER BY
    fr.year DESC,
    mc.year DESC
    LIMIT 1
    """

    df = pd.read_sql(query, conn, params=(company_name,))

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_profit_history(company_name):
    conn = get_connection()

    query = """
    SELECT
        p.year,
        p.sales,
        p.net_profit
    FROM profitandloss p
    JOIN companies c
        ON p.company_id = c.id
    WHERE c.company_name = ?
    ORDER BY p.year
    """

    df = pd.read_sql(query, conn, params=(company_name,))

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_roe_history(company_name):
    conn = get_connection()

    query = """
    SELECT
        fr.year,
        fr.return_on_equity_pct
    FROM financial_ratios fr
    JOIN companies c
        ON fr.company_id = c.id
    WHERE c.company_name = ?
    ORDER BY fr.year
    """

    df = pd.read_sql(query, conn, params=(company_name,))

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_home_summary():
    conn = get_connection()

    query = """
    SELECT
    ROUND(AVG(return_on_equity_pct),2) AS avg_roe,
    ROUND(AVG(debt_to_equity),2) AS avg_debt_to_equity,
    COUNT(DISTINCT company_id) AS total_companies,
    SUM(CASE WHEN debt_to_equity=0 THEN 1 ELSE 0 END) AS debt_free_companies,
    0 AS avg_revenue_cagr
FROM financial_ratios;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df    

@st.cache_data(ttl=600)
def get_sector_distribution():
    conn = get_connection()

    print("\nTABLES VISIBLE TO get_sector_distribution:")
    print(conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall())

    query = """
    SELECT
        broad_sector,
        COUNT(*) AS company_count
    FROM sectors
    GROUP BY broad_sector
    ORDER BY company_count DESC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_top_companies():
    conn = get_connection()

    query = """
    SELECT
        c.company_name,
        c.roe_percentage
    FROM companies c
    WHERE c.roe_percentage IS NOT NULL
    ORDER BY c.roe_percentage DESC
    LIMIT 5
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_screener_data():

    conn = get_connection()

    companies = pd.read_sql("SELECT * FROM companies", conn)
    ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
    market = pd.read_sql("SELECT * FROM market_cap", conn)

    conn.close()

    # Keep latest financial ratios per company
    ratios = (
        ratios.sort_values("year")
              .groupby("company_id")
              .tail(1)
    )

    # Keep latest market cap row per company
    market = (
        market.sort_values("year")
              .groupby("company_id")
              .tail(1)
    )

    df = companies.merge(
        ratios,
        left_on="id",
        right_on="company_id",
        how="left"
    )

    df = df.merge(
        market,
        left_on="id",
        right_on="company_id",
        how="left",
        suffixes=("", "_market")
    )

    return df

@st.cache_data(ttl=600)
def get_company_valuation(company_name):

    conn = get_connection()

    query = """
    SELECT
        c.company_name,
        mc.pe_ratio,
        mc.pb_ratio,
        mc.ev_ebitda,
        mc.dividend_yield_pct,
        mc.market_cap_crore
    FROM companies c
    JOIN market_cap mc
        ON c.id = mc.company_id
    WHERE c.company_name = ?
    ORDER BY mc.year DESC
    LIMIT 1
    """

    df = pd.read_sql(
        query,
        conn,
        params=(company_name,)
    )

    conn.close()

    return df