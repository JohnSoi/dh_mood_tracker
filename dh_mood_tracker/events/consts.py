"""Константы пакета событий"""

__author__: str = "Digital Horizons"

from enum import StrEnum


class EventNames(StrEnum):
    """
    Название событий приложения

    :cvar SB_USER_CREATED: создание пользователя в SupaBase
    """

    SB_USER_CREATED = "supabase_user_created"
