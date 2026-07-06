# Sprint 2 Retrospective

## What was completed

- Implemented profitability ratios
- Implemented leverage ratios
- Implemented CAGR engine
- Implemented cash flow KPIs
- Built financial ratio engine
- Populated financial_ratios table
- Generated capital_allocation.csv
- Logged ratio edge cases

## Challenges

- CAGR edge cases
- Negative equity handling
- Source data inconsistencies
- ROE/ROCE comparison anomalies
- Financial sector leverage handling

## Key Decisions

- Returned None for invalid denominators
- Used CAGR flags for special cases
- Logged ROE/ROCE discrepancies
- Kept calculation logic separate from database updates

## Lessons Learned

- Validate calculations with unit tests
- Separate business logic from database logic
- Log anomalies instead of changing formulas
- Verify financial ratios against source data