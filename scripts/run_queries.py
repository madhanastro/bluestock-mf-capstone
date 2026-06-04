import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("data/db/bluestock_mf.db")

print("="*55)
print("BLUESTOCK MF - 10 SQL QUERIES RESULTS")
print("="*55)

# Query 1: Top 5 funds by 3 year return
print("\n📊 Query 1: Top 5 Funds by 3-Year Return")
print("-"*55)
q1 = """
SELECT d.scheme_name, d.fund_house, fp.return_3yr_pct
FROM fact_performance fp
JOIN dim_fund d ON fp.amfi_code = d.amfi_code
ORDER BY return_3yr_pct DESC LIMIT 5
"""
print(pd.read_sql(q1, conn).to_string(index=False))

# Query 2: Average NAV per fund in 2025
print("\n📊 Query 2: Top 10 Funds by Average NAV in 2025")
print("-"*55)
q2 = """
SELECT d.scheme_name, ROUND(AVG(n.nav),2) as avg_nav
FROM fact_nav n
JOIN dim_fund d ON n.amfi_code = d.amfi_code
WHERE n.date LIKE '2025%'
GROUP BY n.amfi_code
ORDER BY avg_nav DESC LIMIT 10
"""
print(pd.read_sql(q2, conn).to_string(index=False))

# Query 3: Total transactions by type
print("\n📊 Query 3: Transactions by Type")
print("-"*55)
q3 = """
SELECT transaction_type,
       COUNT(*) as total_count,
       SUM(amount_inr) as total_amount
FROM fact_transactions
GROUP BY transaction_type
"""
print(pd.read_sql(q3, conn).to_string(index=False))

# Query 4: SIP by state
print("\n📊 Query 4: Top 5 States by SIP Investment")
print("-"*55)
q4 = """
SELECT state, COUNT(*) as num_transactions,
       SUM(amount_inr) as total_invested
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY state
ORDER BY total_invested DESC LIMIT 5
"""
print(pd.read_sql(q4, conn).to_string(index=False))

# Query 5: Funds with expense ratio < 1%
print("\n📊 Query 5: Funds with Expense Ratio < 1%")
print("-"*55)
q5 = """
SELECT scheme_name, fund_house, expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC LIMIT 5
"""
print(pd.read_sql(q5, conn).to_string(index=False))

# Query 6: Best Sharpe ratio
print("\n📊 Query 6: Top 5 Funds by Sharpe Ratio")
print("-"*55)
q6 = """
SELECT d.scheme_name, d.category, fp.sharpe_ratio
FROM fact_performance fp
JOIN dim_fund d ON fp.amfi_code = d.amfi_code
ORDER BY fp.sharpe_ratio DESC LIMIT 5
"""
print(pd.read_sql(q6, conn).to_string(index=False))

# Query 7: Positive alpha funds
print("\n📊 Query 7: Funds with Positive Alpha")
print("-"*55)
q7 = """
SELECT d.scheme_name, d.fund_house, fp.alpha, fp.beta
FROM fact_performance fp
JOIN dim_fund d ON fp.amfi_code = d.amfi_code
WHERE fp.alpha > 0
ORDER BY fp.alpha DESC LIMIT 5
"""
print(pd.read_sql(q7, conn).to_string(index=False))

# Query 8: By age group
print("\n📊 Query 8: Transactions by Age Group")
print("-"*55)
q8 = """
SELECT age_group, COUNT(*) as num_transactions,
       ROUND(AVG(amount_inr),2) as avg_amount
FROM fact_transactions
GROUP BY age_group
ORDER BY avg_amount DESC
"""
print(pd.read_sql(q8, conn).to_string(index=False))

# Query 9: Nifty 50 highest values
print("\n📊 Query 9: Nifty 50 Top 5 Closing Values")
print("-"*55)
q9 = """
SELECT date, close_value
FROM fact_benchmark
WHERE index_name = 'NIFTY50'
ORDER BY close_value DESC LIMIT 5
"""
print(pd.read_sql(q9, conn).to_string(index=False))

# Query 10: Fund count by category
print("\n📊 Query 10: Fund Count by Category")
print("-"*55)
q10 = """
SELECT category, COUNT(*) as num_funds,
       ROUND(AVG(expense_ratio_pct),2) as avg_expense_ratio
FROM dim_fund
GROUP BY category
"""
print(pd.read_sql(q10, conn).to_string(index=False))

conn.close()
print("\n✅ All 10 queries executed successfully!")