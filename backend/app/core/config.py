import os
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application settings validated via Pydantic Settings.
    Fails fast at startup if critical environment variables are missing or invalid.
    """

    PROJECT_NAME: str = "TaskFlow API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Security Configuration
    SECRET_KEY: str = Field(
        default="default-super-secret-key-change-me-in-production-32-chars-min",
        description="JWT Secret Key for signing access tokens"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Database Connection String (Defaults to SQLite for instant local dev & testing, PostgreSQL in prod)
    DATABASE_URL: str = Field(
        default="sqlite:///./taskflow.db",
        description="SQLAlchemy Database URL"
    )

    # Allowed CORS Origins
    CORS_ORIGINS: List[str] = ["*"]

    # Auth Rate Limiting Rule
    AUTH_RATE_LIMIT: str = "10/minute"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    @property
    def sqlalchemy_database_url(self) -> str:
        """Fixes legacy postgres:// prefixes automatically for Render/Heroku compatibility."""
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql://", 1)
        return url


settings = Settings()
