import pandas as pd
df = pd.read_csv("../expense.csv")
df["date"] = pd.to_datetime(df["date"])

df = df[(df["date"] >= "2025-09-01") & (df["date"] <= "2025-11-30")]

pivot = df.pivot_table(
    index="date",
    columns="category",
    values="amount",
    aggfunc="sum",
    fill_value=0
).sort_index()

pivot["total"] = pivot.sum(axis=1)

cols = ["drink","food","other","transport","utility","total"]

for c in cols:
    pivot[f"prev_{c}"] = pivot[c].shift(1)

pivot = pivot.dropna()

print("===== HEAD =====")
print(pivot.head())

print("===== ROWS =====")
print(len(pivot))