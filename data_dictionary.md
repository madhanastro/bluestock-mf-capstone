# Bluestock Fintech MF Capstone
# Data Dictionary

## 01. dim_fund (Fund Master)
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | INTEGER | Unique fund code from AMFI |
| fund_house | TEXT | AMC name (e.g. SBI Mutual Fund) |
| scheme_name | TEXT | Full fund name |
| category | TEXT | Equity / Debt |
| sub_category | TEXT | Large Cap / Mid Cap / Small Cap etc. |
| plan | TEXT | Regular or Direct |
| benchmark | TEXT | Index fund is compared against |
| expense_ratio_pct | REAL | Annual fee charged (%) |
| fund_manager | TEXT | Name of fund manager |
| risk_category | TEXT | Low / Moderate / High / Very High |

## 02. fact_nav (NAV History)
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | INTEGER | Foreign key to dim_fund |
| date | TEXT | Trading date (YYYY-MM-DD) |
| nav | REAL | Net Asset Value in Rs. |

## 03. fact_transactions (Investor Transactions)
| Column | Type | Description |
|--------|------|-------------|
| investor_id | TEXT | Unique investor ID |
| transaction_date | TEXT | Date of transaction |
| amfi_code | INTEGER | Fund invested in |
| transaction_type | TEXT | SIP / Lumpsum / Redemption |
| amount_inr | INTEGER | Transaction amount in Rs. |
| state | TEXT | Investor's state |
| city | TEXT | Investor's city |
| city_tier | TEXT | T30 or B30 city |
| age_group | TEXT | 18-25 / 26-35 / 36-45 / 46-55 / 56+ |
| gender | TEXT | Male / Female |
| payment_mode | TEXT | UPI / Net Banking / Mandate / Cheque |
| kyc_status | TEXT | Verified / Pending |

## 04. fact_performance (Scheme Performance)
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | INTEGER | Foreign key to dim_fund |
| return_1yr_pct | REAL | 1 year return % |
| return_3yr_pct | REAL | 3 year CAGR % |
| return_5yr_pct | REAL | 5 year CAGR % |
| alpha | REAL | Return above benchmark |
| beta | REAL | Market sensitivity (1.0 = same as market) |
| sharpe_ratio | REAL | Risk adjusted return (higher is better) |
| sortino_ratio | REAL | Downside risk adjusted return |
| max_drawdown_pct | REAL | Worst peak to trough decline % |

## 05. fact_benchmark (Benchmark Indices)
| Column | Type | Description |
|--------|------|-------------|
| date | TEXT | Trading date |
| index_name | TEXT | NIFTY50 / NIFTY100 / BSE SmallCap etc. |
| close_value | REAL | Closing value of index |