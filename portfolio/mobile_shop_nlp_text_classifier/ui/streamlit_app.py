import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  # FastAPIのURL

st.set_page_config(page_title="Mobile Shop FAQ Classifier", layout="centered")

st.title("📱 Mobile Shop FAQ Classifier")
st.write("携帯販売の問い合わせ文を入力すると、カテゴリを推定します。")

text = st.text_area("問い合わせ文", height=120, placeholder="例）MNPしたら解約金はいくらですか？")

col1, col2 = st.columns(2)
with col1:
    threshold = st.slider("needs_review 期待値", 0.50, 0.95, 0.65, 0.01)
with col2:
    st.caption("confidence が期待値未満なら needs_review=True")

if st.button("分類する", type="primary"):
    if not text.strip():
        st.warning("テキストを入力してください。")
        st.stop()

    try:
        res = requests.post(
            f"{API_URL}/predict",
            json={"text": text.strip()},
            timeout=5
        )
        if res.status_code != 200:
            st.error(f"API error: {res.status_code} {res.text}")
            st.stop()

        data = res.json()

        st.subheader("結果")
        st.metric("予測カテゴリ", data.get("label", "-"))

        conf = data.get("confidence", None)
        if conf is None:
            st.info("このモデルは confidence を返しません（predict_proba非対応）。")
        else:
            st.metric("confidence", f"{conf:.3f}")

        # 閾値はUI側で再判定（APIと値変えて試せる）
        needs_review_ui = (conf is None) or (conf < threshold)
        if needs_review_ui:
            st.warning("⚠️ needs_review: 人の確認が必要かも")
        else:
            st.success("✅ 自動対応してOKそう")

        # 候補表示（APIがcandidates返す場合）
        candidates = data.get("candidates")
        if candidates:
            st.subheader("上位候補（top3）")
            for c in candidates:
                st.write(f"- **{c['label']}** : {c['proba']:.3f}")

    except requests.exceptions.ConnectionError:
        st.error("FastAPIに接続できません。先に FastAPI を起動してください。")
    except Exception as e:
        st.error(f"Unexpected error: {e}")