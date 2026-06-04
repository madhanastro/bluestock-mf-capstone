import pandas as pd
import sqlite3
import os

print("="*50)
print("CREATING BLUESTOCK MF DATABASE")
print("="*50)

# Create db folder if not exists
os.makedirs("data/db", exist_ok=True)

# Connect to SQLite database (creates it if not exists)
conn = sqlite3.connect("data/db/bluestock_mf.db")
cursor = conn.cursor()

print("✅ Database connected!")

# Read and execute schema.sql
with open("sql/schema.sql", "r") as f:
    schema = f.read()

cursor.executescript(schema)
conn.commit()
print("✅ Tables created!")

# ── Load dim_fund ─────────────────────────────────────
df_fund = pd.read_csv("data/processed/clean_fund_master.csv")
df_fund = df_fund[['amfi_code','fund_house','scheme_name','category',
                   'sub_category','plan','benchmark','expense_ratio_pct',
                   'fund_manager','risk_category']]
df_fund.to_sql('dim_fund', conn, if_exists='replace', index=False)
print(f"✅ dim_fund loaded: {len(df_fund)} rows")

# ── Load fact_nav ─────────────────────────────────────
df_nav = pd.read_csv("data/processed/clean_nav.csv")
df_nav.to_sql('fact_nav', conn, if_exists='replace', index=False)
print(f"✅ fact_nav loaded: {len(df_nav)} rows")

# ── Load fact_transactions ────────────────────────────
df_tx = pd.read_csv("data/processed/clean_transactions.csv")
df_tx = df_tx[['investor_id','transaction_date','amfi_code',
               'transaction_type','amount_inr','state','city',
               'city_tier','age_group','gender','payment_mode','kyc_status']]
df_tx.to_sql('fact_transactions', conn, if_exists='replace', index=False)
print(f"✅ fact_transactions loaded: {len(df_tx)} rows")

# ── Load fact_performance ─────────────────────────────
df_perf = pd.read_csv("data/processed/clean_performance.csv")
df_perf = df_perf[['amfi_code','return_1yr_pct','return_3yr_pct',
                   'return_5yr_pct','alpha','beta','sharpe_ratio',
                   'sortino_ratio','max_drawdown_pct']]
df_perf.to_sql('fact_performance', conn, if_exists='replace', index=False)
print(f"✅ fact_performance loaded: {len(df_perf)} rows")

# ── Load fact_benchmark ───────────────────────────────
df_bench = pd.read_csv("data/processed/clean_benchmark.csv")
df_bench.to_sql('fact_benchmark', conn, if_exists='replace', index=False)
print(f"✅ fact_benchmark loaded: {len(df_bench)} rows")

# ── Verify everything ─────────────────────────────────
print("\n" + "="*50)
print("DATABASE VERIFICATION")
print("="*50)

tables = ['dim_fund','fact_nav','fact_transactions',
          'fact_performance','fact_benchmark']

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"  {table}: {count:,} rows")

conn.close()
print("\n🎉 bluestock_mf.db created successfully!")