# N100 Financial Intelligence Platform

## Project Overview

The N100 Financial Intelligence Platform is an end-to-end financial analytics application built to analyse companies within the Nifty 100 index using historical financial statements, market data and derived performance indicators.

The project combines an ETL pipeline, KPI calculation engine, interactive Streamlit dashboard and FastAPI backend to provide a complete financial intelligence platform for company analysis, screening and benchmarking.



# Key Features

- Automated ETL pipeline for importing Excel datasets into SQLite
- Data validation using custom Data Quality (DQ) rules
- Financial KPI calculation engine
- Company profile dashboard
- Financial stock screener
- Peer comparison analysis
- Sector analytics
- Capital allocation analysis
- Valuation engine
- FastAPI REST API
- Interactive Streamlit dashboard
- PDF tearsheet generation
- Excel and CSV export
- Comprehensive unit and API testing



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



# Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into the project directory

```bash
cd N100_Financial_Intelligence
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

Windows

```bash
venv\Scripts\activate
```

Install project dependencies

```bash
pip install -r requirements.txt
```



# ETL Pipeline

Load the source datasets into the SQLite database.

```bash
python src/etl/loader.py
```

Validate the datasets

```bash
python src/validation/validator.py
```

Generate financial KPIs

```bash
python src/kpi/ratios.py
```


# Running the Dashboard

Launch the Streamlit dashboard

```bash
streamlit run src/dashboard/app.py
```


# Running the API

Start the FastAPI server

```bash
uvicorn src.api.main:app --reload --port 8000
```

Swagger documentation

```
http://127.0.0.1:8000/docs
```


# Running Tests

Run the complete test suite

```bash
pytest
```

Generate the HTML test report

```bash
pytest tests --html=reports/pytest_report.html
```



# Dashboard Modules

### Home

Displays key financial metrics and an overview of the platform.

### Company Profile

Shows detailed company information, historical performance and financial ratios.

### Stock Screener

Filters companies using financial metrics such as ROE, Debt-to-Equity, Free Cash Flow and CAGR.

### Peer Comparison

Compares companies against industry peers using percentile rankings and radar metrics.

### Sector Analytics

Provides sector-level comparisons and performance insights.

### Capital Allocation

Analyses cash flow quality, capital allocation strategy and Free Cash Flow metrics.

### Reports

Provides downloadable reports, valuation summaries and analytical outputs.


# API Modules

The FastAPI backend exposes REST endpoints including:

- Health
- Companies
- Screener
- Sectors
- Peer Comparison
- Market Capitalisation
- Portfolio Statistics
- Documents

Interactive API documentation is available through Swagger UI.


# Project Structure

N100_Financial_Intelligence/

├── data/
├── docs/
├── output/
├── reports/
├── sql/
├── src/
│   ├── analytics/
│   ├── api/
│   ├── dashboard/
│   ├── etl/
│   ├── kpi/
│   ├── nlp/
│   └── validation/
├── tests/
└── README.md


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


# Future Improvements

- PostgreSQL support
- Docker deployment
- User authentication
- CI/CD pipeline
- Cloud deployment
- Live market data integration
- Portfolio management
- Role-based access control

