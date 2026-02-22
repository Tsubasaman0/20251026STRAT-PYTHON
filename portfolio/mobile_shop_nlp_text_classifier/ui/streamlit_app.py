# ui/app.py
import requests
import streamlit as st

st.set_page_config(page_title="Mobile Shop FAQ Classifier", layout="centered")
st.title("📱 Mobile Shop FAQ Classifier")

# docker compose 内では api サービス名がホストになる
API_URL = "http://api:8000"

text = st.text_area(
    "問い合わせ文",
    placeholder="例：MNPしたら解約金はいくらですか？",
    height=120
)

threshold = st.slider("needs_review 閾値", 0.50, 0.95, 0.65, 0.01)

if st.button("分類する", type="primary", use_container_width=True):
    if not text.strip():
        st.warning("テキストを入力してください")
    else:
        try:
            r = requests.post(
                f"{API_URL}/predict",
                json={"text": text.strip()},
                timeout=10
            )
            r.raise_for_status()
            data = r.json()

            st.subheader("結果")
            st.write(f"**label:** {data.get('label')}")
            conf = data.get("confidence")
            st.write(f"**confidence:** {conf}")

            needs_review = data.get("needs_review")
            if needs_review is None and conf is not None:
                needs_review = conf < threshold

            if needs_review:
                st.warning("⚠️ needs_review: 人が確認した方がよさそうです")
            else:
                st.success("✅ 自動振り分けしてOKそうです")

            st.caption("※ confidence はモデルの最大確率（高いほど自信が強い）")

        except Exception as e:
            st.error(f"API呼び出しに失敗しました: {e}")
            st.info("APIが起動しているか /health を確認してね")