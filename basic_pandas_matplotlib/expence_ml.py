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
df_exp = pd.read_csv("expense.csv")

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

# print(pivot)
# X, y

X = pivot[["drink", "food", "other", "transport", "utility"]]
y = pivot["total"]

# テストデータ作成
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# モデルの作成
model = LinearRegression()
model.fit(X_train, y_train)

# X_train, X_test, y_train, y_testになにが入っているか確認
# add_bar_print("X_train", X_train)

# 予測データの作成
y_pred = model.predict(X_test)
print("R2: ", r2_score(y_test, y_pred))
print("coef: ", model.coef_)
print("intercept:", model.intercept_)
add_bar_print("X_test", X_test)
add_bar_print("y_test", y_test)
add_bar_print("y_pred", y_pred)
