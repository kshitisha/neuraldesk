from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """
    all config comes from environment variables.
    Pydantic validates types at startup — if a required var is missing,
    the app crashes immediately with a clear error instead of failing
    silently at runtime.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    APP_NAME: str = "NeuralDesk"
    APP_ENV: str = "development"
    DEBUG: bool = False

    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379"

    SECRET_KEY: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    OPENAI_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    GROQ_API_KEY: str = ""

    DEFAULT_PROVIDER: str = "openai"

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"


@lru_cache
def get_settings() -> Settings:
    """
    Cached singleton — settings object is created once and reused.
    lru_cache means we never re-read the .env file on every request.
    """
    return Settings()


settings = get_settings()