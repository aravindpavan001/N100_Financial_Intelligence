-- 1. Total Companies
SELECT COUNT(*) AS total_companies
FROM companies;

-- 2. Companies by Broad Sector
SELECT broad_sector, COUNT(*) AS total
FROM sectors
GROUP BY broad_sector
ORDER BY total DESC;

-- 3. Top 10 Companies by Market Cap
SELECT company_id, market_cap_crore
FROM market_cap
ORDER BY market_cap_crore DESC
LIMIT 10;

-- 4. Average Return on Equity
SELECT AVG(return_on_equity_pct) AS average_roe
FROM financial_ratios;

-- 5. Highest Sales by Company
SELECT company_id,
       MAX(sales) AS highest_sales
FROM profitandloss
GROUP BY company_id
ORDER BY highest_sales DESC
LIMIT 10;

-- 6. Companies with Negative Profit
SELECT company_id,
       year,
       net_profit
FROM profitandloss
WHERE net_profit < 0;

-- 7. Latest Balance Sheet Records
SELECT *
FROM balancesheet
WHERE year = (
    SELECT MAX(year)
    FROM balancesheet
);

-- 8. Total Stock Price Records
SELECT COUNT(*) AS total_stock_records
FROM stock_prices;

-- 9. Average PE Ratio
SELECT AVG(pe_ratio) AS average_pe
FROM market_cap;

-- 10. Companies with More Than 10 Years of Data
SELECT company_id,
       COUNT(*) AS years_available
FROM profitandloss
GROUP BY company_id
HAVING COUNT(*) > 10;