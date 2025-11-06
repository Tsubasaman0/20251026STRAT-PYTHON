import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import os


# 1:準備 --ファイルやフォルダを作成するための変数やファイルの読み込み

today       = dt.date.today().strftime("%Y_%m_%d")
folder      = "A_monthly_reports"
file_path   = "data_files"
file_list   =  os.listdir(file_path)

data        = []

for file_name in file_list:
    file = pd.read_csv(f"{file_path}/{file_name}")
    data.append(file)

os.makedirs(folder, exist_ok=True)



# 2:トータル売り上げと平均価格、棒グラフ用データなどのデータ作成

tabel_out_data = []
graph_out_data = []

for f in data:
    f["total"]    	 	  = f["price"] * f["count"]
    total_sales			    = round(f["total"].sum())
    average_price   		= round(f["price"].mean())
    total_sales_rank		= f.sort_values("total").reset_index()
    top_sales_item			= f["item"][f["total"].idxmax()]
    top_sales_item_total= f["total"].max()
    print(top_sales_item_total)
    top_share_item_rate = round(top_sales_item_total / total_sales * 100, 1)
    summary_row     	= pd.DataFrame([{
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
    graph_out_data.append(total_sales_rank)

print(graph_out_data)

# 3: AIコメント

ai_comment = f"総売上は {total_sales} 円、平均単価は {average_price} 円です。最も売れた商品は「{top_sales_item}」で、全体の {top_share_item_rate}% を占めています。全体的に、上位商品の売上が構成比の大部分を占める傾向があります"

# 4:csvファイルごとにデータ作成

fig,axes = plt.subplots(1, 2, tight_layout=True)

for data in tabel_out_data:
	
	axes[0].bar(
		data["item"],
		data["total"])
