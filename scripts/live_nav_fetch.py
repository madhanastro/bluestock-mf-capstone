import requests
import pandas as pd

url = "https://api.mfapi.in/mf/125497"

response = requests.get(url)

data = response.json()

df = pd.DataFrame([data["data"][0]])

df.to_csv("data/raw/live_nav.csv", index=False)

print("Live NAV saved successfully!")
print(df.head())