import numpy as np
import pandas as pd
from src.config import SIM_APPLICATIONS_DAILY_CSV

pd.set_option("display.max_rows", 100)
pd.set_option("display.min_rows", 100)
pd.set_option("display.max_columns", 100)


def make_sim_applecations_csv(
        start="2020-01-01",
        end="2024-12-31",
        base=50,
        noise_std=8,
        trend_per_day=0.03,
        seed=42,
        out_csv_path=SIM_APPLICATIONS_DAILY_CSV,
):
    """
    日別の申込件数(applications)を月効果、曜日効果で増減させて作る。
    - base: 平均の土台
    - noise_std: ばらつき具合
    """

    rng =  np.random.default_rng(seed)

    # 1) 日付レンジ
    df = pd.DataFrame({"date": pd.date_range(start=start, end=end, freq="D")})
    df["date"] = pd.to_datetime(df["date"])

    # 2 ) 月と曜日を特徴量として作る
    df["month"] = df["date"].dt.month # 1~12月
    df["weekday"] = df["date"].dt.weekday # 0(月) ~ 6(日)
    df["year"] = df["date"].dt.year

    # 3 ) 月ごとの増減 例: 新生活、年度末(3)、 年末年始セール(12,1)は増える、夏(8)は落ちる等
    month_effect = {
        1: +12,  2: +30,  3: +50, 4: +10,
        5: +2,  6:  -30,  7: -20, 8: -13,
        9: +3, 10: +12, 11: +6, 12: +18
    }

    # 4) 曜日ごとの増減（例：土日は増える、平日は普通、など）
    weekday_effect = {
        0:  3,   # 月
        1:  0,   # 火
        2:  0,   # 水
        3:  0,   # 木
        4:  2,   # 金
        5:  15,   # 土
        6:  20   # 日
    }

    # 5) 効果を列に足し合わせる
    df["month_effect"] = df["month"].map(month_effect)
    df["weekday_effect"] = df["weekday"].map(weekday_effect)

    # 6) トレンド(時間が進むほどに増える)
    df["t"] = (df["date"] - df["date"].min()).dt.days
    df["trend_effect"] = df["t"] * trend_per_day

    # 7) 年ごとのズレ(年によって全体が少し上下する)
    year_effect = {
        2022: -3,
        2023: 0,
        2024: +4
    }

    df["year_effect"] = df["year"].map(year_effect).fillna(0)

    # 8) ノイズ
    noise = rng.normal(0, noise_std, size=len(df))

    # 9) applications
    df["applications"] = (
        base
        + df["month_effect"]
        + df["weekday_effect"]
        + df["trend_effect"]
        + df["year_effect"]
        + noise     
    ).round().astype(int)
    
    # 0未満が出ないように最低0に収める
    df["applications"] = df["applications"].clip(lower=0)

    # 保存
    out_csv_path.parent.mkdir(parents=True, exist_ok=True)
    out_df = df[["date", "applications", "year", "month", "weekday"]]
    out_df.to_csv(out_csv_path, index=False, encoding="utf-8")
    print("saved: ", out_csv_path)
    
    return out_df

if __name__ == "__main__":
    df = make_sim_applecations_csv()
    print(df.head(3))
    print(df.tail(3))