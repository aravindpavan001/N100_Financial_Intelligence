import streamlit as st
import utils.db as db
import os
def get_recommendation(row):

    quality = row["composite_quality_score"]
    pe = row["pe_ratio"]
    debt = row["debt_to_equity"]

    score = quality

    if pe <= 20:
        score += 10
    elif pe > 40:
        score -= 10

    if debt <= 0.5:
        score += 10
    elif debt > 1:
        score -= 10

    score = max(0, min(100, score))

    if score >= 80:
        recommendation = "🟢 BUY"
        reason = "Strong quality, attractive valuation and healthy balance sheet."

    elif score >= 60:
        recommendation = "🟡 HOLD"
        reason = "Average valuation with acceptable financial quality."

    else:
        recommendation = "🔴 AVOID"
        reason = "Weak financial profile or expensive valuation."

    return recommendation, reason, score
print("=" * 60)
print("DB MODULE:", db.__file__)
print("=" * 60)
import plotly.express as px
import pandas as pd
from pathlib import Path

print("=== RUNNING THIS APP.PY ===")

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]

screener_path = BASE_DIR / "output" / "screener_dataset.csv"

screener_df = pd.read_csv(screener_path) 
print("=" * 60)
print("CSV PATH:", screener_path)
print("CSV EXISTS:", os.path.exists(screener_path))
print("CSV SHAPE:", screener_df.shape)
print("CSV COLUMNS:")
print(screener_df.columns.tolist())
print("=" * 60)
companies = db.get_companies()
summary = db.get_home_summary()
sector_data = db.get_sector_distribution()
top_companies = db.get_top_companies()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.header("Dashboard Controls")


st.sidebar.subheader("📊 Stock Screener")

min_roe = st.sidebar.slider(
    "Minimum ROE (%)",
    0,
    40,
    15,
)

max_debt = st.sidebar.slider(
    "Maximum Debt to Equity",
    0.0,
    5.0,
    1.0,
)

min_revenue_cagr = st.sidebar.slider(
    "Minimum Revenue CAGR (%)",
    0,
    30,
    10,
)

min_pat_cagr = st.sidebar.slider(
    "Minimum PAT CAGR (%)",
    0,
    30,
    10,
)

min_fcf = st.sidebar.slider(
    "Minimum Free Cash Flow",
    0,
    5000,
    0,
)

max_pe = st.sidebar.slider(
    "Maximum P/E",
    0,
    150,
    150,
)

max_pb = st.sidebar.slider(
    "Maximum P/B",
    0,
    20,
    20,
)

min_dividend = st.sidebar.slider(
    "Minimum Dividend Yield (%)",
    0.0,
    10.0,
    0.0,
)

min_interest = st.sidebar.slider(
    "Minimum Interest Coverage",
    0,
    100,
    0,
)



filtered = screener_df[
    (screener_df["roe_percentage"] >= min_roe)
    & (screener_df["debt_to_equity"] <= max_debt)
    & (screener_df["revenue_cagr_5yr"] >= min_revenue_cagr)
    & (screener_df["pat_cagr_5yr"] >= min_pat_cagr)
    & (screener_df["free_cash_flow_cr"] >= min_fcf)
    & (screener_df["pe_ratio"] <= max_pe)
    & (screener_df["pb_ratio"] <= max_pb)
    & (screener_df["dividend_yield_pct"] >= min_dividend)
    & (
        screener_df["interest_coverage"]
        .fillna(0)
        >= min_interest
    )
]
st.sidebar.markdown("---")



selected_company = st.sidebar.selectbox(
    "Select Company",
    companies["company_name"],
)

# --------------------------------------------------
# HOME
# --------------------------------------------------
st.title("🏠 Home")
st.write("### Nifty 100 Financial Analytics Dashboard")

# --------------------------------------------------
# DASHBOARD SUMMARY
# --------------------------------------------------
st.subheader("Dashboard Summary")

summary_row = summary.iloc[0]

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Average ROE", f"{summary_row['avg_roe']:.2f}%")

with col2:
    st.metric(
        "Avg Debt/Equity",
        f"{summary_row['avg_debt_to_equity']:.2f}",
    )

with col3:
    st.metric(
        "Companies",
        int(summary_row["total_companies"]),
    )

with col4:
    st.metric(
        "Debt-Free",
        int(summary_row["debt_free_companies"]),
    )

with col5:
    st.metric(
        "Revenue CAGR",
        f"{summary_row['avg_revenue_cagr']:.2f}%",
    )

# --------------------------------------------------
# SECTOR CHART
# --------------------------------------------------
st.subheader("Sector Distribution")

fig = px.pie(
    sector_data,
    names="broad_sector",
    values="company_count",
    hole=0.45,
    title="Companies by Sector",
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# TOP COMPANIES
# --------------------------------------------------
st.subheader("🏆 Top 5 Companies")

top_companies.index = top_companies.index + 1

st.dataframe(
    top_companies,
    use_container_width=True,
)

# --------------------------------------------------
# SCREENER
# --------------------------------------------------
st.header("📊 Stock Screener")

st.sidebar.markdown("### Presets")

st.sidebar.markdown("### Presets")

preset = st.sidebar.selectbox(
    "Preset",
    [
        "Custom",
        "Quality",
        "Growth",
        "Value",
        "Dividend",
        "Debt Free",
        "Turnaround",
    ]
)

if preset == "Quality":
    filtered = screener_df[
        (screener_df["roe_percentage"] >= 20)
        & (screener_df["debt_to_equity"] <= 0.5)
    ]

elif preset == "Value":
    filtered = screener_df[
        (screener_df["pe_ratio"] <= 20)
        & (screener_df["pb_ratio"] <= 3)
    ]

elif preset == "Growth":
    filtered = screener_df[
        (screener_df["revenue_cagr_5yr"] >= 15)
        & (screener_df["pat_cagr_5yr"] >= 15)
    ]

elif preset == "Dividend":
    filtered = screener_df[
        screener_df["dividend_yield_pct"] >= 2
    ]

elif preset == "Debt Free":
    filtered = screener_df[
        screener_df["debt_to_equity"] <= 0.2
    ]

elif preset == "Turnaround":
    filtered = screener_df[
        screener_df["pat_cagr_5yr"] > 0
    ]

st.write(f"### {len(filtered)} companies match your filters")

display_df = filtered[
    [
    "id_company",
    "company_name",
    "roe_percentage",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "free_cash_flow_cr",
    "interest_coverage",
    "pe_ratio",
    "pb_ratio",
    "dividend_yield_pct",

    ]
]

st.dataframe(
    display_df,
    use_container_width=True,
)

csv = display_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Companies",
    data=csv,
    file_name="filtered_companies.csv",
    mime="text/csv",
)

# --------------------------------------------------
# COMPANY DATA
# --------------------------------------------------
company = db.get_company_profile(selected_company)
kpis = db.get_company_kpis(selected_company)
print(kpis.columns)
print(kpis)
valuation = db.get_company_valuation(selected_company)
history = db.get_profit_history(selected_company)
roe_history = db.get_roe_history(selected_company)


st.subheader("Company Profile")

if not company.empty:

    row = company.iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Company", row["company_name"])
        st.metric("Ticker", row["id"])

    with col2:
     st.image(row["company_logo"], width=120)

    st.write("### About Company")
    st.write(row["about_company"])
    
else:
    st.error("Company not found.")


st.subheader("Financial KPIs")


if not kpis.empty:

    row = kpis.iloc[0]
    recommendation, reason, score = get_recommendation(row)   
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("ROE (%)", f"{row['roe_percentage']:.2f}")
        st.metric("Net Profit Margin (%)", f"{row['net_profit_margin_pct']:.2f}")

    with col2:
        st.metric("ROCE (%)", f"{row['roce_percentage']:.2f}")
        st.metric("Debt to Equity", f"{row['debt_to_equity']:.2f}")

    with col3:
        st.metric("Revenue CAGR (5Y)", f"{row['revenue_cagr_5yr']:.2f}%")
        st.metric("Free Cash Flow", f"{row['free_cash_flow_cr']:.2f}")    
        st.metric("Quality Score",f"{row['composite_quality_score']:.1f}")
        st.subheader("Investment Recommendation")
        st.metric("Recommendation", recommendation)
        st.metric("Valuation Score", f"{score:.0f}/100")
        st.info(reason)

st.subheader("Valuation")
if not valuation.empty:

    row = valuation.iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("P/E", f"{row['pe_ratio']:.2f}")

    with c2:
        st.metric("P/B", f"{row['pb_ratio']:.2f}")

    with c3:
        st.metric("EV/EBITDA", f"{row['ev_ebitda']:.2f}")

    with c4:
        st.metric(
            "Dividend Yield",
            f"{row['dividend_yield_pct']:.2f}%"
        )

        pe = row["pe_ratio"]

        if pe <= 15:
         st.success("🟢 Undervalued")

        elif pe <= 25:
          st.warning("🟡 Fairly Valued")

        else:
         st.error("🔴 Overvalued")
         st.subheader("Revenue vs Net Profit")

if not history.empty:

    fig = px.bar(
        history,
        x="year",
        y=["sales", "net_profit"],
        barmode="group",
        title="Revenue vs Net Profit"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No financial history available.")


st.subheader("ROE Trend")

if not roe_history.empty:

    fig = px.line(
        roe_history,
        x="year",
        y="return_on_equity_pct",
        markers=True,
        title="Return on Equity Over Time"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No ROE history available.")


st.subheader("Pros & Cons")

if not kpis.empty:

    row = kpis.iloc[0]

    pros = []
    cons = []

    # ROE
    if row["roe_percentage"] >= 15:
        pros.append("High Return on Equity")
    else:
        cons.append("Low Return on Equity")

    # Debt
    if row["debt_to_equity"] <= 0.5:
        pros.append("Low Debt")
    else:
        cons.append("High Debt")

    # Revenue Growth
    if row["revenue_cagr_5yr"] >= 10:
        pros.append("Strong Revenue Growth")
    else:
        cons.append("Weak Revenue Growth")

    # Free Cash Flow
    if row["free_cash_flow_cr"] > 0:
        pros.append("Positive Free Cash Flow")
    else:
        cons.append("Negative Free Cash Flow")
    col1, col2 = st.columns(2)

    with col1:
        st.success("### Pros")
        for item in pros:
            st.write(f"✅ {item}")

    with col2:
        st.error("### Cons")
        for item in cons:
            st.write(f"❌ {item}")    