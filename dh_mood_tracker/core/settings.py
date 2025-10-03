import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str = "0.0.1"

    DATABASE_URL: str
    REDIS_URL: str
    SUPABASE_URL: str
    SUPABASE_TOKEN: str

    DEBUG: bool = False

    class Config:
        env_file = ".env.local" if not os.getenv("DOCKER") else ".env.dev"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()


def get_settings():
    return settings
