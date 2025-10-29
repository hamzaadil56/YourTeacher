"""
Configuration settings for the YourTeacher backend
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    app_name: str = "YourTeacher API"
    app_version: str = "1.0.0"
    api_prefix: str = "/api"

    # Server Configuration
    backend_port: int = 8000
    host: str = "localhost"

    # CORS Configuration
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]

    # API Keys
    gemini_api_key: str
    openai_api_key: str = ""

    # OpenAI Configuration
    openai_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"

    # Model Configuration
    default_model: str = "gemini-2.0-flash"

    # Session Configuration
    session_timeout_minutes: int = 60
    max_message_history: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = False


# Create global settings instance
settings = Settings()
