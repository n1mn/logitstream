from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str
    app_version: str
    environment: str
    debug: bool
    database_url: str

    kafka_bootstrap_servers: str

    redis_url: str
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )
settings = Settings()