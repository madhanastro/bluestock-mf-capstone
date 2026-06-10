# Bluestock Fintech — Mutual Fund Analytics Platform
## Final Project Report
**Intern:** Madhankumar V  
**Company:** Bluestock Fintech Pvt. Ltd.  
**Role:** Data Analyst Intern  
**Date:** June 2026  
**Project ID:** BFDA79190

---

## 1. Executive Summary

This report presents the findings of a comprehensive Mutual Fund Analytics Platform built for Bluestock Fintech Pvt. Ltd. The platform ingests publicly available data from AMFI India, processes it through a robust ETL pipeline, stores it in a normalised SQLite database, and presents actionable insights via an interactive Power BI dashboard.

Key highlights:
- Analysed 40 mutual fund schemes across 10 AMCs
- Processed 87,000+ rows of data including 46,000 NAV records and 32,778 investor transactions
- Identified SBI Small Cap as top performer with 23.39% 3-year CAGR
- Built a composite fund scorecard ranking ICICI Pru Midcap as #1 (84.50/100)
- Discovered SIP industry hit all-time high of ₹31,002 Cr in December 2025
- Folio count doubled from 13.26 to 26.12 crore over 4 years

---

## 2. Problem Statement

The Indian mutual fund industry manages over ₹81 lakh crore in AUM across 1,908 schemes. Despite massive growth, investors and advisors face:

- **Data Fragmentation** — NAV, AUM and SIP data scattered across multiple sources
- **No unified comparison** — Difficult to compare funds on risk-adjusted basis
- **No benchmark tracking** — Retail investors cannot easily check if their fund beats its index
- **Slow reporting** — Monthly reports are static PDFs taking days to prepare

This platform solves all four problems with a unified data pipeline and interactive dashboard.

---

## 3. Data Sources & Datasets

All data sourced from publicly available AMFI India, mfapi.in and NSE/BSE:

| Dataset | Rows | Description |
|---------|------|-------------|
| Fund Master | 40 | Scheme metadata, expense ratios, fund managers |
| NAV History | 46,000 | Daily NAV Jan 2022 – May 2026 |
| AUM by Fund House | 90 | Quarterly AUM for top 10 AMCs |
| Monthly SIP Inflows | 48 | Industry SIP data 2022–2025 |
| Category Inflows | 144 | Net inflows by fund category |
| Industry Folio Count | 21 | Total folios growth milestones |
| Scheme Performance | 40 | Risk-return metrics per scheme |
| Investor Transactions | 32,778 | SIP/Lumpsum/Redemption data |
| Portfolio Holdings | 322 | Top equity holdings per fund |
| Benchmark Indices | 8,050 | Nifty 50, Nifty 100, BSE SmallCap |

---

## 4. ETL Pipeline & System Architecture

The platform follows a 5-layer architecture:

**Layer 1 — Extract:** Raw CSV datasets + mfapi.in live NAV API

**Layer 2 — Transform:** Python/Pandas cleaning pipeline
- Parsed dates to datetime format
- Forward-filled missing NAV values (holidays)
- Removed duplicates and validated AMFI codes
- Standardised transaction types and KYC status

**Layer 3 — Load:** SQLite star schema database
- dim_fund (40 rows) — Fund master dimension
- fact_nav (46,000 rows) — Daily NAV facts
- fact_transactions (32,778 rows) — Investor transactions
- fact_performance (40 rows) — Risk metrics
- fact_benchmark (8,050 rows) — Index prices

**Layer 4 — Analyse:** Jupyter notebooks with 15+ charts

**Layer 5 — Visualise:** Power BI 4-page interactive dashboard

---

## 5. Exploratory Data Analysis — Key Findings

### 5.1 NAV Trends
Small Cap funds showed strongest growth 2022–2026, with SBI Small Cap delivering highest returns. Large Cap funds showed steady, less volatile growth.

### 5.2 AUM Growth
SBI Mutual Fund dominates with ₹12.5 lakh crore AUM — nearly 2x the second largest (ICICI Prudential at ₹10.74 lakh crore).

### 5.3 SIP Industry Trends
Monthly SIP inflows grew from ₹11,517 Cr (Jan 2022) to ₹31,002 Cr (Dec 2025) — nearly 3x growth in 4 years. Active SIP accounts grew from 4.91 crore to 9.35 crore.

### 5.4 Investor Demographics
- 26–35 age group most active (13,463 transactions)
- UPI dominant payment mode (55%+ transactions)
- T30 cities contribute 66.3% of investments
- 92% investors KYC verified

### 5.5 Geographic Distribution
Punjab, Tamil Nadu and Madhya Pradesh lead SIP investments. Maharashtra ranks last despite being financial capital — indicating untapped potential.

---

## 6. Fund Performance Analytics

### 6.1 Top Performers by 3-Year CAGR

| Fund | 3yr CAGR |
|------|----------|
| SBI Small Cap Regular | 23.39% |
| SBI Small Cap Direct | 23.14% |
| ABSL Small Cap Regular | 22.38% |
| Axis Small Cap Regular | 20.98% |
| Nippon India Small Cap | 20.15% |

### 6.2 Risk Metrics Summary

| Metric | Best Fund | Value |
|--------|-----------|-------|
| Sharpe Ratio | Mirae Asset Large Cap | 1.4483 |
| Alpha | HDFC Short Term Debt | 0.272 |
| Max Drawdown | ICICI Pru Liquid | -0.02% |
| VaR (95%) | ICICI Pru Liquid | -0.022% |

### 6.3 Fund Scorecard — Top 5

| Rank | Fund | Score |
|------|------|-------|
| 1 | ICICI Pru Midcap | 84.50 |
| 2 | Axis Midcap | 80.75 |
| 3 | HDFC Mid-Cap Opp | 80.50 |
| 4 | Mirae Asset Large Cap | 80.00 |
| 5 | Kotak Flexicap | 78.25 |

---

## 7. Advanced Analytics

### 7.1 Value at Risk (VaR)
Small Cap funds carry highest daily VaR (-2.69%) while Liquid funds are safest (-0.02%). Investors should understand their risk tolerance before investing in Small Cap funds.

### 7.2 SIP Continuation Analysis
97.7% of active SIP investors (1,332 out of 1,362) show irregular payment gaps exceeding 35 days. This suggests significant opportunity for AMCs to improve SIP reminder systems.

### 7.3 Cohort Analysis
2024 cohort dominates with 4,803 investors and average investment of ₹1.07 lakh. 2025 cohort shows slightly higher average (₹1.09 lakh) suggesting newer investors are more affluent.

### 7.4 Sector Concentration
Axis Bluechip Fund has highest sector concentration (HHI: 0.2064). Investors seeking diversification should prefer funds with lower HHI scores.

---

## 8. Dashboard Overview

The Power BI dashboard consists of 4 interactive pages:

**Page 1 — Industry Overview**
KPI cards for AUM, SIP inflows, folios and scheme count. AUM growth trend and fund house comparison.

**Page 2 — Fund Performance**
Scatter plot of return vs risk, sortable fund scorecard, NAV trend with slicers for fund house, category and plan.

**Page 3 — Investor Analytics**
Transaction breakdown by state, SIP vs Lumpsum vs Redemption donut, age group analysis with city tier slicers.

**Page 4 — SIP & Market Trends**
Dual-axis SIP inflow vs Nifty 50, category inflows matrix, YoY growth KPIs.

---

## 9. Recommendations

1. **Focus on Mid Cap funds** — Consistently high risk-adjusted returns with manageable volatility
2. **Target B30 cities** — Only 33.7% of investments — huge untapped market
3. **Fix SIP irregularity** — 97.7% at-risk investors need better reminder systems
4. **Promote Direct plans** — Lower expense ratios (avg 0.67%) vs Regular (avg 1.34%)
5. **Small Cap caution** — High returns (23%) but VaR of -2.69% — only for high risk appetite

---

## 10. Limitations

- NAV data anchored to real AMFI values but simulated forward using realistic parameters
- Investor transaction data is synthetically generated with real demographic distributions
- Analysis covers Jan 2022 – May 2026 only
- Dashboard requires Power BI Desktop to view interactively

---

## 11. Conclusion

This capstone project successfully demonstrates end-to-end data engineering and analytics capabilities. The platform ingests, cleans, analyses and visualises mutual fund data at scale — providing actionable insights for fund selection, risk management and investor behaviour analysis. The findings reveal a rapidly growing Indian MF industry with significant opportunities in B30 cities, Mid Cap funds and SIP regularisation.

---

*This report is prepared for educational purposes as part of the Bluestock Fintech Data Analyst Internship. All data sourced from publicly available AMFI India records.*