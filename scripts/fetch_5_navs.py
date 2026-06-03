import requests
import pandas as pd

schemes = {
    "sbi_bluechip": 119551,
    "icici_bluechip": 120503,
    "nippon_largecap": 118632,
    "axis_bluechip": 119092,
    "kotak_bluechip": 120841
}

for name, code in schemes.items():
    url = f"https://api.mfapi.in/mf/{code}"

    response = requests.get(url)
    data = response.json()

    df = pd.DataFrame(data["data"])

    file_name = f"data/raw/{name}_nav.csv"
    df.to_csv(file_name, index=False)

    print(f"Saved: {file_name}")
    