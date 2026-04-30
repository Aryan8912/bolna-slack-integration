
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Slack
    slack_webhook_url: str

    # Bolna (used by scripts/trigger_call.py to initiate calls)
    bolna_api_key: str = ""
    bolna_agent_id: str = ""
    bolna_base_url: str = "https://api.bolna.ai"

    # App
    app_env: str = "development"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


# Single shared instance imported everywhere
settings = Settings()