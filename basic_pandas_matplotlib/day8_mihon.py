import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# 1. データ読み込み
df = pd.read_csv("data.csv")

# 数値をちゃんと数値にしておく（保険）
df["count"] = pd.to_numeric(df["count"], errors="coerce")
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# 2. 集計列を追加
df["total"] = df["count"] * df["price"]

# 3. サマリー行を作成
total_sales = df["total"].sum()
average_price = df["price"].mean()

summary_rows = pd.DataFrame([
    {"item": "total_sales", "count": None, "price": None, "total": total_sales},
    {"item": "average_price", "count": None, "price": None, "total": round(average_price)},
])

# 分析用と保存用を分ける
df_out = pd.concat([df, summary_rows], ignore_index=True)

# 4. グラフ用のデータ（サマリー行は除外）
plot_df = df[["item", "total"]].copy()

# 5. グラフを1枚に並べる
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# --- 左：棒グラフ ---
axes[0].bar(plot_df["item"], plot_df["total"])
axes[0].set_title("Sales by item")
axes[0].set_xlabel("item")
axes[0].set_ylabel("total")

# 値を表示
for i, v in enumerate(plot_df["total"]):
    axes[0].text(i, v, f"{int(v)}", ha="center", va="bottom")

# --- 右：円グラフ ---
axes[1].pie(
    plot_df["total"],
    labels=plot_df["item"],
    autopct="%.1f%%",
    startangle=90
)
axes[1].set_title("Sales share")

plt.tight_layout()

# 6. 画像として保存
today = date.today().isoformat()
plt.savefig(f"report_{today}.png", dpi=150)
print(f"✅ report_{today}.png を出力しました")

# 7. Excelに保存（任意）
df_out.to_excel(f"report_{today}.xlsx", index=False)
print(f"✅ report_{today}.xlsx を出力しました")
