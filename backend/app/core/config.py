import os
from typing import List, Union
from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application settings validated via Pydantic Settings.
    Fails fast at startup if critical production configuration is missing or insecure.
    """

    PROJECT_NAME: str = "TaskFlow API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = Field(
        default="development",
        description="Runtime environment: 'development', 'staging', or 'production'"
    )

    # Security Configuration
    SECRET_KEY: str = Field(
        default="insecure-dev-secret-key-do-not-use-in-production",
        description="JWT Secret Key for signing access tokens (must be set in production)"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Database Connection String
    DATABASE_URL: str = Field(
        default="sqlite:///./taskflow.db",
        description="SQLAlchemy Database URL (SQLite for local dev, PostgreSQL for production)"
    )

    # Allowed CORS Origins (Supports comma-separated strings or JSON arrays)
    CORS_ORIGINS: Union[List[str], str] = ["*"]

    # Auth Rate Limiting Rule
    AUTH_RATE_LIMIT: str = "10/minute"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if v.strip().startswith("[") and v.strip().endswith("]"):
                import json
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        elif isinstance(v, list):
            return v
        return ["*"]

    @model_validator(mode="after")
    def validate_production_configuration(self) -> "Settings":
        """Fails fast if production environment attempts to run with insecure default secrets."""
        if self.ENVIRONMENT.lower() == "production":
            if (
                not self.SECRET_KEY
                or self.SECRET_KEY == "insecure-dev-secret-key-do-not-use-in-production"
                or len(self.SECRET_KEY) < 32
            ):
                raise ValueError(
                    "FATAL CONFIGURATION ERROR: SECRET_KEY must be explicitly set to a secure, "
                    "unique value of at least 32 characters in production."
                )
            if self.DATABASE_URL.startswith("sqlite"):
                raise ValueError(
                    "FATAL CONFIGURATION ERROR: Production environment requires a production database "
                    "(e.g., PostgreSQL). SQLite is disallowed in production."
                )
            if self.CORS_ORIGINS == ["*"]:
                import warnings
                warnings.warn(
                    "WARNING: CORS_ORIGINS is set to wildcard '*' in production. "
                    "Specify exact allowed frontend origins in production.",
                    UserWarning
                )
        return self

    @property
    def sqlalchemy_database_url(self) -> str:
        """Fixes legacy postgres:// prefixes automatically for Render/Heroku compatibility."""
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql://", 1)
        return url


settings = Settings()
