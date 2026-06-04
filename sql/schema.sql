-- Bluestock Fintech MF Capstone
-- Database Schema - Day 2

-- Table 1: Fund Master (dimension table)
CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    fund_house TEXT,
    scheme_name TEXT,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    benchmark TEXT,
    expense_ratio_pct REAL,
    fund_manager TEXT,
    risk_category TEXT
);

-- Table 2: NAV History (fact table)
CREATE TABLE IF NOT EXISTS fact_nav (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    date TEXT,
    nav REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Table 3: Investor Transactions (fact table)
CREATE TABLE IF NOT EXISTS fact_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id TEXT,
    transaction_date TEXT,
    amfi_code INTEGER,
    transaction_type TEXT,
    amount_inr INTEGER,
    state TEXT,
    city TEXT,
    city_tier TEXT,
    age_group TEXT,
    gender TEXT,
    payment_mode TEXT,
    kyc_status TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Table 4: Scheme Performance (fact table)
CREATE TABLE IF NOT EXISTS fact_performance (
    amfi_code INTEGER PRIMARY KEY,
    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,
    alpha REAL,
    beta REAL,
    sharpe_ratio REAL,
    sortino_ratio REAL,
    max_drawdown_pct REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Table 5: Benchmark Indices (fact table)
CREATE TABLE IF NOT EXISTS fact_benchmark (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    index_name TEXT,
    close_value REAL
);