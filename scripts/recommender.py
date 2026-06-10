
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
