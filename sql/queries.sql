-- Bluestock Fintech MF Capstone
-- 10 Analytical SQL Queries - Day 2

-- Query 1: Top 5 funds by 3 year return
SELECT scheme_name, fund_house, return_3yr_pct
FROM fact_performance fp
JOIN dim_fund df ON fp.amfi_code = df.amfi_code
ORDER BY return_3yr_pct DESC
LIMIT 5;

-- Query 2: Average NAV per fund in 2025
SELECT d.scheme_name, ROUND(AVG(n.nav), 2) as avg_nav
FROM fact_nav n
JOIN dim_fund d ON n.amfi_code = d.amfi_code
WHERE n.date LIKE '2025%'
GROUP BY n.amfi_code
ORDER BY avg_nav DESC
LIMIT 10;

-- Query 3: Total transactions by type
SELECT transaction_type,
       COUNT(*) as total_count,
       SUM(amount_inr) as total_amount
FROM fact_transactions
GROUP BY transaction_type;

-- Query 4: Transactions by state
SELECT state,
       COUNT(*) as num_transactions,
       SUM(amount_inr) as total_invested
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY state
ORDER BY total_invested DESC;

-- Query 5: Funds with expense ratio less than 1%
SELECT scheme_name, fund_house, expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- Query 6: Best Sharpe ratio funds
SELECT d.scheme_name, d.category, fp.sharpe_ratio
FROM fact_performance fp
JOIN dim_fund d ON fp.amfi_code = d.amfi_code
ORDER BY fp.sharpe_ratio DESC
LIMIT 5;

-- Query 7: Funds with positive alpha
SELECT d.scheme_name, d.fund_house, fp.alpha, fp.beta
FROM fact_performance fp
JOIN dim_fund d ON fp.amfi_code = d.amfi_code
WHERE fp.alpha > 0
ORDER BY fp.alpha DESC;

-- Query 8: Transaction count by age group
SELECT age_group,
       COUNT(*) as num_transactions,
       ROUND(AVG(amount_inr), 2) as avg_amount
FROM fact_transactions
GROUP BY age_group
ORDER BY avg_amount DESC;

-- Query 9: Nifty 50 highest closing value
SELECT date, close_value
FROM fact_benchmark
WHERE index_name = 'NIFTY50'
ORDER BY close_value DESC
LIMIT 5;

-- Query 10: Fund count by category
SELECT category,
       COUNT(*) as num_funds,
       ROUND(AVG(expense_ratio_pct), 2) as avg_expense_ratio
FROM dim_fund
GROUP BY category;