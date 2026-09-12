import os
from typing import List

from dotenv import load_dotenv

load_dotenv()


def _parse_origins(value: str) -> List[str]:
    return [origin.strip() for origin in value.split(",") if origin.strip()]


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "LearnMate AI")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    API_V1_PREFIX: str = os.getenv("API_V1_PREFIX", "/api/v1")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:99aa88bb@localhost:5432/learnmate"
    )
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    CORS_ORIGINS: List[str] = _parse_origins(
        os.getenv("CORS_ORIGINS", "http://localhost:5173")
    )
    AUTO_CREATE_TABLES: bool = os.getenv("AUTO_CREATE_TABLES", "true").lower() == "true"

    def validate(self) -> None:
        if self.APP_ENV.lower() == "production" and (
            not self.SECRET_KEY or len(self.SECRET_KEY) < 32
        ):
            raise RuntimeError("SECRET_KEY must be set to a strong value in production.")
        if not self.SECRET_KEY:
            self.SECRET_KEY = "development-only-change-me-learnmate"

settings = Settings()
settings.validate()
