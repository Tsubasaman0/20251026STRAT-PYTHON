# config.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
CSV_DIR = BASE_DIR / "data" / "csv"
SRC_DIR = BASE_DIR / "src"
MODELS_DIR = BASE_DIR / "models"

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