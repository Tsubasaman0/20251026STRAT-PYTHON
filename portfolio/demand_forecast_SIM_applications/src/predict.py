# predict.py
import pandas as pd
import joblib
from pathlib import Path
from src.features import make_monthly_features
from src.config import MODELS_DIR, get_model_path
from src.load_data import load_daily_data
from src.model_registry import MODEL_NAME, MODEL_VERSION, FEATURES

def load_model():
    model_path = get_model_path(MODEL_NAME, MODEL_VERSION)
    return joblib.load(model_path)

def predict_next_month() -> int:
    # 1. データ読み込み
    df_daily = load_daily_data()

    # 2. 月次特徴量作成
    df_feat = make_monthly_features(df_daily)

    # 3. 最新1行(来月予測の入力)
    X_last = df_feat[FEATURES].tail(1)

    # 4 .モデル読み込み
    model = load_model()

    # 5. 予測
    y_pred = model.predict(X_last)

    return int(round(y_pred[0]))

def main():
    pred = predict_next_month()
    print(f"来月のSIM申込件数予測: {pred}")
    
if __name__ == "__main__":
    main()