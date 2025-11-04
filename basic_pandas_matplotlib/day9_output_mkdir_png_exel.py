import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import os

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
today = dt.date.today().strftime("%Y_%m_%d")
folder = f"python_report_{today}"
os.makedirs(folder, exist_ok=True)

data = pd.read_csv("data.csv")

data["total"] = (data["price"] * data["count"]).round
sorted_total_price_data = data.sort_values("total",ignore_index=True)
sorted_total_price = sorted_total_price_data["total"]
labels = sorted_total_price_data["item"]
total_sales = round(data["total"].sum())
average_price = round(data["price"].mean())
summary_rows = pd.DataFrame([{
    "item" : "total_sales",
    "count" : None,
    "price" : None,
    "total" : total_sales
},
{
    "item" : "average_price",
    "count" : None,
    "price" : None,
    "total" : average_price
}])
table_out = pd.concat([data, summary_rows])

axes[0].pie(
    x = sorted_total_price,
    labels = labels,
    autopct="%.1f%%",
    startangle=90,
    pctdistance=0.8,
    labeldistance=1.1
    )

axes[0].set_title("sales_share")


bars = axes[1].bar(
        labels,
        sorted_total_price,
        width=0.5,
        color = "blue"
    )

axes[1].set_xlabel("item")
axes[1].set_ylabel("price(JPY)")
axes[1].set_title("total_price")

for bar in bars:
    x = bar.get_x() + bar.get_width()/2
    y =bar.get_height()
    axes[1].text(
        x,
        y + 50,
        int(y),
        ha="center",
        va="bottom"
        )
plt.savefig(f"{folder}/{folder}.png")
table_out.to_excel(f"{folder}/{folder}.xlsx", index=False)
print("フォルダ、PNG、エクセルへ出力完了")