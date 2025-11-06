import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import os


# 1:準備 --ファイルやフォルダを作成するための変数やファイルの読み込み

today       = dt.date.today().strftime("%Y_%m_%d")
folder      = "A_monthly_reports"
file_path   = "data_files"
file_list   = os.listdir(file_path)
os.makedirs(folder, exist_ok=True)

data        = []

for file_name in file_list:
    file = pd.read_csv(f"{file_path}/{file_name}")
    data.append(file)


# 2:トータル売り上げと平均価格、棒グラフ用データなどのデータ作成

tabel_out_data = []
graph_out_data = []

for i, f in enumerate(data):
    fig,axes    = plt.subplots(1, 2, figsize=(10, 5))
    data_label              = file_list[i].replace("data_", "").replace(".csv", "")
    os.makedirs(f"{folder}/report_{data_label}", exist_ok=True)
    f["total"]    	 	    = f["price"] * f["count"]
    total_sales			    = round(f["total"].sum())
    average_price   		= round(f["price"].mean())
    top_sales_item_name		= f["item"][f["total"].idxmax()]
    top_sales_item_total    = f["total"].max()
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
    
    tabel_out_data.append(pd.concat([f, summary_row]))
    graph_out_data = f.sort_values("total").reset_index()

    ai_comment = (
        f" {data_label} 月の総売上は {total_sales} 円、平均単価は {average_price} 円です。\n"
        f"最も売れた商品は「{top_sales_item_name}」で、全体の {top_share_item_rate}% を占めています。\n"
        f"全体的に、上位商品の売上が構成比の大部分を占める傾向があります"
        )
    
    # 棒グラフの作成
    bars = axes[0].bar(
        graph_out_data["item"],
        graph_out_data["total"],
        color="blue"
    )
    axes[0].set_xlabel("item")
    axes[0].set_ylabel("total_sales(JPY)")
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
    print(graph_out_data)
    plt.savefig(f"{folder}/{data_label}.png")
    plt.close(fig)