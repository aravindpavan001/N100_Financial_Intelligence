# N100 Financial Intelligence Platform

## Project Overview

The N100 Financial Intelligence Platform is an end-to-end financial analytics application built to analyse companies within the Nifty 100 index using historical financial statements, market data and derived performance indicators.

The project combines an ETL pipeline, KPI calculation engine, interactive Streamlit dashboard and FastAPI backend to provide a complete financial intelligence platform for company analysis, screening and benchmarking.

---

#  Live Demo

**Live Dashboard:**  
[Open Streamlit Dashboard](https://n100financialintelligence-5yznrrsl3x4wefhje8us3o.streamlit.app/)

**API Documentation:**  
[Open FastAPI Swagger Documentation](https://n100-financial-intelligence-api.onrender.com/docs)


> The Streamlit dashboard link will be updated once the current deployment URL is restored.

---

#  Project Highlights

- **92 Nifty 100 companies** analysed
- **50+ financial KPIs**
- Automated ETL pipeline for importing financial datasets
- Data validation using custom Data Quality (DQ) rules
- SQLite-based financial data storage
- Financial KPI calculation engine
- Interactive Streamlit dashboard
- FastAPI REST API with Swagger documentation
- **101 automated tests passing**
- API performance testing with concurrent requests
- PDF tearsheet generation
- Excel and CSV export
- Company screening and peer benchmarking
- Sector-level financial analysis

---

#  Key Analytical Insights

The platform enables analysis of financial performance across the Nifty 100 using profitability, growth, leverage, valuation and cash-flow metrics.

Examples of analytical questions supported by the platform:

- Which companies demonstrate strong profitability and return on equity?
- Which companies combine strong growth with healthy cash generation?
- Which companies have relatively high leverage or weaker interest coverage?
- How do companies compare with their sector peers?
- Which sectors demonstrate stronger financial performance?
- How effectively are companies converting operating cash flow into Free Cash Flow?

The platform is designed to help analysts move from raw financial data to structured comparisons and financial insights.

---

#  Key Features

## Data Eng

- Automated ETL pipeline for importing Excel datasets into SQLite
- Data validation using custom Data Quality (DQ) rules
- Load auditing and validation reporting
- Structured financial data storage

## Financial Analytics

- Financial KPI calculation engine
- Company financial analysis
- Profitability analysis
- Growth analysis
- Leverage and capital structure analysis
- Cash flow analysis
- Free Cash Flow analysis
- Valuation analysis
- Sector analytics
- Peer benchmarking
- Capital allocation analysis

## Interactive Dashboard

The Streamlit dashboard provides an interactive interface for exploring financial performance across the Nifty 100.

Dashboard modules include:

- Home
- Company Profile
- Stock Screener
- Peer Comparison
- Sector Analytics
- Capital Allocation
- Reports

## API

The FastAPI backend provides REST endpoints for accessing and analysing financial data.

The API includes:

- Health
- Companies
- Screener
- Sectors
- Peer Comparison
- Market Capitalisation
- Portfolio Statistics
- Documents

Interactive API documentation is available through Swagger UI.

---


# Technology Stack

- Python
- Pandas
- NumPy
- SQLite
- FastAPI
- Streamlit
- Plotly
- OpenPyXL
- ReportLab
- Pytest
- Git
- VS Code


# Generated Outputs

Examples of generated project outputs include:

- valuation_summary.xlsx
- cashflow_intelligence.xlsx
- portfolio_stats.csv
- validation_failures.csv
- load_audit.csv
- peer_report.xlsx
- pytest_report.html
- performance_results.csv



