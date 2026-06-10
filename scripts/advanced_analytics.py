import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

print("="*55)
print("DAY 6: ADVANCED ANALYTICS + RISK METRICS")
print("="*55)

# Load data
df_nav  = pd.read_csv("data/processed/returns_computed.csv", parse_dates=['date'])
df_fund = pd.read_csv("data/processed/clean_fund_master.csv")
df_tx   = pd.read_csv("data/processed/clean_transactions.csv", parse_dates=['transaction_date'])
df_hold = pd.read_csv("data/processed/clean_portfolio_holdings.csv")
df_perf = pd.read_csv("data/processed/clean_performance.csv")

print("✅ Data loaded!")

# ══════════════════════════════════════════════════════
# TASK 1: Historical VaR (95%) and CVaR
# ══════════════════════════════════════════════════════
print("\n📊 Task 1: Computing VaR & CVaR...")

var_rows = []
for code, grp in df_nav.groupby('amfi_code'):
    returns = grp['daily_return'].dropna()
    if len(returns) < 30:
        continue
    var_95  = np.percentile(returns, 5)
    cvar_95 = returns[returns <= var_95].mean()
    var_rows.append({
        'amfi_code': code,
        'var_95_pct':  round(var_95 * 100, 4),
        'cvar_95_pct': round(cvar_95 * 100, 4)
    })

df_var = pd.DataFrame(var_rows)
df_var = df_var.merge(df_fund[['amfi_code','scheme_name','category']], on='amfi_code')
df_var = df_var.sort_values('var_95_pct')
df_var.to_csv("data/processed/var_cvar_report.csv", index=False)

print("✅ VaR & CVaR computed!")
print("\nTop 5 Highest Risk Funds (worst VaR):")
print(df_var[['scheme_name','var_95_pct','cvar_95_pct']].head(5).to_string(index=False))
print("\nTop 5 Lowest Risk Funds (best VaR):")
print(df_var[['scheme_name','var_95_pct','cvar_95_pct']].tail(5).to_string(index=False))

# ══════════════════════════════════════════════════════
# TASK 2: Rolling 90-day Sharpe Ratio
# ══════════════════════════════════════════════════════
print("\n📊 Task 2: Computing Rolling Sharpe Ratio...")

RF_daily = 0.065 / 252

# Pick 5 funds
top5_codes = df_nav['amfi_code'].unique()[:5]

fig, ax = plt.subplots(figsize=(14, 6))

for code in top5_codes:
    grp = df_nav[df_nav['amfi_code'] == code].sort_values('date')
    returns = grp.set_index('date')['daily_return']
    rolling_sharpe = (
        (returns - RF_daily).rolling(90).mean() /
        returns.rolling(90).std()
    ) * np.sqrt(252)

    name = df_fund[df_fund['amfi_code']==code]['scheme_name'].values
    label = name[0].split('-')[0].strip() if len(name) > 0 else str(code)
    ax.plot(rolling_sharpe.index, rolling_sharpe.values,
            linewidth=1.5, label=label)

ax.axhline(y=1, color='red', linestyle='--', alpha=0.5, label='Sharpe=1 (Good)')
ax.axhline(y=0, color='gray', linestyle=':', alpha=0.3)
ax.set_title('Rolling 90-Day Sharpe Ratio (5 Funds)',
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Date', fontsize=11)
ax.set_ylabel('Rolling Sharpe Ratio', fontsize=11)
ax.legend(fontsize=8)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("reports/charts/rolling_sharpe_chart.png", dpi=150)
plt.close()
print("✅ Rolling Sharpe chart saved!")

# ══════════════════════════════════════════════════════
# TASK 3: Investor Cohort Analysis
# ══════════════════════════════════════════════════════
print("\n📊 Task 3: Investor Cohort Analysis...")

# Group investors by first transaction year
first_tx = df_tx.groupby('investor_id')['transaction_date'].min().reset_index()
first_tx['cohort_year'] = first_tx['transaction_date'].dt.year
df_tx = df_tx.merge(first_tx[['investor_id','cohort_year']], on='investor_id')

cohort = df_tx.groupby('cohort_year').agg(
    num_investors  = ('investor_id', 'nunique'),
    avg_sip_amount = ('amount_inr', 'mean'),
    total_invested = ('amount_inr', 'sum'),
    num_transactions = ('investor_id', 'count')
).reset_index()

cohort['avg_sip_amount'] = cohort['avg_sip_amount'].round(2)
cohort['total_invested']  = cohort['total_invested'].round(2)
cohort.to_csv("data/processed/cohort_analysis.csv", index=False)

print("✅ Cohort Analysis done!")
print(cohort.to_string(index=False))

# ══════════════════════════════════════════════════════
# TASK 4: SIP Continuation Analysis
# ══════════════════════════════════════════════════════
print("\n📊 Task 4: SIP Continuation Analysis...")

sip_tx = df_tx[df_tx['transaction_type'] == 'SIP'].copy()
sip_tx = sip_tx.sort_values(['investor_id','transaction_date'])

# Investors with 6+ SIP transactions
sip_count = sip_tx.groupby('investor_id').size()
active_sip = sip_count[sip_count >= 6].index

sip_active = sip_tx[sip_tx['investor_id'].isin(active_sip)].copy()

# Compute average gap between transactions
sip_active['prev_date'] = sip_active.groupby('investor_id')['transaction_date'].shift(1)
sip_active['gap_days'] = (sip_active['transaction_date'] - sip_active['prev_date']).dt.days
sip_gap = sip_active.groupby('investor_id')['gap_days'].mean().reset_index()
sip_gap.columns = ['investor_id','avg_gap_days']
sip_gap['status'] = sip_gap['avg_gap_days'].apply(
    lambda x: 'At-Risk' if x > 35 else 'Regular')

sip_gap.to_csv("data/processed/sip_continuity.csv", index=False)
print("✅ SIP Continuity Analysis done!")
print(f"   Total active SIP investors: {len(sip_gap)}")
print(f"   At-Risk investors (gap > 35 days): {len(sip_gap[sip_gap['status']=='At-Risk'])}")
print(f"   Regular investors: {len(sip_gap[sip_gap['status']=='Regular'])}")

# ══════════════════════════════════════════════════════
# TASK 5: Fund Recommender
# ══════════════════════════════════════════════════════
print("\n📊 Task 5: Fund Recommender...")

df_rec = df_perf.copy()
df_rec['risk_category'] = df_rec['risk_grade']

def recommend_funds(risk_appetite):
    """Recommend top 3 funds based on investor risk appetite"""
    filtered = df_rec[df_rec['risk_category'] == risk_appetite]
    if len(filtered) == 0:
        return pd.DataFrame()
    top3 = filtered.nlargest(3, 'sharpe_ratio')[
        ['scheme_name','fund_house','risk_grade','sharpe_ratio','return_3yr_pct']]
    return top3

print("\n🔵 Low Risk Investor:")
print(recommend_funds('Low').to_string(index=False))

print("\n🟡 Moderate Risk Investor:")
print(recommend_funds('Moderate').to_string(index=False))

print("\n🔴 High Risk Investor:")
print(recommend_funds('Very High').to_string(index=False))

# Save recommender as script
recommender_code = '''
import pandas as pd

df_perf = pd.read_csv("data/processed/clean_performance.csv")
df_fund = pd.read_csv("data/processed/clean_fund_master.csv")
df_rec  = df_perf.merge(df_fund[["amfi_code","risk_category"]], on="amfi_code")

def recommend_funds(risk_appetite):
    filtered = df_rec[df_rec["risk_category"] == risk_appetite]
    if len(filtered) == 0:
        return "No funds found for this risk category"
    top3 = filtered.nlargest(3, "sharpe_ratio")[
        ["scheme_name","risk_category","sharpe_ratio","return_3yr_pct"]]
    return top3

# Example usage
print(recommend_funds("Low"))
print(recommend_funds("Moderate"))
print(recommend_funds("Very High"))
'''
with open("scripts/recommender.py", "w") as f:
    f.write(recommender_code)
print("\n✅ recommender.py saved!")

# ══════════════════════════════════════════════════════
# TASK 6: Sector Concentration (HHI)
# ══════════════════════════════════════════════════════
print("\n📊 Task 6: Sector Concentration Analysis (HHI)...")

hhi_rows = []
for code, grp in df_hold.groupby('amfi_code'):
    weights = grp['weight_pct'] / 100
    hhi = (weights ** 2).sum()
    hhi_rows.append({'amfi_code': code, 'hhi_score': round(hhi, 4)})

df_hhi = pd.DataFrame(hhi_rows)
df_hhi = df_hhi.merge(df_fund[['amfi_code','scheme_name']], on='amfi_code')
df_hhi = df_hhi.sort_values('hhi_score', ascending=False)
df_hhi.to_csv("data/processed/sector_hhi.csv", index=False)

# HHI Chart
fig, ax = plt.subplots(figsize=(12, 6))
colors = ['#e74c3c' if h > 0.15 else '#2ecc71' for h in df_hhi['hhi_score']]
ax.bar(df_hhi['scheme_name'].str.split('-').str[0].str.strip(),
       df_hhi['hhi_score'], color=colors, edgecolor='white')
ax.axhline(y=0.15, color='red', linestyle='--', label='High Concentration (0.15)')
ax.set_title('Portfolio Sector Concentration (HHI Score)',
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Fund', fontsize=10)
ax.set_ylabel('HHI Score', fontsize=11)
ax.legend()
plt.xticks(rotation=90, fontsize=7)
plt.tight_layout()
plt.savefig("reports/charts/sector_hhi_chart.png", dpi=150)
plt.close()
print("✅ Sector HHI analysis done!")
print(f"\nMost concentrated fund: {df_hhi.iloc[0]['scheme_name']} — HHI: {df_hhi.iloc[0]['hhi_score']}")

print("\n" + "="*55)
print("🎉 ALL DAY 6 TASKS COMPLETE!")
print("="*55)
print("\nFiles saved:")
print("  ✅ data/processed/var_cvar_report.csv")
print("  ✅ data/processed/cohort_analysis.csv")
print("  ✅ data/processed/sip_continuity.csv")
print("  ✅ data/processed/sector_hhi.csv")
print("  ✅ reports/charts/rolling_sharpe_chart.png")
print("  ✅ reports/charts/sector_hhi_chart.png")
print("  ✅ scripts/recommender.py")