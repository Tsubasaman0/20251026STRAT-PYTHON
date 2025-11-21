import datetime as dt
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

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

# print("\n=== Category Summary ===")
# print(category_sum)
# print("\n=== Payment Summary ===")
# print(payment_sum)

daily_sum = monthly.groupby(monthly["date"].dt.day)["amount"].sum().sort_index()
daily_df = daily_sum.reset_index()
daily_df.columns = ["day", "amount"]

# print("\n=== Daily Summary ===")
# print(daily_sum)

# グラフの作成

# 保存先フォルダの作成
out_dir = Path("charts") / year_month
out_dir.mkdir(parents=True, exist_ok=True)

# categoryごと支出金額
plt.figure(facecolor="w")
plt.bar(category_sum["category"], category_sum["amount"])
plt.title("category_summary")
plt.xlabel("category")
plt.xticks(rotation=45)
plt.ylabel("amount")
plt.tight_layout()
plt.savefig(out_dir / "category.png")
#plt.show()

# 日別の支出額
plt.figure(facecolor="w")
plt.plot(daily_df["day"], daily_df["amount"], marker="o")
plt.title("daily_summary")
plt.xlabel("day")
plt.ylabel("amount")
plt.xticks(daily_df["day"])
plt.tight_layout()
plt.savefig(out_dir / "daily.png")
#plt.show()

pivot = monthly.pivot_table(
    index=monthly["date"].dt.day,
    columns="category",
    values="amount",
    aggfunc="sum",
    fill_value=0    
)

# print(pivot)

# interceptをグラフで理解する
model = LinearRegression()
a = model.coef_[0]
b = model.intercept_

x_line = np.linspace(0, 60, 100)
y_line = a * x_line + b

plt.scatter(df["ad_cost"], df["sales"], color="blue")
plt.plot(x_line, y_line, color="red")
plt.show()