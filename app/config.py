"""
Configuration management using pydantic-settings.
Loads environment variables from .env file and provides typed settings.
"""
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    API_USERNAME: str
    API_PASSWORD_HASH: str
    DATABASE_URL: str = "sqlite:///./tournament_planner.db"
    
    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"  # Ignore extra fields
    )


# Global settings instance
settings = Settings()
