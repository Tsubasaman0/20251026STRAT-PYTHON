# src/evaluate_model.py
import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error
from math import sqrt

from src.load_data import load_daily_data
from src.features import make_monthly_features
from src.config import get_model_path
from src.model_registry import MODEL_NAME, MODEL_VERSION, FEATURES

def evaluate():
    # 1. データ準備
    df_daily = load_daily_data()
    df_feat = make_monthly_features(df_daily).dropna()

    X = df_feat[FEATURES]
    y_true = df_feat["applications"]

    # 2. モデル読み込み
    model_path = get_model_path(MODEL_NAME, MODEL_VERSION)
    model = joblib.load(model_path)

    # 3. 予測
    y_pred = model.predict(X)

    # 4. 評価
    mae = mean_absolute_error(y_true, y_pred)
    rmse = sqrt(mean_squared_error(y_true, y_pred))

    print(mae, rmse)

    print(f"MAE: {mae:.1f}")
    print(f"RMSE: {rmse:.1f}")

    return mae, rmse

if __name__ == "__main__":
    evaluate()