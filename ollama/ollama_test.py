import requests
import json

url = "http://localhost:11434/api/generate"

with open("plans.json", "r", encoding="utf-8") as f:
    plan_data = json.load(f)

facts = json.dumps(plan_data, ensure_ascii=False, indent=2)

# ユーザー条件(ここを好きに書き換える)
user_condition = """"
[ユーザー条件]
- 月のデータ量: 8GB
- 通話: ほとんどしない(5分かけ放題は不要)
- 重視すること: 毎月の料金をできるだけ安く
"""

question = "povoとLINEMOの違いをわかりやすく説明して"

TEMPLATE = """
[役割]
あなたはスマホ料金アドバイザーです。

[厳格なルール]
- 事実の説明は、必ず次のJSONデータに書かれている内容だけを使うこと。
- JSON に書かれていない料金、キャンペーン、サービス名を、新しく作ってはいけません。
- JSONに書かれていないことは『ここでは不明』と答えること。
- 「LINEモバイル」「カーボナード」などの、このJSONに無い単語を出してはいけません。

[プラン情報（JSON）]
```json
{facts}
{user_condition}

[タスク]
次の質問に日本語で答えてください:
「{question}」

[出力形式]
1. 要約（中学生でもわかる表現で）
2. povo の特徴(JSONに書かれている項目だけで)
3. LINEMO 特徴(JSONい書かれている項目だけで)
4. どんな人にどちらがおすすめか(ユーザー条件を踏まえて理由を書く)
"""

prompt = TEMPLATE.format(
    facts=facts,
    user_condition=user_condition,
    question=question,
)

payload = {
    "model": "phi3",
    "prompt": prompt,
    "stream": False,
    "temperature": 0.0
}

res  = requests.post(url, json=payload)
res.raise_for_status()

data = res.json()
text = data["response"]

if ("povo" not in text) or ("LINEMO" not in text):
    print("* 回答に必要情報がないため放棄しました")


print("\n=== CLEAN RESPONSE ===")
print(text)
