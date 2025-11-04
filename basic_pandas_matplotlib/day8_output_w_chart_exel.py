import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

fig = plt.figure()

def get_today():
    return dt.date.today()


data = pd.read_csv("data.csv")

data["total"] = data["price"] * data["count"]
sorted_total_price_data = data.sort_values("total",ignore_index=True)
sorted_total_price = sorted_total_price_data["total"]
labels = sorted_total_price_data["item"]

pie_fig = fig.add_subplot(1, 2, 1)
pie_fig.pie(
    x = sorted_total_price,
    labels = labels,
    autopct="%.1f%%",
    startangle=90,
    pctdistance=0.8,
    labeldistance=1.1
    )

pie_fig.set_title("sales_share")

bar_fig = fig.add_subplot(1, 2, 2)
bars = bar_fig.bar(
        labels,
        sorted_total_price,
        width=0.5,
        color = "blue"
    )

bar_fig.set_title("total_price")

for bar in bars:
    x = bar.get_x() + bar.get_width()/2
    y =bar.get_height()
    bar_fig.text(
        x,
        y + 50,
        int(y),
        ha="center",
        va="bottom"
        )
plt.savefig(f"day8_data_{get_today()}.png")
print("png出力完了")