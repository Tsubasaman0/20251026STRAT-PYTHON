# train_model.py
import pandas as pd
from .features import make_monthly_features
from sklearn.linear_model import LinearRegression
from pathlib import Path
import joblib

from .features import make_monthly_features

MODEL_PATH = Path("models/artifacts/model.joblib")

def train_model(df_daily: pd.DataFrame):
    df = make_monthly_features(df_daily).dropna()

    X = df[["prev1", "prev_2", "prev_3", "ma3"]]
    y = df["applications"]

    model = LinearRegression()
    model.fit(X, y)
    return model, df

def save_model(model):
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print("saved: ", MODEL_PATH)

if __name__ == "__main__":
    from .load_data import load_daily_data # CSV読み込み これから作成