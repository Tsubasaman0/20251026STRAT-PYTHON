import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import os

# === 1. 初期設定 ===
today = dt.date.today().strftime("%Y_%m_%d")
folder = f"python_ai_report_{today}"
os.makedirs(folder, exist_ok=True)
print("📁 フォルダ作成完了:", folder)

# === 2. データ読み込み ===
data = pd.read_csv("data.csv")
data["total"] = data["price"] * data["count"]
sorted_data = data.sort_values("total", ascending=False, ignore_index=True)

# === 3. 集計 ===
total_sales = round(sorted_data["total"].sum())
average_price = round(sorted_data["price"].mean())
top_item = sorted_data.iloc[0]["item"]
top_share = round(sorted_data.iloc[0]["total"] / total_sales * 100, 1)

# === 4. 自動コメント生成 ===
comment = (
    f"【自動レポート】\n"
    f"総売上は {total_sales:,} 円、平均単価は {average_price:,} 円です。\n"
    f"最も売れた商品は「{top_item}」で、全体の {top_share}% を占めています。\n"
    f"全体的に、上位商品の売上が構成比の大部分を占める傾向があります。"
)
print(comment)

# === 5. グラフ ===
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# 円グラフ
axes[0].pie(
    sorted_data["total"],
    labels=sorted_data["item"],
    autopct="%.1f%%",
    startangle=90,
    pctdistance=0.8,
    labeldistance=1.1
)
axes[0].set_title("Sales Share")

# 棒グラフ
bars = axes[1].bar(
    sorted_data["item"],
    sorted_data["total"],
    color="cornflowerblue"
)
axes[1].set_title("Total Sales by Item")
axes[1].set_xlabel("Item")
axes[1].set_ylabel("Sales (JPY)")
for bar in bars:
    x = bar.get_x() + bar.get_width() / 2
    y = bar.get_height()
    axes[1].text(x, y + 50, int(y), ha="center", va="bottom")

plt.tight_layout()

# === 6. 保存 ===
img_path = f"{folder}/report_{today}.png"
excel_path = f"{folder}/report_{today}.xlsx"
txt_path = f"{folder}/comment_{today}.txt"

plt.savefig(img_path, dpi=150)
data.to_excel(excel_path, index=False)
with open(txt_path, "w", encoding="utf-8") as f:
    f.write(comment)

print(f"\n✅ レポート出力完了！\n📊 画像: {img_path}\n📗 Excel: {excel_path}\n📝 コメント: {txt_path}")
