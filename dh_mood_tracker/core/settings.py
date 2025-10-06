# pylint: disable=too-few-public-methods
"""Модуль настроек приложения"""

__author__: str = "Digital Horizons"

import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Класс с настройками приложения

    :cvar APP_NAME: название приложения
    :type APP_NAME: str
    :cvar APP_VERSION: версия приложения
    :type APP_VERSION: str
    :cvar DATABASE_URL: адрес подключения к БД
    :type DATABASE_URL: str
    :cvar REDIS_URL: адрес подключения к Redis
    :type REDIS_URL: str
    :cvar SUPABASE_URL: адрес для подключения к SupaBase
    :type SUPABASE_URL: str
    :cvar SUPABASE_TOKEN: токен доступа к SupaBase
    :type SUPABASE_TOKEN: str
    :cvar DEBUG: режим отладки
    :type DEBUG: bool
    """

    APP_NAME: str = "Base App"
    APP_VERSION: str = "0.0.1"

    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/db_name"
    REDIS_URL: str = "redis://localhost:6379"
    SUPABASE_URL: str = "http://localhost:8000"
    SUPABASE_TOKEN: str = "<TOKEN>"

    DEBUG: bool = False

    class Config:
        """Конфигуратор работы класса"""

        env_file = ".env.local" if not os.getenv("DOCKER") else ".env.dev"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Глобальный инстанс настроек приложения
settings: Settings = Settings()
