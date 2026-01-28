# train_text_classifier.py
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix

from sudachipy import dictionary, tokenizer as sudachi_tokenizer

from src.config import MODEL_FAQ_DIR, MODEL_FAQ_PATH, FAQ_CSV_PATH

tokenizer_obj = dictionary.Dictionary().create()
mode = sudachi_tokenizer.Tokenizer.SplitMode.C

def sudachi_tokenizer(text):
    return [m.surface() for m in tokenizer_obj.tokenize(text, mode)]

def main():
    # 1. データ読み込み
    df = pd.read_csv(FAQ_CSV_PATH)

    X = df["text"]
    y = df["label"]
    print(df["label"].value_counts())

    # 2. train / test 分割
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.3,
        random_state=42,
        stratify=y
    )

    # 3. パイプラインモデル、これを書き換える
    pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        analyzer="char",
        ngram_range=(2, 5),
        min_df=1
    )),
    ("clf", LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ))
    ])

    # 4. 学習
    pipeline.fit(X_train, y_train)

    # 5. 評価
    y_pred = pipeline.predict(X_test)

    print("=== classification report")
    print(classification_report(y_test, y_pred))

    print("=== confusion metrix ===")
    print(confusion_matrix(y_test, y_pred))


    # 6. モデル保存
    MODEL_FAQ_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_FAQ_PATH)
    print(f"saved: model: {MODEL_FAQ_PATH}")

    # 日本語読込できているか確認
    vec = pipeline.named_steps["tfidf"]
    X_train_vec = vec.transform(X_train)
    print(df["label"].value_counts())
    print("vocab size:", len(vec.vocabulary_))
    print("nonzero features:", X_train_vec.nnz)

if __name__ == "__main__":
    main()