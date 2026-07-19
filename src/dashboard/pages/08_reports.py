import streamlit as st
from pathlib import Path
import pandas as pd

st.title("📄 Reports")

st.markdown(
    "Download all generated reports from the Financial Intelligence Engine."
)


BASE_DIR = Path(__file__).resolve().parents[3]

OUTPUT_DIR = BASE_DIR / "output"

st.subheader("Available Reports")

files = list(OUTPUT_DIR.glob("*"))

if files:
    for file in files:
        st.write(file.name)
else:
    st.warning("No reports found.")


st.subheader("Download Reports")

files = list(OUTPUT_DIR.glob("*"))

if not files:
    st.warning("No reports available.")
else:
    for file in files:
        with open(file, "rb") as f:
            st.download_button(
                label=f"Download {file.name}",
                data=f,
                file_name=file.name,
            )


st.subheader("Project Statistics")

try:
    companies = pd.read_excel(
        OUTPUT_DIR / "valuation_summary.xlsx"
    )

except FileNotFoundError:
    st.error("valuation_summary.xlsx not found.")
    st.stop()

col1, col2, col3 = st.columns(3)

col1.metric("Companies", len(companies))

col2.metric(
    "Premium",
    (companies["valuation_flag"] == "Premium").sum()
)

col3.metric(
    "Discount",
    (companies["valuation_flag"] == "Discount").sum()
)

st.subheader("Valuation Distribution")

counts = companies["valuation_flag"].value_counts()

st.bar_chart(counts)

st.subheader("Valuation Summary Preview")

st.dataframe(companies.head(20))

