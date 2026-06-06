import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

print("="*55)
print("DAY 4: FUND PERFORMANCE ANALYTICS")
print("="*55)

# Load data
df_nav   = pd.read_csv("data/processed/clean_nav.csv", parse_dates=['date'])
df_fund  = pd.read_csv("data/processed/clean_fund_master.csv")
df_bench = pd.read_csv("data/processed/clean_benchmark.csv", parse_dates=['date'])

print("✅ Data loaded!")

# ══════════════════════════════════════════════════════
# TASK 1: Compute Daily Returns for all funds
# ══════════════════════════════════════════════════════
print("\n📊 Task 1: Computing Daily Returns...")

df_nav = df_nav.sort_values(['amfi_code','date'])
df_nav['daily_return'] = df_nav.groupby('amfi_code')['nav'].pct_change()
df_nav = df_nav.dropna(subset=['daily_return'])

# Annualised return per fund
ann_returns = df_nav.groupby('amfi_code')['daily_return'].apply(
    lambda x: (1 + x).prod() ** (252/len(x)) - 1
).reset_index()
ann_returns.columns = ['amfi_code','annualised_return']

df_nav.to_csv("data/processed/returns_computed.csv", index=False)
print(f"✅ Daily returns computed for {df_nav['amfi_code'].nunique()} funds")
print(f"   Sample annualised return: {ann_returns['annualised_return'].mean():.2%}")

# ══════════════════════════════════════════════════════
# TASK 2: Calculate CAGR for 1yr, 3yr, 5yr
# ══════════════════════════════════════════════════════
print("\n📊 Task 2: Calculating CAGR...")

def compute_cagr(group, years):
    """Compute CAGR for a given number of years"""
    end_date = group['date'].max()
    start_date = end_date - pd.DateOffset(years=years)
    subset = group[group['date'] >= start_date]
    if len(subset) < 2:
        return None
    nav_start = subset['nav'].iloc[0]
    nav_end   = subset['nav'].iloc[-1]
    n_years   = len(subset) / 252
    return (nav_end / nav_start) ** (1 / n_years) - 1

cagr_rows = []
for code, grp in df_nav.groupby('amfi_code'):
    cagr_rows.append({
        'amfi_code': code,
        'cagr_1yr':  compute_cagr(grp, 1),
        'cagr_3yr':  compute_cagr(grp, 3),
        'cagr_5yr':  compute_cagr(grp, 5),
    })

df_cagr = pd.DataFrame(cagr_rows)
df_cagr = df_cagr.merge(df_fund[['amfi_code','scheme_name','category']], on='amfi_code')
df_cagr.to_csv("data/processed/cagr_report.csv", index=False)
print("✅ CAGR computed!")
print(df_cagr[['scheme_name','cagr_1yr','cagr_3yr','cagr_5yr']].head(5).to_string(index=False))

# ══════════════════════════════════════════════════════
# TASK 3: Sharpe Ratio
# ══════════════════════════════════════════════════════
print("\n📊 Task 3: Computing Sharpe Ratio...")

RF = 0.065 / 252  # RBI repo rate 6.5% daily

sharpe_rows = []
for code, grp in df_nav.groupby('amfi_code'):
    excess = grp['daily_return'] - RF
    sharpe = (excess.mean() / excess.std()) * np.sqrt(252)
    sharpe_rows.append({'amfi_code': code, 'sharpe_ratio': round(sharpe, 4)})

df_sharpe = pd.DataFrame(sharpe_rows)
df_sharpe = df_sharpe.merge(df_fund[['amfi_code','scheme_name']], on='amfi_code')
df_sharpe = df_sharpe.sort_values('sharpe_ratio', ascending=False)
df_sharpe.to_csv("data/processed/sharpe_values.csv", index=False)
print("✅ Sharpe Ratio computed!")
print(f"   Top fund: {df_sharpe.iloc[0]['scheme_name']} — Sharpe: {df_sharpe.iloc[0]['sharpe_ratio']}")

# ══════════════════════════════════════════════════════
# TASK 4: Sortino Ratio
# ══════════════════════════════════════════════════════
print("\n📊 Task 4: Computing Sortino Ratio...")

sortino_rows = []
for code, grp in df_nav.groupby('amfi_code'):
    excess = grp['daily_return'] - RF
    downside = excess[excess < 0].std()
    sortino = (excess.mean() / downside) * np.sqrt(252) if downside > 0 else 0
    sortino_rows.append({'amfi_code': code, 'sortino_ratio': round(sortino, 4)})

df_sortino = pd.DataFrame(sortino_rows)
df_sortino = df_sortino.merge(df_fund[['amfi_code','scheme_name']], on='amfi_code')
df_sortino.to_csv("data/processed/sortino_values.csv", index=False)
print("✅ Sortino Ratio computed!")
print(f"   Top fund: {df_sortino.sort_values('sortino_ratio',ascending=False).iloc[0]['scheme_name']}")

# ══════════════════════════════════════════════════════
# TASK 5: Alpha & Beta vs Nifty 100
# ══════════════════════════════════════════════════════
print("\n📊 Task 5: Computing Alpha & Beta...")

# Get Nifty 100 benchmark returns
nifty100 = df_bench[df_bench['index_name']=='NIFTY100'].copy()
nifty100 = nifty100.sort_values('date')
nifty100['bench_return'] = nifty100['close_value'].pct_change()
nifty100 = nifty100.dropna()

alpha_beta_rows = []
for code, grp in df_nav.groupby('amfi_code'):
    merged = grp.merge(nifty100[['date','bench_return']], on='date', how='inner')
    if len(merged) < 30:
        continue
    slope, intercept, r, p, se = stats.linregress(
        merged['bench_return'], merged['daily_return'])
    alpha = intercept * 252
    beta  = slope
    alpha_beta_rows.append({
        'amfi_code': code,
        'alpha': round(alpha, 4),
        'beta':  round(beta, 4),
        'r_squared': round(r**2, 4)
    })

df_ab = pd.DataFrame(alpha_beta_rows)
df_ab = df_ab.merge(df_fund[['amfi_code','scheme_name','category']], on='amfi_code')
df_ab.to_csv("data/processed/alpha_beta.csv", index=False)
print("✅ Alpha & Beta computed!")
print(df_ab[['scheme_name','alpha','beta']].head(5).to_string(index=False))

# ══════════════════════════════════════════════════════
# TASK 6: Maximum Drawdown
# ══════════════════════════════════════════════════════
print("\n📊 Task 6: Computing Maximum Drawdown...")

dd_rows = []
for code, grp in df_nav.groupby('amfi_code'):
    grp = grp.sort_values('date')
    rolling_max = grp['nav'].cummax()
    drawdown = (grp['nav'] / rolling_max) - 1
    max_dd = drawdown.min()
    dd_rows.append({'amfi_code': code, 'max_drawdown_pct': round(max_dd * 100, 2)})

df_dd = pd.DataFrame(dd_rows)
df_dd = df_dd.merge(df_fund[['amfi_code','scheme_name']], on='amfi_code')
df_dd = df_dd.sort_values('max_drawdown_pct')
df_dd.to_csv("data/processed/max_drawdown.csv", index=False)
print("✅ Maximum Drawdown computed!")
print(f"   Worst drawdown: {df_dd.iloc[0]['scheme_name']} — {df_dd.iloc[0]['max_drawdown_pct']}%")

# ══════════════════════════════════════════════════════
# TASK 7: Fund Scorecard
# ══════════════════════════════════════════════════════
print("\n📊 Task 7: Building Fund Scorecard...")

# Merge all metrics
df_score = df_cagr[['amfi_code','cagr_3yr']].copy()
df_score = df_score.merge(df_sharpe[['amfi_code','sharpe_ratio']], on='amfi_code')
df_score = df_score.merge(df_ab[['amfi_code','alpha']], on='amfi_code')
df_score = df_score.merge(df_dd[['amfi_code','max_drawdown_pct']], on='amfi_code')
df_score = df_score.merge(df_fund[['amfi_code','scheme_name','expense_ratio_pct']], on='amfi_code')

# Rank each metric (higher rank = better)
df_score['rank_return']   = df_score['cagr_3yr'].rank(ascending=True)
df_score['rank_sharpe']   = df_score['sharpe_ratio'].rank(ascending=True)
df_score['rank_alpha']    = df_score['alpha'].rank(ascending=True)
df_score['rank_expense']  = df_score['expense_ratio_pct'].rank(ascending=False)
df_score['rank_drawdown'] = df_score['max_drawdown_pct'].rank(ascending=False)

# Composite score
n = len(df_score)
df_score['composite_score'] = (
    0.30 * df_score['rank_return'] +
    0.25 * df_score['rank_sharpe'] +
    0.20 * df_score['rank_alpha'] +
    0.15 * df_score['rank_expense'] +
    0.10 * df_score['rank_drawdown']
) / n * 100

df_score = df_score.sort_values('composite_score', ascending=False)
df_score.to_csv("data/processed/fund_scorecard.csv", index=False)
print("✅ Fund Scorecard built!")
print("\nTop 5 Funds by Composite Score:")
print(df_score[['scheme_name','composite_score','cagr_3yr','sharpe_ratio']].head(5).to_string(index=False))

# ══════════════════════════════════════════════════════
# TASK 8: Benchmark Comparison Chart
# ══════════════════════════════════════════════════════
print("\n📊 Task 8: Creating Benchmark Comparison Chart...")

# Top 5 funds by composite score
top5_codes = df_score.head(5)['amfi_code'].tolist()
top5_names = df_score.head(5)['scheme_name'].str.split('-').str[0].str.strip().tolist()

# Nifty 50 benchmark
nifty50 = df_bench[df_bench['index_name']=='NIFTY50'].copy()
nifty50 = nifty50.sort_values('date')

# Normalise to 100 at start
fig, ax = plt.subplots(figsize=(14, 6))

for code, name in zip(top5_codes, top5_names):
    grp = df_nav[df_nav['amfi_code']==code].sort_values('date')
    grp = grp[grp['date'] >= '2022-01-01']
    normalised = grp['nav'] / grp['nav'].iloc[0] * 100
    ax.plot(grp['date'], normalised, linewidth=1.5, label=name)

# Plot Nifty 50
n50 = nifty50[nifty50['date'] >= '2022-01-01']
n50_norm = n50['close_value'] / n50['close_value'].iloc[0] * 100
ax.plot(n50['date'], n50_norm, 'k--', linewidth=2, label='Nifty 50 (Benchmark)')

ax.set_title('Top 5 Funds vs Nifty 50 Benchmark (2022–2026)',
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Date', fontsize=11)
ax.set_ylabel('Normalised Value (Base=100)', fontsize=11)
ax.legend(fontsize=8)
ax.axhline(y=100, color='gray', linestyle=':', alpha=0.5)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("reports/charts/benchmark_chart.png", dpi=150)
plt.close()
print("✅ Benchmark chart saved!")

print("\n" + "="*55)
print("🎉 ALL DAY 4 TASKS COMPLETE!")
print("="*55)
print("\nFiles saved:")
print("  ✅ data/processed/returns_computed.csv")
print("  ✅ data/processed/cagr_report.csv")
print("  ✅ data/processed/sharpe_values.csv")
print("  ✅ data/processed/sortino_values.csv")
print("  ✅ data/processed/alpha_beta.csv")
print("  ✅ data/processed/max_drawdown.csv")
print("  ✅ data/processed/fund_scorecard.csv")
print("  ✅ reports/charts/benchmark_chart.png")