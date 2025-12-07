import requests
import json
import re

url = "http://localhost:11434/api/generate"

with open("plans.json", "r") as f:
    plan_data = json.load(f)

povo = plan_data["povo"]
linemo = plan_data["linemo"]

def calc_povo_monthly_cost(data_gb: float, calls_5min_count: int):
    """povoのだいたいの料金を計算"""
    base = int(povo["base_fee"])

    # データ:
    # 渡された使用GB数に応じて、必要なトッピングGB数を選ぶ
    best_data_price = None
    for p in povo["data_plans"]:
        gb = p.get("data_gb")
        price = p["price_yen"]
        # data_gbがNobe(24時間使い放題)は一旦無視
        if gb is None:
            continue
        if gb >= data_gb:
            if best_data_price is None or price < best_data_price:
                best_data_price = price
    
    if best_data_price is None:
        # 全然足りない場合は一番大きい容量を買う
        best_data_price = max(p["price_yen"])

 
    # 通話:
    # 5分以内の通話がそれなりにあるという設定
    call_option_price = 0
    if calls_5min_count > 0:
        for c in povo["call_options"]:
            if c["name"].startswith("5分"):
                call_option_price = c["price_yen"]                       
                break

    total = base + best_data_price + call_option_price
    return int(total)