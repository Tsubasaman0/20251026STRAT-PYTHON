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

def sudachi_tokenize(text):
    return [m.surface() for m in tokenizer_obj.tokenize(text, mode)]

def build_char_pipeline():
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            analyzer="char",
            ngram_range=(2, 5),
            min_df=1
        )),
        ("clf", LogisticRegression(
            max_iter=2000,
            class_weight="balanced"
        )),
    ])

def build_sudachi_pipeline():
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            tokenizer=sudachi_tokenize,
            token_pattern=None,
            ngram_range=(1, 2),
            min_df=1
        )),
        ("clf", LogisticRegression(
            max_iter=2000,
            class_weight="balanced"
        ))
    ])

def evaluate_one(name, pipeline, X_train, X_test, y_train, y_test):
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    print(f"\n===== {name} =====")
    print("=== classification report ===")
    print(classification_report(y_test, y_pred))
    print("=== confusion metrix ===")
    print(confusion_matrix(y_test, y_pred))

    return pipeline

def main():
    # 1. データ読み込み
    df = pd.read_csv(FAQ_CSV_PATH)

    X = df["text"].astype(str)
    y = df["label"].astype(str)
    print("label counts:")
    print(y.value_counts())

    # 2. train / test 分割
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.3,
        random_state=42,
        stratify=y
    )

    # 3. パイプラインモデル
    char_pipe = build_char_pipeline()
    sudachi_pipe = build_sudachi_pipeline()

    char_pipe = evaluate_one("CHAR N-GRAM", char_pipe, X_train, X_test, y_train, y_test)
    sudachi_pipe = evaluate_one("SUDACHI TOKEN", sudachi_pipe, X_train, X_test, y_train, y_test)

    best = char_pipe

    # 4. モデル保存
    MODEL_FAQ_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(best, MODEL_FAQ_PATH)
    print(f"\nsaved: model: {MODEL_FAQ_PATH}")

    # 日本語読込できているか確認
    vec = best.named_steps["tfidf"]
    X_train_vec = vec.transform(X_train)
    print(df["label"].value_counts())
    print("vocab size:", len(vec.vocabulary_))
    print("nonzero features:", X_train_vec.nnz)

if __name__ == "__main__":
    main()