"""Configuration settings for AlphaFold MCP server."""

import logging
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    # Server settings
    SERVR_NAME: str = "AlphaFoldMCP"
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8050

    # API settings
    MAX_RETIRES: int = 3
    REQUEST_TIMEOUT: int = 10

    # Cache settings
    CACHE_TTL: int = 86400  # 24 hours
    CACHE_DIR: Optional[str] = None

    # SSL/TLS settings
    SSL_CERT_FILE: Optional[str] = Field(None, env="SSL_CERT_FILE")
    SSL_KEY_FILE: Optional[str] = Field(None, env="SSL_KEY_FILE")

    # Logging
    LOG_LEVEL: str = "INFO"

    # AlphaFold API settings
    ANTHROPIC_API_KEY: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
