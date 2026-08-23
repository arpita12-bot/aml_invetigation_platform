"""
==========================================================
AML Investigation Platform

Configuration Management

Responsibilities
----------------
✓ Load environment variables
✓ Validate application settings
✓ Expose a singleton settings object
✓ Central configuration for all modules
==========================================================
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Backend root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """
    Global Application Configuration
    """

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ==========================================================
    # APPLICATION
    # ==========================================================
    APP_NAME: str = Field(default="AML Investigation Platform")
    APP_VERSION: str = Field(default="1.0.0")
    APP_ENV: str = Field(default="development")
    DEBUG: bool = Field(default=True)

    # ==========================================================
    # FASTAPI
    # ==========================================================
    HOST: str
    PORT: int

    API_PREFIX: str

    # ==========================================================
    # POSTGRESQL
    # ==========================================================
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # ==========================================================
    # NEO4J
    # ==========================================================
    NEO4J_URI: str
    NEO4J_USERNAME: str
    NEO4J_PASSWORD: str

    NEO4J_DATABASE: str = "neo4j"
    NEO4J_MAX_CONNECTION_POOL_SIZE: int = 50
    NEO4J_CONNECTION_TIMEOUT: int = 30

    # ==========================================================
    # FILE UPLOAD
    # ==========================================================
    UPLOAD_DIRECTORY: str
    MAX_UPLOAD_SIZE_MB: int
    ALLOWED_EXTENSIONS: str

    # ==========================================================
    # VALIDATION
    # ==========================================================
    MAX_COLUMN_NAME_LENGTH: int
    MAX_TABLE_NAME_LENGTH: int

    REMOVE_DUPLICATES: bool
    REMOVE_EMPTY_ROWS: bool
    TRIM_WHITESPACES: bool
    NORMALIZE_COLUMN_NAMES: bool
    AUTO_INFER_DATATYPES: bool

    # ==========================================================
    # DATA PROFILING
    # ==========================================================
    ENABLE_DATA_PROFILING: bool
    PROFILE_SAMPLE_ROWS: int

    # ==========================================================
    # DUPLICATE DETECTION
    # ==========================================================
    ENABLE_FILE_HASH_CHECK: bool
    ENABLE_ROW_HASH_CHECK: bool
    ENABLE_INCREMENTAL_LOADING: bool

    # ==========================================================
    # LOGGING
    # ==========================================================
    LOG_DIRECTORY: str
    LOG_LEVEL: str

    # ==========================================================
    # GRAPH
    # ==========================================================
    BUILD_GRAPH_AFTER_UPLOAD: bool

    # ==========================================================
    # MACHINE LEARNING
    # ==========================================================
    TRAIN_TRANSE_AFTER_UPLOAD: bool
    TRAIN_ROTATE_AFTER_UPLOAD: bool
    TRAIN_GAT_AFTER_UPLOAD: bool
    
    # ==========================================================
    # JWT AUTHENTICATION
    # ==========================================================
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    @property
    def postgres_url(self) -> str:
        """
        SQLAlchemy PostgreSQL connection string
        """
        return (
            f"postgresql+psycopg2://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    @property
    def upload_path(self) -> Path:
        """
        Upload directory
        """
        path = BASE_DIR / self.UPLOAD_DIRECTORY
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def log_path(self) -> Path:
        """
        Log directory
        """
        path = BASE_DIR / self.LOG_DIRECTORY
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def allowed_extensions(self) -> list[str]:
        """
        Allowed upload extensions
        """
        return [
            ext.strip().lower()
            for ext in self.ALLOWED_EXTENSIONS.split(",")
        ]


@lru_cache
def get_settings() -> Settings:
    """
    Singleton configuration instance
    """
    return Settings()


settings = get_settings()