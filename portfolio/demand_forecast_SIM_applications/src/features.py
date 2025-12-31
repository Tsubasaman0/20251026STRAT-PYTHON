# features.py
import pandas as pd
from src.load_data import load_daily_data

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
    .rolling(3)
    .mean()
    )
    
    # 前3ヶ月分集計を追加
    for n in range(1, 4):
        monthly[f"prev_{n}"] = monthly["applications"].shift(n)
    
    return monthly