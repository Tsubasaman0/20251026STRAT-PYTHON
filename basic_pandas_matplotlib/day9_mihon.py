import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# === 1. 日付・フォルダ設定 ===
today = datetime.today().strftime("%Y-%m-%d")
folder = f"report_{today}"
os.makedirs(folder, exist_ok=True)  # 日付フォルダを自動作成

# === 2. データ読み込み ===
df = pd.read_csv("data.csv")
df["count"] = pd.to_numeric(df["count"], errors="coerce")
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["total"] = df["count"] * df["price"]

# === 3. 集計 ===
total_sales = df["total"].sum()
average_price = df["price"].mean()

summary_rows = pd.DataFrame([
    {"item": "total_sales", "count": None, "price": None, "total": total_sales},
    {"item": "average_price", "count": None, "price": None, "total": round(average_price)},
])

df_out = pd.concat([df, summary_rows], ignore_index=True)

# === 4. グラフ作成 ===
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# 棒グラフ
bars = axes[0].bar(df["item"], df["total"], color="skyblue")
axes[0].set_title("Total Sales by Item")
axes[0].set_xlabel("Item")
axes[0].set_ylabel("Sales (JPY)")
for bar in bars:
    x = bar.get_x() + bar.get_width() / 2
    y = bar.get_height()
    axes[0].text(x, y + y * 0.05, f"{int(y)}", ha="center", va="bottom")

# 円グラフ
axes[1].pie(
    df["total"], 
    labels=df["item"], 
    autopct="%.1f%%", 
    startangle=90,
    pctdistance=0.8, 
    labeldistance=1.1
)
axes[1].set_title("Sales Share")

plt.tight_layout()

# === 5. ファイル出力 ===
img_path = os.path.join(folder, f"report_{today}.png")
excel_path = os.path.join(folder, f"report_{today}.xlsx")

plt.savefig(img_path, dpi=150)
df_out.to_excel(excel_path, index=False)

print(f"✅ レポート作成完了！\n📊 画像: {img_path}\n📗 Excel: {excel_path}")
