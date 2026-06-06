import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ── Setup ─────────────────────────────────────────────
CHARTS_DIR = "reports/charts"
plt.style.use('seaborn-v0_8')

print("="*55)
print("DAY 3: EXPLORATORY DATA ANALYSIS")
print("="*55)

# Load all cleaned datasets
df_nav     = pd.read_csv("data/processed/clean_nav.csv", parse_dates=['date'])
df_fund    = pd.read_csv("data/processed/clean_fund_master.csv")
df_aum     = pd.read_csv("data/processed/clean_aum.csv", parse_dates=['date'])
df_sip     = pd.read_csv("data/processed/clean_sip.csv", parse_dates=['month'])
df_cat     = pd.read_csv("data/processed/clean_category_inflows.csv", parse_dates=['month'])
df_folio   = pd.read_csv("data/processed/clean_folio_count.csv", parse_dates=['month'])
df_tx      = pd.read_csv("data/processed/clean_transactions.csv")
df_hold    = pd.read_csv("data/processed/clean_portfolio_holdings.csv")

print("✅ All datasets loaded!")

# ══════════════════════════════════════════════════════
# CHART 1: NAV Trend Lines for 6 selected funds
# ══════════════════════════════════════════════════════
print("\n📊 Creating Chart 1: NAV Trend Lines...")

# Pick 6 funds from different categories
selected = [119551, 119598, 119571, 119556, 119552, 119563]
df_sel = df_nav[df_nav['amfi_code'].isin(selected)].copy()
df_sel = df_sel.merge(df_fund[['amfi_code','scheme_name']], on='amfi_code')

# Shorten name for legend
df_sel['short_name'] = df_sel['scheme_name'].str.split('-').str[0].str.strip()

fig, ax = plt.subplots(figsize=(14, 6))
for code, grp in df_sel.groupby('amfi_code'):
    name = grp['short_name'].iloc[0]
    ax.plot(grp['date'], grp['nav'], linewidth=1.5, label=name)

ax.set_title('NAV Trend Lines — Selected Funds (2022–2026)', 
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Date', fontsize=11)
ax.set_ylabel('NAV (₹)', fontsize=11)
ax.legend(fontsize=8, loc='upper left')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/chart1_nav_trends.png", dpi=150)
plt.close()
print("✅ Chart 1 saved!")

# ══════════════════════════════════════════════════════
# CHART 2: AUM Growth by Fund House
# ══════════════════════════════════════════════════════
print("📊 Creating Chart 2: AUM Growth by Fund House...")

df_aum['year'] = df_aum['date'].dt.year
df_aum_yr = df_aum.groupby(['year','fund_house'])['aum_lakh_crore'].mean().reset_index()

fig, ax = plt.subplots(figsize=(14, 6))
sns.barplot(data=df_aum_yr, x='fund_house', y='aum_lakh_crore', 
            hue='year', ax=ax, palette='Blues')
ax.set_title('AUM Growth by Fund House (2022–2025)', 
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Fund House', fontsize=11)
ax.set_ylabel('AUM (Lakh Crore ₹)', fontsize=11)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/chart2_aum_growth.png", dpi=150)
plt.close()
print("✅ Chart 2 saved!")

# ══════════════════════════════════════════════════════
# CHART 3: SIP Inflow Time Series
# ══════════════════════════════════════════════════════
print("📊 Creating Chart 3: SIP Inflow Trend...")

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(df_sip['month'], df_sip['sip_inflow_crore'], 
        color='#2196F3', linewidth=2, marker='o', markersize=3)
ax.fill_between(df_sip['month'], df_sip['sip_inflow_crore'], 
                alpha=0.15, color='#2196F3')

# Mark the ATH milestone
ath_row = df_sip.loc[df_sip['sip_inflow_crore'].idxmax()]
ax.annotate(f"ATH ₹{int(ath_row['sip_inflow_crore']):,} Cr",
            xy=(ath_row['month'], ath_row['sip_inflow_crore']),
            xytext=(30, -30), textcoords='offset points',
            arrowprops=dict(arrowstyle='->', color='red'),
            fontsize=9, color='red')

ax.set_title('Monthly SIP Inflows (Jan 2022 – Dec 2025)', 
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Month', fontsize=11)
ax.set_ylabel('SIP Inflow (₹ Crore)', fontsize=11)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/chart3_sip_inflow.png", dpi=150)
plt.close()
print("✅ Chart 3 saved!")

# ══════════════════════════════════════════════════════
# CHART 4: Category Inflow Heatmap
# ══════════════════════════════════════════════════════
print("📊 Creating Chart 4: Category Inflow Heatmap...")

df_cat['month_str'] = df_cat['month'].dt.strftime('%b %Y')
pivot = df_cat.pivot_table(index='category', columns='month_str', 
                            values='net_inflow_crore', aggfunc='sum')

fig, ax = plt.subplots(figsize=(14, 7))
sns.heatmap(pivot, cmap='RdYlGn', center=0, ax=ax,
            linewidths=0.3, annot=False, fmt='.0f',
            cbar_kws={'label': 'Net Inflow (₹ Crore)'})
ax.set_title('Category-wise Net Inflows Heatmap (FY 2024–25)', 
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Month', fontsize=11)
ax.set_ylabel('Category', fontsize=11)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/chart4_category_heatmap.png", dpi=150)
plt.close()
print("✅ Chart 4 saved!")

# ══════════════════════════════════════════════════════
# CHART 5: Investor Age Demographics
# ══════════════════════════════════════════════════════
print("📊 Creating Chart 5: Investor Demographics...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# Pie chart - age distribution
age_counts = df_tx['age_group'].value_counts()
colors = ['#FF6B6B','#4ECDC4','#45B7D1','#96CEB4','#FFEAA7']
ax1.pie(age_counts.values, labels=age_counts.index, 
        autopct='%1.1f%%', colors=colors, startangle=90)
ax1.set_title('Investor Age Distribution', fontsize=12, fontweight='bold')

# Box plot - SIP amount by age group
sip_only = df_tx[df_tx['transaction_type'] == 'SIP']
age_order = ['18-25','26-35','36-45','46-55','56+']
sns.boxplot(data=sip_only, x='age_group', y='amount_inr', 
            order=age_order, ax=ax2, palette='pastel')
ax2.set_title('SIP Amount by Age Group', fontsize=12, fontweight='bold')
ax2.set_xlabel('Age Group', fontsize=10)
ax2.set_ylabel('SIP Amount (₹)', fontsize=10)

plt.suptitle('Investor Demographics Analysis', 
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/chart5_demographics.png", dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart 5 saved!")

# ══════════════════════════════════════════════════════
# CHART 6: Geographic Distribution
# ══════════════════════════════════════════════════════
print("📊 Creating Chart 6: Geographic Distribution...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Bar chart - SIP by state
state_sip = df_tx[df_tx['transaction_type']=='SIP'].groupby('state')['amount_inr'].sum().sort_values()
state_sip.plot(kind='barh', ax=ax1, color='#3498db')
ax1.set_title('Total SIP Amount by State', fontsize=12, fontweight='bold')
ax1.set_xlabel('Total Amount (₹)', fontsize=10)

# Pie - T30 vs B30
tier_counts = df_tx['city_tier'].value_counts()
ax2.pie(tier_counts.values, labels=tier_counts.index,
        autopct='%1.1f%%', colors=['#2ecc71','#e74c3c'], startangle=90)
ax2.set_title('T30 vs B30 City Distribution', fontsize=12, fontweight='bold')

plt.suptitle('Geographic Distribution of Investments',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/chart6_geographic.png", dpi=150)
plt.close()
print("✅ Chart 6 saved!")

# ══════════════════════════════════════════════════════
# CHART 7: Folio Count Growth
# ══════════════════════════════════════════════════════
print("📊 Creating Chart 7: Folio Count Growth...")

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df_folio['month'], df_folio['total_folios_crore'],
        color='#9b59b6', linewidth=2.5, marker='o', markersize=5)
ax.fill_between(df_folio['month'], df_folio['total_folios_crore'],
                alpha=0.15, color='#9b59b6')
ax.set_title('Industry Folio Count Growth (2022–2025)',
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Month', fontsize=11)
ax.set_ylabel('Total Folios (Crore)', fontsize=11)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/chart7_folio_growth.png", dpi=150)
plt.close()
print("✅ Chart 7 saved!")

# ══════════════════════════════════════════════════════
# CHART 8: Correlation Matrix
# ══════════════════════════════════════════════════════
print("📊 Creating Chart 8: Correlation Matrix...")

# Pick 10 funds and compute daily returns
top10 = df_nav['amfi_code'].unique()[:10]
df_corr = df_nav[df_nav['amfi_code'].isin(top10)].copy()
df_corr['return'] = df_corr.groupby('amfi_code')['nav'].pct_change()
pivot_corr = df_corr.pivot_table(index='date', columns='amfi_code', values='return')
pivot_corr.columns = [str(c) for c in pivot_corr.columns]
corr_matrix = pivot_corr.corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
            center=0, ax=ax, square=True, linewidths=0.3)
ax.set_title('NAV Return Correlation Matrix (10 Funds)',
             fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/chart8_correlation.png", dpi=150)
plt.close()
print("✅ Chart 8 saved!")

# ══════════════════════════════════════════════════════
# CHART 9: Sector Allocation Donut
# ══════════════════════════════════════════════════════
print("📊 Creating Chart 9: Sector Allocation...")

sector_wt = df_hold.groupby('sector')['weight_pct'].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 8))
colors = plt.cm.Set3(range(len(sector_wt)))
wedges, texts, autotexts = ax.pie(
    sector_wt.values, labels=sector_wt.index,
    autopct='%1.1f%%', colors=colors,
    wedgeprops=dict(width=0.5), startangle=90)
ax.set_title('Sector Allocation Across Equity Portfolios',
             fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/chart9_sector_allocation.png", dpi=150)
plt.close()
print("✅ Chart 9 saved!")

# ══════════════════════════════════════════════════════
# CHART 10: Payment Mode Distribution
# ══════════════════════════════════════════════════════
print("📊 Creating Chart 10: Payment Mode...")

fig, ax = plt.subplots(figsize=(8, 5))
pay_counts = df_tx['payment_mode'].value_counts()
colors = ['#3498db','#2ecc71','#e74c3c','#f39c12']
bars = ax.bar(pay_counts.index, pay_counts.values, color=colors, edgecolor='white')
for bar, val in zip(bars, pay_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
            f'{val:,}', ha='center', va='bottom', fontsize=10)
ax.set_title('Transaction Count by Payment Mode',
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Payment Mode', fontsize=11)
ax.set_ylabel('Number of Transactions', fontsize=11)
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/chart10_payment_mode.png", dpi=150)
plt.close()
print("✅ Chart 10 saved!")

print("\n" + "="*55)
print("🎉 ALL 10 CHARTS SAVED to reports/charts/")
print("="*55)


# ══════════════════════════════════════════════════════
# CHART 11: Gender Distribution
# ══════════════════════════════════════════════════════
print("📊 Creating Chart 11: Gender Distribution...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

gender_counts = df_tx['gender'].value_counts()
ax1.pie(gender_counts.values, labels=gender_counts.index,
        autopct='%1.1f%%', colors=['#3498db','#e91e63'], startangle=90)
ax1.set_title('Investor Gender Distribution', fontsize=12, fontweight='bold')

gender_amt = df_tx.groupby('gender')['amount_inr'].mean()
ax2.bar(gender_amt.index, gender_amt.values, color=['#3498db','#e91e63'])
ax2.set_title('Average Investment by Gender', fontsize=12, fontweight='bold')
ax2.set_ylabel('Average Amount (₹)', fontsize=10)
for i, v in enumerate(gender_amt.values):
    ax2.text(i, v + 500, f'₹{v:,.0f}', ha='center', fontsize=10)

plt.suptitle('Gender Analysis', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/chart11_gender.png", dpi=150)
plt.close()
print("✅ Chart 11 saved!")

# ══════════════════════════════════════════════════════
# CHART 12: Monthly Transaction Volume
# ══════════════════════════════════════════════════════
print("📊 Creating Chart 12: Monthly Transaction Volume...")

df_tx['transaction_date'] = pd.to_datetime(df_tx['transaction_date'])
df_tx['month'] = df_tx['transaction_date'].dt.to_period('M')
monthly_vol = df_tx.groupby(['month','transaction_type']).size().unstack(fill_value=0)
monthly_vol.index = monthly_vol.index.astype(str)

fig, ax = plt.subplots(figsize=(14, 5))
monthly_vol.plot(kind='bar', ax=ax, stacked=True,
                 color=['#e74c3c','#2ecc71','#3498db'])
ax.set_title('Monthly Transaction Volume by Type',
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Month', fontsize=11)
ax.set_ylabel('Number of Transactions', fontsize=11)
ax.legend(title='Type')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/chart12_monthly_volume.png", dpi=150)
plt.close()
print("✅ Chart 12 saved!")

# ══════════════════════════════════════════════════════
# CHART 13: Top 10 Funds by 3 Year Return
# ══════════════════════════════════════════════════════
print("📊 Creating Chart 13: Top Performing Funds...")

df_perf2 = pd.read_csv("data/processed/clean_performance.csv")

# scheme_name already exists in performance file — no merge needed!
df_perf2['label'] = df_perf2['scheme_name'].str.split('-').str[0].str.strip()
top10 = df_perf2.nlargest(10, 'return_3yr_pct')

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(top10['label'], top10['return_3yr_pct'],
               color='#27ae60', edgecolor='white')
for bar, val in zip(bars, top10['return_3yr_pct']):
    ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}%', va='center', fontsize=9)
ax.set_title('Top 10 Funds by 3-Year CAGR Return',
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('3-Year Return (%)', fontsize=11)
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/chart13_top_funds.png", dpi=150)
plt.close()
print("✅ Chart 13 saved!")

# ══════════════════════════════════════════════════════
# CHART 14: Expense Ratio Distribution
# ══════════════════════════════════════════════════════
print("📊 Creating Chart 14: Expense Ratio Distribution...")

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(df_fund['expense_ratio_pct'], bins=15,
        color='#e67e22', edgecolor='white', alpha=0.8)
ax.axvline(df_fund['expense_ratio_pct'].mean(), color='red',
           linestyle='--', linewidth=2,
           label=f"Mean: {df_fund['expense_ratio_pct'].mean():.2f}%")
ax.set_title('Distribution of Expense Ratios Across Funds',
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Expense Ratio (%)', fontsize=11)
ax.set_ylabel('Number of Funds', fontsize=11)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/chart14_expense_ratio.png", dpi=150)
plt.close()
print("✅ Chart 14 saved!")

# ══════════════════════════════════════════════════════
# CHART 15: KYC Status + Risk Category
# ══════════════════════════════════════════════════════
print("📊 Creating Chart 15: KYC and Risk Category...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# KYC Status
kyc = df_tx['kyc_status'].value_counts()
ax1.pie(kyc.values, labels=kyc.index,
        autopct='%1.1f%%', colors=['#2ecc71','#e74c3c'], startangle=90)
ax1.set_title('KYC Status Distribution', fontsize=12, fontweight='bold')

# Risk Category
risk = df_fund['risk_category'].value_counts()
colors = ['#e74c3c','#e67e22','#f1c40f','#2ecc71','#3498db']
ax2.bar(risk.index, risk.values, color=colors, edgecolor='white')
ax2.set_title('Funds by Risk Category', fontsize=12, fontweight='bold')
ax2.set_xlabel('Risk Category', fontsize=10)
ax2.set_ylabel('Number of Funds', fontsize=10)
plt.xticks(rotation=30)

plt.suptitle('KYC Status & Risk Analysis',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/chart15_kyc_risk.png", dpi=150)
plt.close()
print("✅ Chart 15 saved!")

print("\n" + "="*55)
print("🎉 ALL 15 CHARTS COMPLETE!")
print(f"📁 Saved to: reports/charts/")
print("="*55)