import streamlit as st
import utils.db as db
import plotly.express as px


st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
)

st.title("🏠 Home")

st.write("### Nifty 100 Financial Analytics Dashboard")

companies = db.get_companies()
summary = db.get_home_summary()
sector_data = db.get_sector_distribution()
top_companies = db.get_top_companies()

st.sidebar.header("Dashboard Controls")

st.subheader("Dashboard Summary")

summary_row = summary.iloc[0]

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Average ROE", f"{summary_row['avg_roe']:.2f}%")

with col2:
    st.metric("Avg Debt/Equity", f"{summary_row['avg_debt_to_equity']:.2f}")

with col3:
    st.metric("Companies", int(summary_row["total_companies"]))

with col4:
    st.metric("Debt-Free", int(summary_row["debt_free_companies"]))

with col5:
    st.metric("Revenue CAGR", f"{summary_row['avg_revenue_cagr']:.2f}%")


    st.subheader("Sector Distribution")

fig = px.pie(
    sector_data,
    names="broad_sector",
    values="company_count",
    hole=0.45,
    title="Companies by Sector"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🏆 Top 5 Companies (Based on ROE)")

top_companies.index = top_companies.index + 1

st.dataframe(
    top_companies,
    use_container_width=True
)

selected_company = st.sidebar.selectbox(
    "Select Company",
    companies["company_name"]
)
company = db.get_company_profile(selected_company)
kpis = db.get_company_kpis(selected_company)
history = db.get_profit_history(selected_company)
roe_history = db.get_roe_history(selected_company)

company = db.get_company_profile(selected_company)
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