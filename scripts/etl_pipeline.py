import pandas as pd
import os

# Path to your raw data folder
data_path = "data/raw"

# Get list of all CSV files in the folder
csv_files = [f for f in os.listdir(data_path) if f.endswith(".csv")]

print(f"Total CSV files found: {len(csv_files)}")
print("Files:", csv_files)

# Loop through each file and load it
for file in csv_files:
    file_path = os.path.join(data_path, file)
    
    df = pd.read_csv(file_path)
    
    print("\n" + "="*50)
    print(f"File: {file}")
    print("="*50)
    
    print(f"Shape: {df.shape}")        # rows x columns
    print(f"\nColumns: {df.columns.tolist()}")
    
    print("\nData Types:")
    print(df.dtypes)
    
    print("\nFirst 3 Rows:")
    print(df.head(3))

    # ── Task 6: Explore Fund Master ──────────────────────────
print("\n" + "="*50)
print("FUND MASTER EXPLORATION")
print("="*50)

df_master = pd.read_csv("data/raw/01_fund_master.csv")

print(f"Total Schemes: {len(df_master)}")
print(f"\nUnique Fund Houses:\n{df_master['fund_house'].unique()}")
print(f"\nCategories:\n{df_master['category'].unique()}")
print(f"\nSub-Categories:\n{df_master['sub_category'].unique()}")
print(f"\nRisk Grades:\n{df_master['risk_category'].unique()}")

# ── Task 7: Validate AMFI Codes ──────────────────────────
print("\n" + "="*50)
print("AMFI CODE VALIDATION")
print("="*50)

df_nav = pd.read_csv("data/raw/02_nav_history.csv")

master_codes = set(df_master['amfi_code'])
nav_codes = set(df_nav['amfi_code'])

missing = nav_codes - master_codes

print(f"Fund master codes : {len(master_codes)}")
print(f"NAV history codes : {len(nav_codes)}")

if missing:
    print(f"⚠️  Missing codes: {missing}")
else:
    print("✅ All codes match! Data quality OK.")

# ── Task 6: Explore Fund Master ──────────────────────────
print("\n" + "="*50)
print("FUND MASTER EXPLORATION")
print("="*50)

df_master = pd.read_csv("data/raw/01_fund_master.csv")

print(f"Total Schemes: {len(df_master)}")
print(f"\nUnique Fund Houses:")
print(df_master['fund_house'].unique())
print(f"\nCategories:")
print(df_master['category'].unique())
print(f"\nRisk Grades:")
print(df_master['risk_category'].unique())

# ── Task 7: Validate AMFI Codes ──────────────────────────
print("\n" + "="*50)
print("AMFI CODE VALIDATION")
print("="*50)

df_nav = pd.read_csv("data/raw/02_nav_history.csv")

master_codes = set(df_master['amfi_code'])
nav_codes = set(df_nav['amfi_code'])
missing = nav_codes - master_codes

print(f"Fund master codes : {len(master_codes)}")
print(f"NAV history codes : {len(nav_codes)}")

if missing:
    print(f"Missing codes: {missing}")
else:
    print("All codes match! Data quality OK.")