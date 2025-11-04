# 商品、数量、単価、合計、総売り上げ、平均単価をエクセルに出力する
import pandas as pd
import math

csv = pd.read_csv("data.csv")
excel = pd.read_excel("data.xlsx")

csv["合計"] = csv["数量"] * csv["単価"]

total_sales = csv["合計"].sum()

total_row = pd.DataFrame({
    "商品" : ["総売り上げ"],
    "数量" : [""],
    "単価" : [""],
    "合計" : [total_sales]
})

average = math.floor(csv["単価"].sum() / len(csv["単価"]))

total_average =  pd.DataFrame({
    "商品" : ["平均単価"],
    "数量" : [""],
    "単価" : [""],
    "合計" : [average]
})

csv = pd.concat([csv, total_row, total_average])

csv.to_excel("csv.xlsx", index=False)