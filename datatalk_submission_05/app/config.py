"""Service settings, read from environment variables (prefix LEAD_) or a .env file."""
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LEAD_", env_file=".env", extra="ignore")

    model_path: Path = MODELS_DIR / "model_C_0.001.bin"
    threshold: float = 0.5
    max_batch_size: int = 1000


settings = Settings()
