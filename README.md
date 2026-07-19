# N100 Financial Intelligence Dashboard

## Project Overview

The N100 Financial Intelligence Dashboard is a Python-based financial analytics application built to analyse Nifty 100 companies using historical financial data.

The dashboard enables users to:

- View detailed company profiles
- Screen companies using financial filters
- Compare companies within peer groups
- Analyse financial trends
- Explore sector-level insights
- Review capital allocation metrics
- Generate valuation analysis
- Download reports and analytics

---

## Features

- Home Dashboard
- Company Profile
- Financial Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation Analysis
- Reports Dashboard
- Valuation Engine
- Excel & CSV Export

---

## Technology Stack

- Python
- Pandas
- NumPy
- SQLite
- Streamlit
- Plotly
- OpenPyXL
- Git
- VS Code


## Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into the project folder

```bash
cd N100_Financial_Intelligence
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Dashboard

```bash
streamlit run src/dashboard/app.py
```

---

## Run the Valuation Engine

```bash
python src/analytics/valuation.py
```

---

## Generated Outputs

Running the valuation engine generates:

- valuation_summary.xlsx
- valuation_flags.csv

These files are stored inside the `output/` directory.

---

## Dashboard Screens

### Home
Displays key financial KPIs and an overview of the dashboard.

### Company Profile
Displays company information, financial metrics, and business details.

### Stock Screener
Filters companies using financial ratios and exports screened results.

### Peer Comparison
Compares companies against their peer group using financial metrics.

### Trend Analysis
Visualises historical financial performance and trends.

### Sector Analysis
Provides sector-level comparisons and insights.

### Capital Allocation
Displays free cash flow and capital allocation metrics.

### Reports
Allows users to download generated reports, review valuation summaries, and view project statistics.

---

## Outputs

- valuation_summary.xlsx
- valuation_flags.csv

---

## Future Improvements

- Live stock market data integration
- Portfolio tracking
- User authentication
- PDF report generation
- Advanced valuation models
- Dark mode support

---

## Author

Aravind Pavan

Data Analyst | Python | SQL | Power BI | Streamlit