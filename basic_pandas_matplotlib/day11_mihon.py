import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os

# === 1. データフォルダの指定 ===
data_folder = "data_files"
output_root = "monthly_reports"
os.makedirs(output_root, exist_ok=True)

# === 2. CSVファイルをすべて取得 ===
csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

if not csv_files:
    print("⚠️ CSVファイルが見つかりません。data_files フォルダを確認してください。")
else:
    print(f"📁 {len(csv_files)}件のCSVファイルを検出しました。")

# === 3. 各CSVごとに処理 ===
for csv_file in csv_files:
    # ファイル名から年月を抽出
    file_path = os.path.join(data_folder, csv_file)
    date_label = csv_file.replace("data_", "").replace(".csv", "")
    
    # 出力用フォルダ
    today = dt.date.today().strftime("%Y_%m_%d")
    folder = os.path.join(output_root, f"report_{date_label}_{today}")
    os.makedirs(folder, exist_ok=True)
    
    # === データ読み込み ===
    data = pd.read_csv(file_path)
    data["total"] = (data["price"] * data["count"]).astype(int)
    
    # === 集計 ===
    total_sales = data["total"].sum()
    average_price = round(data["price"].mean())
    top_item = data.loc[data["total"].idxmax(), "item"]
    top_value = data["total"].max()
    top_share = round(top_value / total_sales * 100, 1)
    
    # === AIコメント生成 ===
    ai_comment = (
        f"【{date_label} 月レポート】\n"
        f"総売上は {total_sales:,} 円、平均単価は {average_price:,} 円です。\n"
        f"最も売れた商品は「{top_item}」で、全体の {top_share}% を占めています。\n"
        f"上位商品の売上が全体の多くを構成しており、効率的な在庫管理が重要です。"
    )
    
    # === グラフ作成 ===
    sorted_data = data.sort_values("total", ascending=False)
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
    bars = axes[1].bar(sorted_data["item"], sorted_data["total"], color="cornflowerblue")
    axes[1].set_title("Total Sales by Item")
    axes[1].set_xlabel("Item")
    axes[1].set_ylabel("Sales (JPY)")
    for bar in bars:
        x = bar.get_x() + bar.get_width()/2
        y = bar.get_height()
        axes[1].text(x, y + y * 0.02, int(y), ha="center", va="bottom", fontsize=9)
    
    plt.tight_layout()
    
    # === 保存 ===
    img_path = os.path.join(folder, f"report_{date_label}.png")
    excel_path = os.path.join(folder, f"report_{date_label}.xlsx")
    txt_path = os.path.join(folder, f"comment_{date_label}.txt")
    
    plt.savefig(img_path, dpi=150)
    data.to_excel(excel_path, index=False)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(ai_comment)
    
    plt.close(fig)
    print(f"✅ {date_label} のレポート出力完了 → {folder}")
