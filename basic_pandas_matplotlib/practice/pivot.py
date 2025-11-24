import pandas as pd
import datetime as dt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

#テストprint用関数
def add_bar_print(str_msg, print_vari):
    print(f"=========={str_msg}==========")
    print(print_vari)

# expense.csv読込
df_exp = pd.read_csv("../expense.csv")

# 9月分のみ抽出
year_month = "2025-09"
year, month = map(int, year_month.split("-"))
df_exp["date"] = pd.to_datetime(df_exp["date"])
monthly = df_exp[(df_exp["date"].dt.year == year) & (df_exp["date"].dt.month == month)]

# pivot_tableにtotal金額まとめて出力

# 
pivot = monthly.pivot_table(
    index=monthly["date"].dt.day, # index、大枠、
    columns="category", # カテゴリー
    values="amount", #　計算したい値
    aggfunc="sum", # どう計算するか
    fill_value=0 # NaNの場合は0に変換
)

# 列同士をsum
pivot["total"] = pivot.sum(axis=1)

# prev(前の)値を入れるための入れ物作成
for col in ["drink", "food", "other", "transport", "utility", "total"]:
    pivot[f"prev_{col}"] = pivot[f"{col}"].shift(1)

pivot = pivot.dropna() # NaNが入ってる列を削除

# X,y
X = pivot[["prev_drink", "prev_food", "prev_other", "prev_transport", "prev_utility", "prev_total"]]
y = pivot["total"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# print("R2:", r2_score(y_test, y_pred))
# print("coef: ", model.coef_)
# print("intercept: ", model.intercept_)
# print("Y_test: ", y_test)
# print("y_pred: ", y_pred)
print(pivot.head())
print("===== HEAD =====")
print(pivot.head())

print("===== COLUMNS =====")
print(list(pivot.columns))

print("===== ROW COUNT =====")
print(len(pivot))