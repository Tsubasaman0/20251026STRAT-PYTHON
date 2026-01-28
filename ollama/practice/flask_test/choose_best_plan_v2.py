# choose_best_plan_v2.py

def choose_best_plan_v2(data_gb, calls_5min):

    # =====入力エラーチェック=====
    if data_gb < 0 or calls_5min < 0:
        return {
            "status": "error",
            "reason": "入力は0以上にしてください"
        }
    
    if data_gb > 30:
        return {
            "status": "unsupported",
            "reason": "30GBを超える場合はこの料金診断は扱っておりません。"
        }

    povo_cost = 0
    linemo_cost = 0

    # =====povoの料金目安計算=====
    if data_gb <= 3: # 3GB以下
        povo_cost += 900
    elif data_gb <= 6: # 6GB以下
        povo_cost += 1580
    elif data_gb <= 30: # 30GB以下
        povo_cost += 2700
    else:
        povo_cost += 2700 # 30GB以上は、30GBの料金で処理

    if calls_5min > 20: # 5分かけ放題なしの場合、従量課金で 30秒22円 × 20回 = 880円 、なので損益分岐点は最低発信回数20回
        povo_cost += 880

    # ======LINEMOの料金計算=====
    if data_gb <= 3: # 3GB以下
        linemo_cost += 990
        linemo_5min_included = False
    else:
        linemo_cost += 2970 # 3GB以上は30GBの料金で処理
        linemo_5min_included = True # 30GBプランは5分かけ放題が内包

    # =====比較=====

    if calls_5min > 20 and not linemo_5min_included:
        linemo_cost += 880

    if povo_cost < linemo_cost:
        recommended = "povo"
    elif linemo_cost < povo_cost:
        recommended = "LINEMO"
    else:
        recommended = "same"
    
    return {
        "status": "ok",
        "povo_cost": povo_cost,
        "linemo_cost": linemo_cost,
        "recommended": recommended
    }
    
#print(choose_best_plan_v2(1, 0))     # データ少・通話少
# ・povo: data_gb=1 → 900円 # 1GB なので「3GB以下」の900円プランに入る
# 	calls_5min=0 → 0円
# 	合計 900円
# ・LINEMO: data_gb=1 → 990円
# 	calls_5min=0 → 0円
# 	合計 990円
# povo のほうが安いので povo がおすすめ

#print(choose_best_plan_v2(3, 30))    # 少データ・通話多
# ・povo: data_gb=3 → 900円
# 	calls_5min=30 → 880円
# 	合計 1780円
# ・LINEMO: data_gb=3 → 990円
# 	calls_5min=30 → 880円
# 	合計 1870円
# povo のほうが安いので povo がおすすめ

#print(choose_best_plan_v2(8, 30))    # 中データ・通話多（＝自分の条件に近い）
# ・povo: data_gb=8 → 2700円
# 	calls_5min=30 → 880円
# 	合計 3580円
# ・LINEMO: data_gb=8 → 2970円
#   2970円のプランは5分かけ放題込み
# 	合計 2970円
# LINEMO のほうが安いので LINEMO がおすすめ

#print(choose_best_plan_v2(30, 0))    # 大データ・通話なし
# ・povo: data_gb=30 → 2700円
#   calls_5min=0 → 0円
# 	合計 2700円
# ・LINEMO: data_gb=30 → 2970円
# 	2970円のプランは5分かけ放題込み
# 	合計 2970円
#   povo のほうが安いので povo がおすすめ

# print(choose_best_plan_v2(50, 40))   # 想定外に多い
# ・povo: data_gb=50 → 2700円
# 	calls_5min= 40 → 880円
# 	合計 3580円
# ・LINEMO: data_gb=50 → 2970円 # 3GBを超えるので30GBプラン(2970円)扱い
# 	2970円のプランは5分かけ放題込み
# 	合計 2970円
# LINEMO のほうが安いので LINEMO がおすすめ

# print(choose_best_plan_v2(-1, 0))
# ValueError: 入力は0以上をしてください
