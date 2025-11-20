from pathlib import Path
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

#1 準備、ファイル、フォルダ作のための変数やファイルの読み込み

today       = dt.date.today().strftime("%Y_%m_%d")
out_root    = Path("my_monthly_reports")
in_dir      = Path("data_files")
csv_files   = sorted(p for p in in_dir.iterdir() if p.suffix.lower() == ".csv")
out_root.mkdir(parents=True, exist_ok=True)

TOP_N       = 3 # 円グラフに出す上位件数

def load_and_prepara(csv_path: Path) -> pd.DataFrame | None:
    """ひとつのCSVをも読み込んで、全処理まで済ませたdfを返す、失敗したらNone"""
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"WARNING 読込失敗: {csv_path.name} ({e})")
        return None
    
    required_cols = {"item", "price", "count"}
    if not required_cols.issubset(df.columns):
        print(f"WARNING カラム不足: {csv_path.name} 必要: {required_cols} 実際: {set(df.columns)}")
        return None
    
    #数値の安全化
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
    df["count"] = pd.to_numeric(df["count"], errors="coerce").fillna(0).astype(int)
    df["total"] = df["price"] * df["count"]

    return df

#2 total売り上げと平均価格、棒グラフデータ用などのデータ作成

summary_rows = []

for csv_path in csv_files:
    data_lavel = csv_path.stem.replace("data_", "")
    out_dir    = out_root / f"report_{data_lavel}"
    out_dir.mkdir(parents=True, exist_ok=True)

    # 読込と前処理（ここが関数になった）
    df = load_and_prepara(csv_path)
    if df is None:
        continue # このファイルはスキップ

    # 合計売上と単価の加重平均金額
    total_sales         = int(df["total"].sum())
    total_count         = int(df["count"].sum())
    avg_price_weighted  = int(round(total_sales / total_count)) if total_count > 0 else 0
    
    # csv用商品構成を入力
    if total_sales > 0:
        df["share_percent"] = (df["total"] / total_sales * 100).round(2)
    else:
        df["share_percent"] = 0
        
    # トップ商品情報
    if len(df) and total_sales > 0:
        top_idx              = df["total"].idxmax()
        top_sales_item_name  = str(df.loc[top_idx, "item"])
        top_sales_item_total = float(df.loc[top_idx, "total"])
        top_share_item_rate  = round(top_sales_item_total / total_sales * 100, 1)
    else:
        top_sales_item_name, top_sales_item_total, top_sales_item_rate = "-", 0.0, 0.0
        
    # テーブル末尾にサマリー行をつける
    summary_tail = pd.DataFrame([
        {
            "item": "total_sales",
            "count": None,
            "price": None,
            "total": total_sales
        },
        {
            "item": "average_price_weighted",
            "count": None,
            "price": None,
            "total": avg_price_weighted
        }
    ])
    
    ai_comment = (
        f"{data_lavel} 月に総売り上げ {total_sales} 円、平均単価（加重） {avg_price_weighted} 円です。\n"
        f"最も売れた商品は「{top_sales_item_name}」で、全体の {top_share_item_rate}% 占めています。\n"
        f"全体的に、状商品の売り上げが構成比の大部分を占める傾向があります"
    )
    
    # グラフ作成
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # 棒グラフ用のデータ(降順)
    plot_df         = df.sort_values("total", ascending=False).reset_index(drop=True)
    graph_labels    = plot_df["item"]
    graph_total     = plot_df["total"]

    # 棒グラフ
    bars = axes[0].bar(
        graph_labels,
        graph_total,
        color="blue"
    )
    axes[0].set_ylabel("item")
    axes[0].set_xlabel("total_sales(JPY)")
    axes[0].set_title(f"{data_lavel} total_sales")
    axes[0].tick_params(axis="x", rotation=30)

    for bar in bars:
        x = bar.get_x() + bar.get_width() / 2
        y = bar.get_height()
        axes[0].text(
            x,
            y,
            f"{int(y):,}",
            ha="center",
            va="bottom"
        )
        
    # 円グラフ用に上位TOP_Nだけ取り出し
    top_total_df = plot_df["total"].head(TOP_N)
    top_item_df  = plot_df["item"].head(TOP_N)

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

    axes[1].set_title(f"{data_lavel} total_sales_share")

    fig.tight_layout()
    plt.savefig(out_dir / f"report_{data_lavel}.png", dpi=150)
    plt.close(fig)

    # コメントテキスト出力
    (out_dir / f"comment_{data_lavel}.txt").write_text(ai_comment, encoding="utf-8")

    # Excel出力（明細＋サマリー
    monthly_tabel = pd.concat([df, summary_tail], ignore_index=False)
    with pd.ExcelWriter(out_dir / f"average_price_weighted_{data_lavel}.xlsx") as writer:
        monthly_tabel.to_excel(writer, index=False)
    
    # 全月サマリー用の行を追加
    summary_rows.append({
        "monthly": data_lavel,
        "total_sales": total_sales,
        "average_price": avg_price_weighted,
        "top_item": top_sales_item_name,
        "top_share_percent": top_share_item_rate
    })
    
    print(ai_comment)

    
# 月の比較表の出力
summary_df = pd.DataFrame(summary_rows)

# 月順に並べる（”YYYY_MM”想定）
summary_df = summary_df.sort_values("monthly").reset_index(drop=True)

# 前月比(％)を追加
summary_df["mom_percent"] = (
    summary_df["total_sales"]
    .pct_change()
    .mul(100)
    .round(1)
)

# CSV保存(Execlで開きやすいようにutf-8-sig)
summary_df.to_csv(out_root / "summary_all_monthly.csv", index=False, encoding="utf-8-sig")