import os


class Settings:
    APP_NAME = os.getenv("APP_NAME", "LearnMate AI")
    APP_ENV = os.getenv("APP_ENV", "development")
    API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")


settings = Settings()
