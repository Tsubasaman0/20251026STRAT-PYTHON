# config.py
from pathlib import Path

# === ディレクトリパス名 ===
BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
CSV_DIR = BASE_DIR / "data" / "csv"
SRC_DIR = BASE_DIR / "src"
MODELS_DIR = BASE_DIR / "models"

# === 元データ(CSVの)名 ===
SIM_APPLICATIONS_DAILY_CSV = CSV_DIR / "sim_applications.csv"
SIM_APPLICATIONS_MONTHLY_CSV = CSV_DIR / "sim_applications_monthly.csv" # 将来拡張用


# === モデルのバージョン、ディレクトリ名 ===
DEFAULT_MODEL_VERSION = "v1"

def get_model_path(model_name: str, version: str) -> Path:

    if version is None:
        version = DEFAULT_MODEL_VERSION
    return (
        MODELS_DIR
        / "artifacts"
        / model_name
        / version
        / "moddel.joblib"
    )