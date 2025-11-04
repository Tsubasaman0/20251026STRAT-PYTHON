# item、count、price、合計、総売り上げ、平均priceをエクセルに出力する
import pandas as pd
import math 
import matplotlib.pyplot as plt

csv = pd.read_csv("data.csv")
excel = pd.read_excel("data.xlsx")

csv["total"] = csv["count"] * csv["price"]

total_sales = csv["total"].sum()

total_row = pd.DataFrame({
    "item" : ["total_sales"],
    "count" : [None],
    "price" : [None],
    "total" : [total_sales]
})

average = math.floor(csv["price"].mean())

total_average =  pd.DataFrame({
    "item" : ["average_price"],
    "count" : [None],
    "price" : [None],
    "total" : [average]
})

csv = pd.concat([csv, total_row, total_average], ignore_index=True)
plot_csv = csv[~csv["item"].isin(["total_sales", "average_price"])]

print(plot_csv)
print(csv)
# csv.to_excel("csv.xlsx", index=False)

plt.bar(plot_csv["item"],plot_csv["total"])
plt.ylabel("total_price")
plt.xlabel("items")
for i in range(len(plot_csv["total"])):
    plt.text(i, plot_csv["total"][i], plot_csv["total"][i])
    
plt.savefig("csv.png")
print("csv.pngとして出力成功")