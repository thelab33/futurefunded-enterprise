from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "FutureFunded"
    ENV: str = "development"

    WEB_HOST: str = "127.0.0.1"
    WEB_PORT: int = 5000

    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    API_BASE_URL: str = "http://127.0.0.1:8000"

    SECRET_KEY: str = "change-me"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
