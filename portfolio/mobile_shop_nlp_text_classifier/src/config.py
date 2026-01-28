# config.py
from pathlib import Path

# === ディレクトリパス ===
BASE_DIR = Path(__file__).resolve().parents[1] # ルートディレクトリ

DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "model"

MODEL_FAQ_DIR = MODEL_DIR / "faq_classifier"


# === ファイルパス ====
FAQ_CSV_PATH = DATA_DIR / "raw" / "faq.csv"
MODEL_FAQ_PATH = MODEL_FAQ_DIR / "model.joblib"