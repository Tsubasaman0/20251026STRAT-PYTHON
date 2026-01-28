# mobile_comment.py
import requests
from mobile_calc import choose_best_plan

URL = "http://localhost:11434/api/generate"


def build_prompt(data_gb, calls_5min, result):
    povo_cost = result["povo_cost"]
    linemo_cost = result["linemo_cost"]
    recommended = result["recommended"]

    prompt = f"""
あなたはスマホ料金のアドバイザーです。
以下の情報を読み取り、日本語でユーザー向けにわかりやすく説明してください。

[ユーザー条件]
- 1ヶ月のデータ使用量: {data_gb}GB
- 5分以内の通話回数: {calls_5min}回/月

[診断結果（Pythonで計算済み）]
- povo の見積もり月額: {povo_cost}円
- LINEMO の見積もり月額: {linemo_cost}円
- Pythonが安いと判定したプラン: {recommended}

制約:
- 新しい料金や割引、GB数や回数を作らないでください。
- 使ってよい数字は次だけです: {data_gb}, {calls_5min}, {povo_cost}, {linemo_cost}
- それ以外の数字は書いてはいけません。
- 料金の計算をやり直さないでください（差額や合計を計算しない）。
- サービス品質・通信速度・エリアなど、ここで与えていない情報についてコメントしないでください。
- 「以上」「未満」「十分」「最適」「制限」「高品質」など、プランの性能を評価する言葉は使わないでください。
- 次の一文を、4番目の文の中に一語一句そのまま入れてください（1回だけ）:
  povoは月額{povo_cost}円、LINEMOは月額{linemo_cost}円です。

出力フォーマット:
- 下の4つの行をこの順番で出力してください。
- 各行は「番号. ラベル: 説明文」の1行だけにしてください。
- 番号とラベルの部分（コロンまで）はそのまま使ってください。

1. ユーザー条件の要約:
2. povo の説明（このユーザーにとってのポイント）:
3. LINEMO の説明（このユーザーにとってのポイント）:
4. どちらをおすすめするかと、その理由:
"""
    return prompt


if __name__ == "__main__":
    data_gb = 8
    calls_5min = 30

    result = choose_best_plan(data_gb, calls_5min)
    povo_cost = result["povo_cost"]
    linemo_cost = result["linemo_cost"]
    recommended = result["recommended"]

    prompt = build_prompt(data_gb, calls_5min, result)

    payload = {
        "model": "phi3",
        "prompt": prompt,
        "stream": False,
        "temperature": 0.2,
    }

    print("=== DEBUG prompt ===")
    print(prompt)

    res = requests.post(URL, json=payload)
    res.raise_for_status()
    data = res.json()
    raw = data.get("response", "")

    print("\n=== RAW LLM RESPONSE ===")
    print(raw)

    # ---- ここから後処理 ----
    lines = [l.strip() for l in raw.splitlines() if l.strip()]

    # 「1.」「2.」「3.」「4.」で始まる行だけ拾う
    slots = {"1": "", "2": "", "3": "", "4": ""}
    for line in lines:
        for k in slots.keys():
            prefix = f"{k}."
            if line.startswith(prefix) and not slots[k]:
                slots[k] = line
                break

    # 足りないところはこっちで埋める
    if not slots["1"]:
        slots["1"] = f"1. ユーザー条件の要約: 1ヶ月にデータ{data_gb}GB、5分以内の通話{calls_5min}回/月を利用するユーザーです。"
    else:
        body1 = slots["1"].split(":", 1)[-1].strip()
    slots["1"] = f"1. ユーザー条件の要約: {body1}"

    if not slots["2"]:
        slots["2"] = f"2. povo の説明（このユーザーにとってのポイント）: データ{data_gb}GB・通話{calls_5min}回/月の条件で、見積もり月額は{povo_cost}円です。"
    else:
        body2 = slots["2"].split(":", 1)[-1].strip()
    slots["2"] = f"2. povo の説明（このユーザーにとってのポイント）: {body2}"

    if not slots["3"]:
        slots["3"] = f"3. LINEMO の説明（このユーザーにとってのポイント）: 同じ条件で、見積もり月額は{linemo_cost}円です。"
    else:
        body3 = slots["3"].split(":", 1)[-1].strip()
    slots["3"] = f"3. LINEMO の説明（このユーザーにとってのポイント）: {body3}"

    sentence = f"povoは月額{povo_cost}円、LINEMOは月額{linemo_cost}円です。"
    if not slots["4"]:
        slots["4"] = (
            f"4. どちらをおすすめするかと、その理由: "
            f"{sentence} この条件では、見積もり月額が低い{recommended}をおすすめします。"
        )
    else:
        # 4 行目に必須文が入っていなければ、先頭に足す
        if sentence not in slots["4"]:
            # 「4. ラベル: 」の後ろに差し込む
            label_prefix = "4. どちらをおすすめするかと、その理由:"
            if slots["4"].startswith(label_prefix):
                rest = slots["4"][len(label_prefix):].strip()
                if rest:
                    slots["4"] = f"{label_prefix} {sentence} {rest}"
                else:
                    slots["4"] = f"{label_prefix} {sentence}"
            else:
                # ラベルがおかしかったときの保険
                slots["4"] = f"4. どちらをおすすめするかと、その理由: {sentence} この条件では、見積もり月額が低い{recommended}をおすすめします。"

    print("\n=== FIXED OUTPUT ===")
    print(slots["1"])
    print(slots["2"])
    print(slots["3"])
    print(slots["4"])