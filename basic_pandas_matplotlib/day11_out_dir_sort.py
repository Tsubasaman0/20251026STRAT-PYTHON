import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import os

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
today = dt.date.today().strftime("%Y_%m_%d")
folder = f"python_monthly_report_{today}"
os.makedirs(folder, exist_ok=True)
#os.makedirs(f"{folder}/new", exist_ok=True)

data = pd.read_csv("data.csv")

data["total"] = (data["price"] * data["count"]).astype(int)

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

top_sales_item = data["item"][data["total"].idxmax()]
top_sales_item_price = data["total"].max()
top_share_price = round(top_sales_item_price / total_sales * 100, 1)
ai_comment = f"""総売上は {total_sales} 円、平均単価は {average_price} 円です。
最も売れた商品は「{top_sales_item}」で、全体の {top_share_price}% を占めています。
全体的に、上位商品の売上が構成比の大部分を占める傾向があります。"""

table_out = pd.concat([data, summary_rows])
print(ai_comment)

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
excel_path = f"{folder}/{folder}.xlsx"

with pd.ExcelWriter(excel_path) as writer:
    data.to_excel(writer, sheet_name="data", index=False)
    table_out.to_excel(writer, sheet_name="summary", index=False)
    
with open(f"{folder}/{folder}.txt", mode="w", encoding="utf-8") as f:
    f.write(ai_comment)
    
print("フォルダ、PNG、エクセルへ出力完了")