import pandas as pd

# 読み込み
df = pd.read_csv("../expense.csv")
df["date"] = pd.to_datetime(df["date"])

# 対象期間
start = "2025-09-01"
end   = "2025-11-30"

df = df[(df["date"] >= start) & (df["date"] <= end)]

# pivot
pivot = df.pivot_table(
    index="date",
    columns="category",
    values="amount",
    aggfunc="sum",
    fill_value=0
).sort_index()

# total
pivot["total"] = pivot.sum(axis=1)

# --- ここからが重要 ----------------------------------------------------------------------

# 1) すべての日付を連続で作る
all_dates = pd.date_range(start=start, end=end, freq="D")

# 2) リインデックス（存在しなかった日 → 0埋め行になる）
pivot = pivot.reindex(all_dates, fill_value=0)

# 3) 名前を戻す
pivot.index.name = "date"

# ------------------------------------------------------------------------------------------

print("===== HEAD =====")
print(pivot.head())

print("===== TAIL =====")
print(pivot.tail())

print("===== ROW COUNT =====")
print(len(pivot))