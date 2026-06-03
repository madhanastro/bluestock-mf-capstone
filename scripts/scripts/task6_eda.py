import pandas as pd

df = pd.read_csv("data/raw/01_fund_master.csv")

print("Unique Fund Houses")
print(df["fund_house"].unique())

print("\nTotal Fund Houses:", df["fund_house"].nunique())

print("\nUnique Categories")
print(df["category"].unique())

print("\nTotal Categories:", df["category"].nunique())

print("\nUnique Sub Categories")
print(df["sub_category"].unique())

print("\nTotal Sub Categories:", df["sub_category"].nunique())

print("\nUnique Risk Categories")
print(df["risk_category"].unique())

print("\nTotal Risk Categories:", df["risk_category"].nunique())