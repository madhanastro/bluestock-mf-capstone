# Bluestock Fintech — Mutual Fund Analytics Platform
### Capstone Project | Data Analyst Intern | June 2026

**Intern:** Madhankumar V  
**Company:** Bluestock Fintech Pvt. Ltd.  
**Duration:** 28 May 2026 – 28 Jul 2026  
**Role:** Data Analyst Intern

---

## 🎯 Project Overview

A full-stack Mutual Fund Analytics Platform built for Bluestock Fintech that:
- Ingests publicly available data from AMFI India and mfapi.in
- Transforms raw data through a robust ETL pipeline
- Stores data in a normalised SQLite database (star schema)
- Analyses 40 fund schemes across 10 AMCs with 87,000+ rows
- Computes risk metrics: Sharpe, Sortino, Alpha, Beta, VaR, CVaR
- Presents insights via an interactive Power BI dashboard

---

## 📊 Key Results

| Metric | Value |
|--------|-------|
| Total funds analysed | 40 schemes |
| NAV records processed | 46,000 rows |
| Investor transactions | 32,778 rows |
| Best performing fund | SBI Small Cap (23.39% 3yr CAGR) |
| Best Sharpe ratio | Mirae Asset Large Cap (1.4483) |
| Industry AUM | ₹81 lakh crore |
| SIP ATH | ₹31,002 Cr (Dec 2025) |

---

## 🗂️ Project Structure

bluestock_mf_capstone/
├── data/
│   ├── raw/          ← 10 original CSV datasets
│   ├── processed/    ← Cleaned + computed CSVs
│   └── db/           ← SQLite database
├── notebooks/        ← Jupyter analysis notebooks
│   ├── EDA_Analysis.ipynb
│   ├── Performance_Analytics.ipynb
│   └── Advanced_Analytics.ipynb
├── scripts/          ← Python ETL and analytics scripts
│   ├── data_ingestion.py
│   ├── data_cleaning.py
│   ├── load_database.py
│   ├── eda_analysis.py
│   ├── performance_analytics.py
│   ├── advanced_analytics.py
│   └── recommender.py
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── dashboard/        ← Power BI .pbix file
├── reports/
│   ├── charts/       ← 17 exported PNG charts
│   ├── EDA_Findings.md
│   ├── Final_Report.md
│   └── Dashboard.pdf
├── run_pipeline.py   ← Master pipeline script
└── requirements.txt
---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run full pipeline
```bash
python run_pipeline.py
```

### 3. Run individual scripts
```bash
python scripts/data_ingestion.py
python scripts/data_cleaning.py
python scripts/load_database.py
python scripts/eda_analysis.py
python scripts/performance_analytics.py
python scripts/advanced_analytics.py
```

### 4. Open dashboard
Open `dashboard/bluestock_mf_dashboard.pbix` in Power BI Desktop

---

## 📦 Datasets (10 files, 87K+ rows)

| File | Description | Rows |
|------|-------------|------|
| 01_fund_master.csv | 40 scheme metadata | 40 |
| 02_nav_history.csv | Daily NAV 2022–2026 | 46,000 |
| 03_aum_by_fund_house.csv | Quarterly AUM top 10 AMCs | 90 |
| 04_monthly_sip_inflows.csv | Monthly SIP data | 48 |
| 05_category_inflows.csv | Net inflows by category | 144 |
| 06_industry_folio_count.csv | Total folios growth | 21 |
| 07_scheme_performance.csv | Risk-return metrics | 40 |
| 08_investor_transactions.csv | SIP/Lumpsum/Redemption | 32,778 |
| 09_portfolio_holdings.csv | Equity holdings | 322 |
| 10_benchmark_indices.csv | Nifty/BSE indices | 8,050 |

---

## 🔑 Key Findings

1. **SBI Small Cap** delivered highest 3-year CAGR of 23.39%
2. **SIP inflows** hit all-time high of ₹31,002 Cr in Dec 2025
3. **T30 cities** contribute 66.3% of all investments
4. **97.7% of SIP investors** have irregular payment gaps (>35 days)
5. **Folio count doubled** from 13.26 to 26.12 crore in 4 years
6. **ICICI Pru Midcap** scores highest in composite scorecard (84.50/100)
7. **Liquid funds** safest with VaR of just -0.02% daily

---

## 🛠️ Tech Stack

| Category | Tool |
|----------|------|
| Language | Python 3.10 |
| Data Processing | Pandas, NumPy |
| Visualisation | Matplotlib, Seaborn, Plotly |
| Database | SQLite + SQLAlchemy |
| Statistics | SciPy |
| Notebooks | Jupyter |
| Dashboard | Power BI Desktop |
| Version Control | Git + GitHub |

---

## 📁 Data Sources

- AMFI India: [amfiindia.com](https://www.amfiindia.com)
- mfapi.in: [api.mfapi.in](https://api.mfapi.in)
- NSE India: [nseindia.com](https://www.nseindia.com)

> All data is for educational purposes only. Not financial advice.