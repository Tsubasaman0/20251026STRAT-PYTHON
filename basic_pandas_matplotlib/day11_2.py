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



# 2:トータル売り上げと平均価格のデータ追加

tabel_out_data = []

for f in data:
    f["total"]      = f["price"] * f["count"]
    total_sales     = round(f["total"].sum())
    average_price   = round(f["price"].mean())
    summary_row     = pd.DataFrame([{
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


# 3:csvファイルごとにデータ作成

fig,axes = plt.subplots(1, 2, tight_layout=True)

for data in tabel_out_data:
	
	axes[0] = 
