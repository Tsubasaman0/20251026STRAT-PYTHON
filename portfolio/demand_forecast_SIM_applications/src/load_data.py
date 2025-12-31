# load_data.py
import pandas as pd
from .config import CSV_DIR

DATA_PATH = CSV_DIR / "sim_applications.csv"

def load_daily_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"CSV not found: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    return df