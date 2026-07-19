# Sprint 4 Retrospective

## Sprint Goal

Build a complete Streamlit-based Financial Intelligence Dashboard for Nifty 100 companies with valuation analysis and downloadable reports.

---

## Completed Work

- Built all 8 Streamlit dashboard screens.
- Integrated the SQLite database.
- Developed the valuation engine.
- Implemented financial screening.
- Added peer comparison.
- Built trend and sector analysis pages.
- Created capital allocation analysis.
- Implemented reports dashboard with downloadable outputs.
- Generated valuation_summary.xlsx and valuation_flags.csv.

---

## Challenges Faced

- Migrating from Excel-based inputs to SQLite.
- Handling missing peer group mappings.
- Managing DataFrame merges with duplicate column names.
- Resolving file path issues for the Reports page.
- Handling missing values in financial calculations.

---

## Solutions Implemented

- Replaced Excel loading with SQLite queries.
- Cleaned DataFrame merges using explicit join keys.
- Added error handling for missing files.
- Implemented valuation classification logic.
- Added report export functionality.

---

## Lessons Learned

- Proper project structure simplifies maintenance.
- SQLite improves scalability compared to Excel files.
- Streamlit caching improves dashboard performance.
- Data validation reduces downstream errors.
- Modular code is easier to debug and extend.

---

## Future Improvements

- Live stock market API integration.
- Portfolio tracking.
- User authentication.
- PDF report generation.
- Dark mode.
- Advanced valuation models.

---

## Sprint Outcome

Sprint 4 was successfully completed with a fully functional Financial Intelligence Dashboard capable of analysing Nifty 100 companies, generating valuation reports, and presenting insights through an interactive Streamlit interface.