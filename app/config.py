"""Configuration management using Pydantic settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Telegram Bot Configuration
    telegram_bot_token: str
    telegram_webhook_url: str = ""
    telegram_secret_token: str = ""

    # LLM Configuration
    llm_api_key: str = ""
    llm_api_base: str = "https://openrouter.ai/api/v1"
    llm_model: str = "openai/gpt-3.5-turbo"

    # n8n Event Logging
    n8n_webhook_url: str = ""

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# Global settings instance
settings = Settings()


