import pandas as pd
import os

# Create processed folder if it doesn't exist
os.makedirs("data/processed", exist_ok=True)

print("="*50)
print("TASK 1: CLEANING NAV HISTORY")
print("="*50)

# Load raw NAV data
df_nav = pd.read_csv("data/raw/02_nav_history.csv")

print(f"Before cleaning: {df_nav.shape}")

# Step 1: Convert date column to proper date format
df_nav['date'] = pd.to_datetime(df_nav['date'])

# Step 2: Sort by fund code and date
df_nav = df_nav.sort_values(['amfi_code', 'date'])

# Step 3: Remove duplicates
df_nav = df_nav.drop_duplicates(subset=['amfi_code', 'date'])

# Step 4: Remove rows where NAV is 0 or negative
df_nav = df_nav[df_nav['nav'] > 0]

# Step 5: Forward fill missing dates (holidays/weekends)
df_nav = df_nav.reset_index(drop=True)

print(f"After cleaning : {df_nav.shape}")
print(f"\nNull values: {df_nav.isnull().sum().sum()}")
print(f"Date range: {df_nav['date'].min()} to {df_nav['date'].max()}")
print(f"\nSample:")
print(df_nav.head(3))

# Save cleaned file
df_nav.to_csv("data/processed/clean_nav.csv", index=False)
print("\n✅ clean_nav.csv saved!")



print("\n" + "="*50)
print("TASK 2: CLEANING INVESTOR TRANSACTIONS")
print("="*50)

df_tx = pd.read_csv("data/raw/08_investor_transactions.csv")
print(f"Before cleaning: {df_tx.shape}")

# Step 1: Convert date to proper format
df_tx['transaction_date'] = pd.to_datetime(df_tx['transaction_date'])

# Step 2: Standardise transaction_type (fix any lowercase/uppercase issues)
df_tx['transaction_type'] = df_tx['transaction_type'].str.strip().str.title()
df_tx['transaction_type'] = df_tx['transaction_type'].str.replace('Sip', 'SIP')

# Step 3: Remove rows where amount is 0 or negative
df_tx = df_tx[df_tx['amount_inr'] > 0]

# Step 4: Remove duplicates
df_tx = df_tx.drop_duplicates()

# Step 5: Check KYC values
print(f"\nKYC Status values: {df_tx['kyc_status'].unique()}")
print(f"Transaction types: {df_tx['transaction_type'].unique()}")

print(f"\nAfter cleaning: {df_tx.shape}")
print(f"Null values: {df_tx.isnull().sum().sum()}")

# Save
df_tx.to_csv("data/processed/clean_transactions.csv", index=False)
print("✅ clean_transactions.csv saved!")



print("\n" + "="*50)
print("TASK 3: CLEANING SCHEME PERFORMANCE")
print("="*50)

df_perf = pd.read_csv("data/raw/07_scheme_performance.csv")
print(f"Before cleaning: {df_perf.shape}")

# Step 1: Remove nulls
df_perf = df_perf.dropna()

# Step 2: Validate expense ratio range (should be 0.1% to 2.5%)
invalid_exp = df_perf[~df_perf['expense_ratio_pct'].between(0.1, 2.5)]
print(f"Invalid expense ratios: {len(invalid_exp)}")

# Step 3: Flag negative Sharpe ratios
negative_sharpe = df_perf[df_perf['sharpe_ratio'] < 0]
print(f"Negative Sharpe ratios: {len(negative_sharpe)}")

print(f"After cleaning: {df_perf.shape}")
print(f"Null values: {df_perf.isnull().sum().sum()}")

# Save
df_perf.to_csv("data/processed/clean_performance.csv", index=False)
print("✅ clean_performance.csv saved!")



print("\n" + "="*50)
print("TASK 4: CLEANING REMAINING DATASETS")
print("="*50)

# Fund Master
df_master = pd.read_csv("data/raw/01_fund_master.csv")
df_master = df_master.drop_duplicates()
df_master['launch_date'] = pd.to_datetime(df_master['launch_date'])
df_master.to_csv("data/processed/clean_fund_master.csv", index=False)
print(f"✅ clean_fund_master.csv saved! Shape: {df_master.shape}")

# AUM by Fund House
df_aum = pd.read_csv("data/raw/03_aum_by_fund_house.csv")
df_aum = df_aum.drop_duplicates()
df_aum['date'] = pd.to_datetime(df_aum['date'])
df_aum.to_csv("data/processed/clean_aum.csv", index=False)
print(f"✅ clean_aum.csv saved! Shape: {df_aum.shape}")

# Monthly SIP Inflows
df_sip = pd.read_csv("data/raw/04_monthly_sip_inflows.csv")
df_sip = df_sip.drop_duplicates()
df_sip['month'] = pd.to_datetime(df_sip['month'])
df_sip['yoy_growth_pct'] = df_sip['yoy_growth_pct'].fillna(0)
df_sip.to_csv("data/processed/clean_sip.csv", index=False)
print(f"✅ clean_sip.csv saved! Shape: {df_sip.shape}")

# Category Inflows
df_cat = pd.read_csv("data/raw/05_category_inflows.csv")
df_cat = df_cat.drop_duplicates()
df_cat['month'] = pd.to_datetime(df_cat['month'])
df_cat.to_csv("data/processed/clean_category_inflows.csv", index=False)
print(f"✅ clean_category_inflows.csv saved! Shape: {df_cat.shape}")

# Folio Count
df_folio = pd.read_csv("data/raw/06_industry_folio_count.csv")
df_folio = df_folio.drop_duplicates()
df_folio['month'] = pd.to_datetime(df_folio['month'])
df_folio.to_csv("data/processed/clean_folio_count.csv", index=False)
print(f"✅ clean_folio_count.csv saved! Shape: {df_folio.shape}")

# Portfolio Holdings
df_hold = pd.read_csv("data/raw/09_portfolio_holdings.csv")
df_hold = df_hold.drop_duplicates()
df_hold['portfolio_date'] = pd.to_datetime(df_hold['portfolio_date'])
df_hold.to_csv("data/processed/clean_portfolio_holdings.csv", index=False)
print(f"✅ clean_portfolio_holdings.csv saved! Shape: {df_hold.shape}")

# Benchmark Indices
df_bench = pd.read_csv("data/raw/10_benchmark_indices.csv")
df_bench = df_bench.drop_duplicates()
df_bench['date'] = pd.to_datetime(df_bench['date'])
df_bench = df_bench[df_bench['close_value'] > 0]
df_bench.to_csv("data/processed/clean_benchmark.csv", index=False)
print(f"✅ clean_benchmark.csv saved! Shape: {df_bench.shape}")

print("\n🎉 ALL 10 DATASETS CLEANED AND SAVED!")