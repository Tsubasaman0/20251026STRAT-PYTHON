import pandas as pd
import datetime as dt

# expense.csv読込
df_exp = pd.read_csv("../expense.csv")

# 9月分のみ抽出
year_month = "2025-09"
year, month = map(int, year_month.split("-"))
df_exp["date"] = pd.to_datetime(df_exp["date"])
monthly = df_exp[(df_exp["date"].dt.year == year) & (df_exp["date"].dt.month == month)]

# pivot_tableにtotal金額まとめて出力
pivot = monthly.pivot_table(
    index=monthly["date"].dt.day,
    columns="category",
    values="amount",
    aggfunc="sum",
    fill_value=0
)

pivot["total"] = pivot.sum(axis=1)

print(pivot)

# X, y