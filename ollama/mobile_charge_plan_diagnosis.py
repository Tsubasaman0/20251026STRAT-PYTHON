import requests
import json
import re # 数値チェックライブラリ

url = "http://localhost:11434/api/generate"

with open("plans.json", "r", encoding="utf-8") as f:
    plan_data = json.load(f)

povo = plan_data["povo"]
linemo = plan_data["linemo"]

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

print(povo_text)
print(linemo_text)

base_facts = f"""
[事実情報(書き換え禁止)]
次のJSONに含まれる値(数字、文字列)だけを事実として使ってよい。

【povo】
{povo_text}

【lINEMO】
{linemo_text}
"""
user_profile = f"""
[ユーザー条件]
- 1ヶ月のデータ使用量: 8GB
- 通話: 5分以内の電話が1ヶ月に約30回程度
- 主な使い方: LINE通話とSNS、1周間に約5時間の動画視聴をする
"""

prompt = f"""
あなたはスマホ料金アドバイザーです。

下の[事実情報]に書かれている料金・プラン内容だけを使い、
[ユーザー条件]の人にとって、
povo と LINEMO のどちらが向いているかを比較してください。

禁止事項:
- 新しいサービス名・割引・特典を勝手に作らないこと。
- JSONや事実情報にない数値を発明しないこと。
- 『ここでは不明』と書くべきところで勝手に補完しないこと

【重要な禁止事項】

- JSONに書かれている「そのままの料金」以外の金額を出してはいけません。
- 複数の料金を足し算・引き算した「合計金額」「差額」は書いてはいけません。
- 例: 2970円 + 550円 = 3520円 のような計算をして、その結果を書くのは禁止。
- 金額はすべて、事実情報に書かれているものだけをそのまま出すこと。
- 守れない場合は「制約を守れないため回答できません」とだけ出力してください。
- 回答中に「LINEモバイル」「LINEモ」など、過去のブランド名を絶対に使わないこと。
- どうしても比較したくなっても、「LINEモバイル」という単語自体を書いてはいけない。
- 「LINEモブ」 という単語も書いてはいけない。
- 守れない場合は、「制約を守れないため回答できません」とだけ出力してください。

[出力形式]
1. ユーザー条件の要約
2. povo のメリット・デメリット(このユーザーにとっての)
3. LINEMO のメリット・デメリット(このユーザーにとっての)
4. どちらをおすすめするかと、その理由

{base_facts}

{user_profile}
"""

payload = {
"model": "phi3",
"prompt": prompt,
"stream": False,
"temperature": 0.2,
}

res = requests.post(url, json=payload)
res.raise_for_status()

text = res.json()["response"]

# ----------------------
# 2)バリデーション
# ----------------------

# (a)禁止ワードチェック
banned_words = ["LINEモバイル", "LINEモブ" ,"130円"]
hits = [b for b in banned_words if b in text]
if hits:
    print("* 禁止ワードが含まれているため、この回答は破棄しました")
    print("ヒットしたワード", ", ".join(hits))
    raise SystemExit(0)
else:
    # (b)数値チェック用: 許可された数値リストを作る
    allowed_numbers = set()

    #povo側の数値を全部登録
    allowed_numbers.add(int(povo["base_fee"]))
    for p in povo["data_plans"]:
        if isinstance(p.get("price_yen"), (int, float)):
            allowed_numbers.add(int(p["price_yen"]))
        if isinstance(p.get("data_gb"), (int, float)):
            allowed_numbers.add(int(p["data_gb"]))
    for c in povo["call_options"]:
        if isinstance(c.get("price_yen"), (int, float)):
            allowed_numbers.add(int(c["price_yen"]))
    
    # LINEMO側の数値を全部登録
    for p in linemo["plans"]:
        if isinstance(p.get("base_fee_yen"), (int, float)):
            allowed_numbers.add(int(p["base_fee_yen"]))
        if isinstance(p.get("data_gb"), (int, float)):
            allowed_numbers.add(int(p["data_gb"]))
    for c in linemo["call_options"]:
        if isinstance(c.get("price_yen"), (int, float)):
            allowed_numbers.add(int(c["price_yen"]))

    # (c) LLMの出力から半角数字を全部抜き出す
    found_numbers = re.findall(r"\d+", text)
    found_numbers_int = {int(n) for n in found_numbers}

    # (d) 許可されていない数値が混ざっていないかチェック
    unknown_numbers = {n for n in found_numbers_int if n not in allowed_numbers and n > 31}

    # 「危険判定」用: 明らかに金額っぽいでかい数字
    danger_numbers = {n for n in unknown_numbers if n >= 1000}

    if danger_numbers:
        print("* JSONいnぞんざいしない金額が含まれているため、この回答は破棄しました")
        print(" 許可外の金額: ", danger_numbers)
        raise SystemExit(0)
    else:
        if unknown_numbers:
            print("* JSONに存在しない数値が含まれているため、この回答は要注意です")
            print("  許可外の数値: ", unknown_numbers)
        print("\n=== CLEAN RESPONSE ===")
        print(text)