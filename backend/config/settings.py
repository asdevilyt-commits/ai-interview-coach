import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    """
    Enterprise Career AI Platform Configuration Settings.
    Loads environment variables with default fallbacks.
    """
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    APP_NAME: str = "Enterprise AI Career Preparation Platform"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # LLM Settings
    GROQ_API_KEY: str = ""
    OPENAI_API_KEY: Optional[str] = None
    PRIMARY_LLM_MODEL: str = "llama-3.1-8b-instant"
    FALLBACK_LLM_MODEL: str = "llama3-8b-8192"
    LLM_TEMPERATURE: float = 0.0
    LLM_MAX_TOKENS: int = 4096

    # Structured Memory / PostgreSQL
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "career_ai_user"
    POSTGRES_PASSWORD: str = "career_ai_pass"
    POSTGRES_DB: str = "career_ai_db"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Conversation Memory / Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0

    @property
    def REDIS_URL(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # Vector Memory
    VECTOR_DB_TYPE: str = "faiss"  # Options: faiss, pgvector
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    VECTOR_DIMENSION: int = 384

    # Security
    JWT_SECRET_KEY: str = "enterprise_career_ai_super_secret_jwt_key_change_in_prod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day


settings = Settings()
