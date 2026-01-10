# features.py
import pandas as pd
import numpy as np

def make_monthly_features(df_daily: pd.DataFrame) -> pd.DataFrame:
    # 月次集計
    monthly = (
        df_daily
        .set_index("date")
        .resample("ME")["applications"]
        .sum()
        .to_frame()
    )

    # 3ヶ月平均追加
    monthly["ma3"] = (
    monthly["applications"]
    .shift(1)
    .rolling(3)
    .mean()
    )
    
    # 前3ヶ月分集計を追加
    for n in range(1, 4):
        monthly[f"prev_{n}"] = monthly["applications"].shift(n)

    # 時間、季節の特徴量を追加
    monthly["month"] = monthly.index.month
    monthly["trend"] = range(len(monthly))
    
    monthly["month_sin"] = np.sin(2 * np.pi * monthly["month"] / 12)
    monthly["month_cos"] = np.cos(2 * np.pi * monthly["month"] / 12)
    
    return monthly