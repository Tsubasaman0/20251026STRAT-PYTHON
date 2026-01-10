# load_data.py
import pandas as pd
from .config import SIM_APPLICATIONS_DAILY_CSV

def load_daily_data() -> pd.DataFrame:
    if not SIM_APPLICATIONS_DAILY_CSV.exists():
        raise FileNotFoundError(f"CSV not found: {SIM_APPLICATIONS_DAILY_CSV}")
    df = pd.read_csv(SIM_APPLICATIONS_DAILY_CSV)
    df["date"] = pd.to_datetime(df["date"])
    return df