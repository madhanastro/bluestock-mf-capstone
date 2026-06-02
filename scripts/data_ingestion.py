import pandas as pd
import os

data_path = "data/raw"

csv_files = [f for f in os.listdir(data_path) if f.endswith(".csv")]

for file in csv_files:
    file_path = os.path.join(data_path, file)

    df = pd.read_csv(file_path)

    print("\n" + "="*50)
    print(f"File: {file}")
    print("="*50)

    print("Shape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Rows:")
    print(df.head())