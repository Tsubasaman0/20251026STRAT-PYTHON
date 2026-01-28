import json
import requests

url = "http://localhost:11434/api/generate"

with open("plans.json", "r", encoding="utf-8") as f:
    plan_data = json.load(f)

povo = plan_data["povo"]
linemo = plan_data["linemo"]

# 事実テキスト（そのまま説明用に渡す）
povo_text = f"""
povo({povo["carrier"]})
- 基本料: {povo["base_fee"]}円
- データ方式: {povo["data_system"]}
- データトッピング:
""" + "\n".join(
    [f" - {p['name']}: {p['price_yen']}円" for p in povo["data_plans"]]
) + """
- 通話オプション:
""" + "\n".join(
    [f" - {c['name']}: {c['price_yen']}円" for c in povo["call_options"]]
) + """
- 特徴:
""" + "\n".join(
    [f" - {feat}" for feat in povo["features"]]
)

linemo_text = f"""
LINEMO({linemo["carrier"]})
- プラン:
""" + "\n".join(
    [f" - {p['name']}: {p['data_gb']}GB {p['base_fee_yen']}円 / 5分かけ放題込: {p['includes_5min_calls']}" for p in linemo["plans"]]
) + """
- 通話オプション:
""" + "\n".join(
    [f" - {c['name']}: {c['price_yen']}円(対象: {','.join(c['target_plans'])})" for c in linemo["call_options"]]
) + """
- 特徴:
""" + "\n".join(
    [f" - {feat}" for feat in linemo["features"]]
)


def calc_povo_monthly_cost(data_gb: float, calls_5min_count: int) -> int:
    """povoのだいたいの月額（雑でOK）"""
    base = int(povo["base_fee"])  # 0円

    # 必要量を満たす中で一番安いトッピングを選ぶ
    best_data_price = None
    for p in povo["data_plans"]:
        gb = p.get("data_gb")
        price = p["price_yen"]
        if gb is None:
            continue
        if gb >= data_gb:
            if best_data_price is None or price < best_data_price:
                best_data_price = price

    if best_data_price is None:
        best_data_price = max(p["price_yen"] for p in povo["data_plans"])

    # 5分かけ放題をつける前提
    call_option_price = 0
    if calls_5min_count > 0:
        for c in povo["call_options"]:
            if c["name"].startswith("5分"):
                call_option_price = c["price_yen"]
                break

    total = base + best_data_price + call_option_price
    return int(total)


def calc_linemo_monthly_cost(data_gb: float, calls_5min_count: int) -> int:
    """LINEMOのだいたいの月額（雑でOK）"""
    candidates = []

    for p in linemo["plans"]:
        gb = p["data_gb"]
        base_fee = p["base_fee_yen"]
        includes_5min = p["includes_5min_calls"]

        if gb < data_gb:
            continue

        total = base_fee

        if calls_5min_count > 0 and not includes_5min:
            for c in linemo["call_options"]:
                if c["name"].startswith("5分"):
                    total += c["price_yen"]
                    break

        candidates.append(total)

    if not candidates:
        p = max(linemo["plans"], key=lambda x: x["data_gb"])
        total = p["base_fee_yen"]
        if calls_5min_count > 0 and not p["includes_5min_calls"]:
            for c in linemo["call_options"]:
                if c["name"].startswith("5分"):
                    total += c["price_yen"]
                    break
        return int(total)

    return int(min(candidates))


def choose_best_plan(data_gb: float, calls_5min_count: int):
    povo_cost = calc_povo_monthly_cost(data_gb, calls_5min_count)
    linemo_cost = calc_linemo_monthly_cost(data_gb, calls_5min_count)

    if povo_cost < linemo_cost:
        recommended = "povo"
    elif linemo_cost < povo_cost:
        recommended = "LINEMO"
    else:
        recommended = "both_same"

    return povo_cost, linemo_cost, recommended


if __name__ == "__main__":
    # ここから実行部分
    data_gb = 8
    calls_5min = 30

    povo_cost, linemo_cost, recommended = choose_best_plan(data_gb, calls_5min)

    print("DEBUG: povo_cost =", povo_cost)
    print("DEBUG: linemo_cost =", linemo_cost)
    print("DEBUG: recommended =", recommended)

facts_text = """
【povo】
- 基本料0円
- トッピング式
- au回線

【LINEMO】
- 3GB, 30GB のプラン
- 30GB プランは5分かけ放題込み
- LINEギガフリー
"""

user_profile_ja = f"""
[ユーザー条件]
- 1ヶ月のデータ使用量: {data_gb}GB
- 通話: 5分以内の電話が1ヶ月に約{calls_5min}回程度
- 主な使い方: LINE通話とSNS、1周間に約5時間の動画視聴をする
"""

prompt = f"""
You are a mobile plan advisor.

You are given:
- Facts about two Japanese mobile plans (in Japanese).
- A user's usage profile (in Japanese).
- The monthly cost of each plan already calculated in Python.

Your job:
- The logical content and comparison result are ALREADY decided in PYTHON RESULT.
- Do NOT add any new logical reasoning.
- Do NOT describe who is cheaper or more expensive by yourself.
- Just rewrite the given PYTHON RESULT and FACTS into natural Japanese sentences,
  without changing any meaning or numbers.

Output format (in Japanese):
1. ユーザー条件の要約
2. povo のメリット・デメリット（このユーザーにとって）
3. LINEMO のメリット・デメリット（このユーザーにとって）
4. どちらをおすすめするかと、その理由（必ず月額料金 {povo_cost}円 / {linemo_cost}円 に触れる）

==================
FACTS (in Japanese)
==================
{facts_text}

==================
USER PROFILE (in Japanese)
==================
{user_profile_ja}

==================
PYTHON RESULT (monthly cost, in yen)
==================
- povo: {povo_cost}円 / 月
- LINEMO: {linemo_cost}円 / 月
- recommended: {recommended}
"""

print("\nDEBUG: sending request to ollama...")
payload = {
        "model": "phi3",
        "prompt": prompt,
        "stream": False,
        "temperature": 0.2,
    }

res = requests.post(url, json=payload)
print("DEBUG: HTTP status =", res.status_code)
try:
    res.raise_for_status()
except Exception as e:
    print("HTTP ERROR:", e)
    print("RAW RESPONSE:", res.text)
    raise

data = res.json()
print("\n=== CLEAN RESPONSE ===")
print(data.get("response", "responseフィールドがありません"))