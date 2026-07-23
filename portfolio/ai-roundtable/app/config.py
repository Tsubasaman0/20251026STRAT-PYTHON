import os
from dataclasses import dataclass

from dotenv import load_dotenv


# ローカルと本番で同じコードを使えるよう、秘密情報は環境変数だけから読む。
load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None


def get_settings() -> Settings:
    return Settings(openai_api_key=os.getenv("OPENAI_API_KEY"))
