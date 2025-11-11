
from pathlib import Path
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import os


# 1:準備 --ファイルやフォルダを作成するための変数やファイルの読み込み

today       = dt.date.today().strftime("%Y_%m_%d")
out_root    = Path("A_monthly_reports")
in_dir      = Path("data_files")
csv_files   = sorted(p for p in in_dir.iterdir() if p.suffix.lower() == ".csv")


# 2:トータル売り上げと平均価格、棒グラフ用データなどのデータ作成

summary_row = []

for csv_path in csv_files:
    data_label              = csv_path.stem.replace("data_", "")
    out_dir                 = out_root / f"report_{data_label}"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"WARNING 読込失敗: {csv_path.name}({e})")
        continue
    
    required_cols = {"item", "price", "count"}
    if not required_cols.issubset(df.columns):
        print(f"WARNING カラム不足: {csv_path.name} 必要： {required_cols} 実際: {set(df.columns)}")
        continue
    
    # 数値数値の安全化
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
    df["count"] = pd.to_numeric(df["count"], errors="coerce").fillna(0).astype(int)
    
    # ここまで修正済
        
        
    df["total"]           	= df["price"] * df["count"]
    total_sales			    = int(round(df["total"].sum()))
    average_price   		= int(round(df["price"].mean()) if len(df) else 0)
    top_sales_item_name		= df["item"][df["total"].idxmax()]
    top_sales_item_total    = df["total"].max()
    top_share_item_rate     = round(top_sales_item_total / total_sales * 100, 1)
    
    summary_row     	    = pd.DataFrame([{
        "item" : "total_sales",
        "count" : None,
        "price" : None,
        "total" : total_sales
    },{        
        "item" : "average_price",
        "count" : None,
        "price" : None,
        "total" : average_price}
    ])
    

    ai_comment = (
        f" {data_label} 月の総売上は {total_sales} 円、平均単価は {average_price} 円です。\n"
        f"最も売れた商品は「{top_sales_item_name}」で、全体の {top_share_item_rate}% を占めています。\n"
        f"全体的に、上位商品の売上が構成比の大部分を占める傾向があります"
        )
    # グラフの作成
    
    fig,axes       = plt.subplots(1, 2, figsize=(10, 5))
    plot_df        = df.sort_values("total",ascending=False).reset_index(drop=True)
    graph_labels   = plot_df["item"]
    graph_total    = plot_df["total"]
    # 棒グラフの作成
    bars = axes[0].bar(
        graph_labels,
        graph_total,
        color="blue"
    )
    axes[0].set_xlabel("item")
    axes[0].set_ylabel("total_sales(JPY)")
    axes[0].set_title(f"{data_label}total_sales")
    for bar in bars:
        x = bar.get_x() + bar.get_width()/2
        y = bar.get_height()
        axes[0].text(
            x,
            y,
            int(y),
            ha="center",
            va="bottom"
            
        )
    
    # 円グラフ作成
    axes[1].pie(
        graph_total
    )
    
    out_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_dir / f"report_{data_label}.png")
    plt.close(fig)
    with open(f"{out_dir}/comment_{data_label}.txt", mode="w") as f:
        f.write(ai_comment)
    print(ai_comment)