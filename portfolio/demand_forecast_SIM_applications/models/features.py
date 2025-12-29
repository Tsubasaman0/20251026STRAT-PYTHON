# features.py
import pandas as pd

def make_monthly_features(df_daily: pd.DataFrame) -> pd.DataFrame:
    df = df_daily.copy()
    df["date"] = pd.to_datetime(df["date"])

    # 月次集計
    monthly = (
        df
        .set_index("date")
        .resample("M")["applications"]
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