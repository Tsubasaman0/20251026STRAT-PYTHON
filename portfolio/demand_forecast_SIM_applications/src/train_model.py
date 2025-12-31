# train_model.py
import pandas as pd
from sklearn.linear_model import LinearRegression
from pathlib import Path
import joblib
from src.load_data import load_daily_data
from src.features import make_monthly_features
from src.config import MODELS_DIR, get_model_path
from src.model_registry import MODEL_NAME, MODEL_VERSION, FEATURES


def train_model(df_daily: pd.DataFrame):
    df = make_monthly_features(df_daily).dropna()

    X = df[FEATURES]
    y = df["applications"]

    model = LinearRegression()
    model.fit(X, y)
    return model, df

def save_model(model) -> None:
    model_path = get_model_path(MODEL_NAME, MODEL_VERSION)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    print("saved: ", model_path)

def main():
    df_daily = load_daily_data()
    model, _ = train_model(df_daily)
    save_model(model)


if __name__ == "__main__":
    main()