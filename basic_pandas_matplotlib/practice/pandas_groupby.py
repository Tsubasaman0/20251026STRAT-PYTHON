import pandas as pd

df = pd.read_csv("ads_multi.csv")

result = df.groupby(["search_ad", "sns_ad"])["sales"].mean()

print(result)