# item、count、price、合計、総売り上げ、平均priceをエクセルに出力する
import pandas as pd
import math
import tkinter
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt

csv = pd.read_csv("data.csv")
excel = pd.read_excel("data.xlsx")

csv["total"] = csv["count"] * csv["price"]

total_sales = csv["total"].sum()

total_row = pd.DataFrame({
    "item" : ["total_sales"],
    "count" : [""],
    "price" : [""],
    "total" : [total_sales]
})

average = math.floor(csv["price"].sum() / len(csv["price"]))

total_average =  pd.DataFrame({
    "item" : ["average_price"],
    "count" : [""],
    "price" : [""],
    "total" : [average]
})

csv = pd.concat([csv, total_row, total_average])
csv = csv.reset_index()

# csv.to_excel("csv.xlsx", index=False)

plt.bar(csv["item"],csv["total"])
plt.ylabel("total_price")
plt.xlabel("items")
for i in range(len(csv["total"])):
    plt.text(i, csv["total"][i], csv["total"][i])
    
plt.savefig("csv.png")
print("csv.pngとして出力成功")