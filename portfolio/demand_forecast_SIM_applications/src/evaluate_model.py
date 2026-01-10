# src/evaluate_model.py
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from math import sqrt
from sklearn.linear_model import LinearRegression

from src.load_data import load_daily_data
from src.features import make_monthly_features
from src.model_registry import FEATURES_PLUS, FEATURES_BASIC

def _metrics(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = sqrt(mean_squared_error(y_true, y_pred))
    return mae, rmse

def evaluate(test_months: int = 3):
    df_daily = load_daily_data()
    df_feat = make_monthly_features(df_daily).dropna()

    if len(df_feat) <= test_months:
        raise ValueError("データが少なすぎます。test_months を小さくするか、期間を増やしてください。")

    train = df_feat.iloc[:-test_months]
    test = df_feat.iloc[-test_months:]

    y_test = test["applications"]

    # === ベースライン1: 先月と同じ ===
    pred_prev1 = test["prev_1"].values
    mae_b1, rmse_b1 = _metrics(y_test, pred_prev1)

    # === ベースライン2: 3ヶ月平均 ===
    pred_ma3 = test["ma3"].values
    mae_b2, rmse_b2 = _metrics(y_test, pred_ma3)

    # === モデル(BASIC特徴量) ===
    X_train_b = train[FEATURES_BASIC]
    X_test_b = test[FEATURES_BASIC]

    model_b = LinearRegression()
    model_b.fit(X_train_b, train["applications"])
    pred_model_b = model_b.predict(X_test_b)
    mae_mb, rmse_mb = _metrics(y_test, pred_model_b)

    # === モデル(PLUS特徴量) ===
    X_train_p = train[FEATURES_PLUS]
    X_test_p = test[FEATURES_PLUS]

    model_p = LinearRegression()
    model_p.fit(X_train_p, train["applications"])
    pred_model_p = model_p.predict(X_test_p)
    mae_mp, rmse_mp = _metrics(y_test, pred_model_p)

    # === 見やすい出力 ===
    y_mean = float(y_test.mean())
    y_max  = float(y_test.max())

    print(f"test_months: {test_months}")
    print("--- baseline ---")
    print(f"prev_1 MAE: {mae_b1:.1f} RMSE: {rmse_b1:.1f}")
    print(f"ma3    MAE: {mae_b2:.1f} RMSE: {rmse_b2:.1f}")

    print("--- models ---")
    print(f"MODEL(BASIC) MAE: {mae_mb:.1f} RMSE: {rmse_mb:.1f}")
    print(f"MODEL(PLUS)  MAE: {mae_mp:.1f} RMSE: {rmse_mp:.1f}")

    print("--- relative ---")
    print(f"MODEL(PLUS) MAE /  mean: {mae_mp / y_mean:.3f}")
    print(f"MODEL(PLUS) RMSE / mean: {rmse_mp / y_mean:.3f}")
    print(f"MODEL(PLUS) MAE / max: {mae_mp / y_max:.3f}")
    print(f"MODEL(PLUS) RMSE / max: {rmse_mp / y_max:.3f}")

    print("--- per month ---")
    for idx in test.index:
        t = int(test.loc[idx, "applications"])
        b1 = int(round(test.loc[idx, "prev_1"]))
        b2 = int(round(test.loc[idx, "ma3"]))
        pb = int(round(pred_model_b[list(test.index).index(idx)]))
        pp = int(round(pred_model_p[list(test.index).index(idx)]))
        print(f"{idx.date()} true={t} prev1={b1} ma3={b2} basic={pb} plus={pp}")
    
    return {
        "test_months" : test_months,
        "baseline_prev1_mae" : mae_b1,
        "baseline_prev1_rmse" : rmse_b1,
        "baseline_ma3_mae" : mae_b2,
        "baseline_ma3_rmse" : rmse_b2,
        "model_basic_mae" : mae_mb,
        "model_basic_rmse" : rmse_mb,
        "model_plus_mae" : mae_mp,
        "model_plus_rmse" : rmse_mp        
        }

def print_summary(results: list[dict]) -> None:
        """
        results = [
         {
            "test_months: " : test_months,
            "baseline_prev1_mae" : mae_b1,
            "baseline_prev1_rmse" : ...,
            ...
        },
        ...
        ]
        """
        df = pd.DataFrame(results)
        print(df)
        df = df.set_index("test_months")
        print("\n===== SUMMARY =====")
        print(df.round(1))

def print_best_model(results: list[dict]) -> None:
    df = pd.DataFrame(results).set_index("test_months")
    candidates = [
          "baseline_prev1_mae",
          "baseline_ma3_mae", 
          "model_basic_mae",
          "model_plus_mae"
          ]
    
    best = df[candidates].idxmin(axis=1)

    print("\nBest model per test window:")
    print(best)

if __name__ == "__main__":
    rows = []
    for m in [3, 6, 12]:
        rows.append(evaluate(test_months=m))
    print_summary(rows)
    print_best_model(rows)