CREATE INDEX IF NOT EXISTS idx_financial_ratios_company_year
ON financial_ratios(company_id, year);

CREATE INDEX IF NOT EXISTS idx_profitandloss_company_year
ON profitandloss(company_id, year);

CREATE INDEX IF NOT EXISTS idx_balancesheet_company_year
ON balancesheet(company_id, year);

CREATE INDEX IF NOT EXISTS idx_cashflow_company_year
ON cashflow(company_id, year);

CREATE INDEX IF NOT EXISTS idx_market_cap_company_year
ON market_cap(company_id, year);

CREATE INDEX IF NOT EXISTS idx_stock_prices_company_date
ON stock_prices(company_id, date);