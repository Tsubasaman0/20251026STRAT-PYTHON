
from pathlib import Path
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import os


# 1:準備 --ファイルやフォルダを作成するための変数やファイルの読み込み

today       = dt.date.today().strftime("%Y_%m_%d")
out_root    = Path("my_monthly_reports")
in_dir      = Path("data_files")
csv_files   = sorted(p for p in in_dir.iterdir() if p.suffix.lower() == ".csv")
out_root.mkdir(parents=True, exist_ok=True)


# 2:トータル売り上げと平均価格、棒グラフ用データなどのデータ作成

summary_rows = []

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
    
    # 数値の安全化
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
    df["count"] = pd.to_numeric(df["count"], errors="coerce").fillna(0).astype(int)
    df["total"] = df["price"] * df["count"]
     
    # 合計売上と単価の加重平均金額
    total_sales			    = int(df["total"].sum())
    total_count             = int(df["count"].sum())
    avg_price_weighted      = int(round(total_sales / total_count if total_count > 0 else 0))
    
    # csv用に商品構成を入力
    df["share_percent"] = (df["total"] / total_sales * 100).round(2) if total_sales > 0 else 0
    
    if len(df) and total_sales > 0:
        top_idx                 = df["total"].idxmax()
        top_sales_item_name		= str(df.loc[top_idx, "item"])
        top_sales_item_total    = float(df.loc[top_idx, "total"])
        top_share_item_rate     = round(top_sales_item_total / total_sales * 100, 1)
    else:
        top_sales_item_name, top_sales_item_total, top_share_item_rate = "-", 0.0, 0.0
    
    summary_tail     	    = pd.DataFrame([{
        "item" : "total_sales",
        "count" : None,
        "price" : None,
        "total" : total_sales
    },{        
        "item" : "average_price",
        "count" : None,
        "price" : None,
        "total" : avg_price_weighted}
    ])
    

    ai_comment = (
        f" {data_label} 月の総売上は {total_sales} 円、平均単価(加重)は {avg_price_weighted} 円です。\n"
        f"最も売れた商品は「{top_sales_item_name}」で、全体の {top_share_item_rate}% を占めています。\n"
        f"全体的に、上位商品の売上が構成比の大部分を占める傾向があります"
        )
    # グラフの作成
    
    fig,axes       = plt.subplots(1, 2, figsize=(10, 5))
    plot_df        = df.sort_values("total",ascending=False).reset_index(drop=True)
    graph_labels   = plot_df["item"]
    graph_total    = plot_df["total"]
    TOP_N          = 3
    top_total_df   = plot_df["total"].head(TOP_N)
    top_item_df    = plot_df["item"].head(TOP_N)
    
    # 棒グラフの作成
    bars = axes[0].bar(
        graph_labels,
        graph_total,
        color="blue"
    )
    axes[0].set_xlabel("item")
    axes[0].set_ylabel("total_sales(JPY)")
    axes[0].set_title(f"{data_label} total_sales")
    axes[0].tick_params(axis="x", rotation=30)
    for bar in bars:
        x = bar.get_x() + bar.get_width()/2
        y = bar.get_height()
        axes[0].text(
            x,
            y,
            f"{int(y):,}",
            ha="center",
            va="bottom"
            
        )
    
    # 円グラフ作成
    if total_sales > 0:
        axes[1].pie(
            top_total_df,
            labels=top_item_df,
            startangle=90,
            autopct="%1.1f%%",
            counterclock=False
        )
        axes[1].axis("equal")
    else:
        axes[1].axis("off")
        axes[1].text(0.0, 0.5, "データなし", fontsize=11, va="center")
    
    axes[1].set_title(f"{data_label} total_sales_share")

    
    out_dir.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    plt.savefig(out_dir / f"report_{data_label}.png", dpi=150)
    plt.close(fig)
    (out_dir/ f"comment_{data_label}.txt").write_text(ai_comment, encoding="utf-8")
    
    monthly_table = pd.concat([df, summary_tail], ignore_index=False)
    with pd.ExcelWriter(out_dir / f"average_price_weighted_{data_label}.xlsx") as writer:
        monthly_table.to_excel(writer, index=False)
    
    summary_rows.append({
        "monthly": data_label,
        "total_sales" : total_sales,
        "average_price" : avg_price_weighted,
        "top_item" : top_sales_item_name,
        "top_share_percent" : top_share_item_rate
    })
    print(ai_comment)

# 月の比較表の出力
summary_df = pd.DataFrame(summary_rows)
summary_df = summary_df.sort_values("monthly").reset_index(drop=True)
summary_df["mom_percent"] = (
    summary_df["total_sales"].pct_change().mul(100).round(1)
    )
summary_df.to_csv(out_root / "summary_all_month.csv", index=False, encoding="utf-8-sig")