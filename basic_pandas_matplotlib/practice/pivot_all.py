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

# --- prev特徴量を追加 -------------------------

cols = ["drink","food","other","transport","utility","total"]

for c in cols:
    pivot[f"prev_{c}"] = pivot[c].shift(1)

pivot = pivot.dropna()  # 最初の1行だけ削除

# --- X, y 作成 -------------------------------

X = pivot[[
    "prev_drink",
    "prev_food",
    "prev_other",
    "prev_transport",
    "prev_utility",
    "prev_total"
]]

y = pivot["total"]

# --- 時系列split（8:2） -----------------------

split_idx = int(len(pivot) * 0.8)

X_train = X.iloc[:split_idx]
X_test  = X.iloc[split_idx:]
y_train = y.iloc[:split_idx]
y_test  = y.iloc[split_idx:]

# --- モデル ----------------------------------

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("R2:", r2_score(y_test, y_pred))
print("coef:", model.coef_)
print("intercept:", model.intercept_)
print("y_test:", list(y_test.values))
print("y_pred:", list(y_pred))

# print("===== HEAD =====")
# print(pivot.head())

# print("===== TAIL =====")
# print(pivot.tail())

# print("===== ROW COUNT =====")
# print(len(pivot))