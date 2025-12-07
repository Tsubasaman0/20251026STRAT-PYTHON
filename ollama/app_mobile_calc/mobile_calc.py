# mobile_calc.py

import json
from pathlib import Path

# ==========
# 設定・データ読み込み
# ==========

DATA_PATH = Path(__file__).parent / "plans.json"

with DATA_PATH.open("r", encoding="utf-8") as f:
    plan_data = json.load(f)

POVO = plan_data["povo"]
LINEMO = plan_data["linemo"]


# ==========
# 計算ロジック
# ==========

def calc_povo_monthly_cost(data_gb: float, calls_5min_count: int) -> int:
    """
    povoの“ざっくり月額”を計算する関数。

    前提:
    - data_plans の duration_days を使って 30日あたりの料金・GB に正規化する
    - ユーザーはほぼ一定ペースでデータを消費する前提（150GB/90日なら 50GB/月扱い）
    - 通話は「5分かけ放題」を付けるかどうかだけで近似する
    - 細かい従量課金や日割りは無視した“診断用のラフなモデル”
    """
    base = int(POVO["base_fee"])

    best_monthly_data_fee = None

    for p in POVO["data_plans"]:
        gb = p.get("data_gb")
        price = p["price_yen"]
        days = p.get("duration_days")

        # 期間情報がない or 24時間系は一旦無視
        if gb is None or days is None:
            continue

        # 月額に正規化（30日換算）
        monthly_fee = price * (30 / days)

        # 「30日あたりの提供GB」が data_gb を満たすか雑にチェック
        monthly_gb = gb * (30 / days)
        if monthly_gb < data_gb:
            continue

        if best_monthly_data_fee is None or monthly_fee < best_monthly_data_fee:
            best_monthly_data_fee = monthly_fee

    if best_monthly_data_fee is None:
        # どうしても見つからなければ、一番大きいプランを月額換算して使う
        best_monthly_data_fee = max(
            p["price_yen"] * (30 / p["duration_days"])
            for p in POVO["data_plans"]
            if p.get("duration_days")
        )

    # 通話（ここは今のままでいい）
    call_option_price = 0
    if calls_5min_count > 0:
        for c in POVO["call_options"]:
            if c["name"].startswith("5分"):
                call_option_price = c["price_yen"]
                break

    total = base + best_monthly_data_fee + call_option_price
    return int(total)


def calc_linemo_monthly_cost(data_gb: float, calls_5min_count: int) -> int:
    """LINEMO のだいたいの月額料金を計算する（雑でOK）"""
    if data_gb < 0 or calls_5min_count < 0:
        raise ValueError("data_gb と calls_5min_count は 0 以上にしてください。")

    candidates: list[int] = []

    for p in LINEMO["plans"]:
        gb = p["data_gb"]
        base_fee = p["base_fee_yen"]
        includes_5min = p["includes_5min_calls"]

        # データ量を満たさないプランは除外
        if gb < data_gb:
            continue

        total = base_fee

        # 5分かけ放題が込みでない場合、オプション追加
        if calls_5min_count > 0 and not includes_5min:
            for c in LINEMO["call_options"]:
                if c["name"].startswith("5分"):
                    total += c["price_yen"]
                    break

        candidates.append(total)

    # どのプランもデータ量を満たさない極端なケース
    if not candidates:
        p = max(LINEMO["plans"], key=lambda x: x["data_gb"])
        total = p["base_fee_yen"]
        if calls_5min_count > 0 and not p["includes_5min_calls"]:
            for c in LINEMO["call_options"]:
                if c["name"].startswith("5分"):
                    total += c["price_yen"]
                    break
        return int(total)

    return int(min(candidates))

DUBUG = False

def choose_best_plan(data_gb: float, calls_5min_count: int):
    """2社の見積もりを比較して、おすすめを返す"""
    povo_cost = calc_povo_monthly_cost(data_gb, calls_5min_count)
    linemo_cost = calc_linemo_monthly_cost(data_gb, calls_5min_count)

    if DUBUG:
        print("[DEBUG CHK] povo_cost =", povo_cost)
        print("[DEBUG CHK] linemo_cost =", linemo_cost)

    if povo_cost < linemo_cost:
        recommended = "povo"
    elif linemo_cost < povo_cost:
        recommended = "LINEMO"
    else:
        recommended = "both_same"

    return {
        "povo_cost": povo_cost,
        "linemo_cost": linemo_cost,
        "recommended": recommended,
    }


# ==========
# 簡易テスト（手動確認用）
# ==========

def _debug_case(data_gb, calls_5min):
    result = choose_best_plan(data_gb, calls_5min)
    print(f"\n=== data_gb={data_gb}, calls_5min={calls_5min} ===")
    print("povo  :", result["povo_cost"], "円/月")
    print("LINEMO:", result["linemo_cost"], "円/月")
    print("おすすめ:", result["recommended"])


if __name__ == "__main__":
    # 自分で「こうなるはず」と頭で決めてから見ること
    _debug_case(8, 30)   # 今の自分の条件
    _debug_case(1, 0)    # ほぼ待ち受け
    _debug_case(30, 0)   # データ多め・通話ほぼなし