import datetime as dt
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# csvの読み込み処理
csv_path = Path("expense.csv")
df = pd.read_csv(csv_path)
df["date"] = pd.to_datetime(df["date"])

# 抽出したい年月（YYYY-MM）
year_month = "2025-09"
year,month = map(int, year_month.split("-"))

# 年月のフィルタリング
monthly = df[(df["date"].dt.year == year) & (df["date"].dt.month == month)]

# 集計したいデータを引数に入れるとその値を返してくれる関数
def categorize_sum(dataframe, category_str):
    return dataframe.groupby(category_str)["amount"].sum().sort_values(ascending=False)

category_sum = categorize_sum(monthly, "category").reset_index()
payment_sum = categorize_sum(monthly, "payment").reset_index()

category_sum.columns = ["category", "amount"]
payment_sum.columns = ["payment", "amount"]

print("\n=== Category Summary ===")
print(category_sum)
print("\n=== Payment Summary ===")
print(payment_sum)

daily_sum = monthly.groupby(monthly["date"].dt.day)["amount"].sum().sort_values(ascending=False).reset_index()

daily_sum.columns = ["Date", "amount"]

print("\n=== Daily Summary ===")
print(daily_sum)

# グラフの作成
# categoryごと支出金額
category_sum.plot(kind="bar")
plt.title("category_summary")
plt.xlabel("category")
plt.ylabel("amount")
plt.show()

# 日別の支出額
daily_sum.sort_index().plot(kind="line")
plt.title("daily_summary")
plt.xlabel("date")
plt.ylabel("amout")
plt.show()