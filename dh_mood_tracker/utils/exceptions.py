"""Модуль исключений вспомогательных функций"""

__author__: str = "Digital Horizons"

from fastapi import status

from dh_mood_tracker.core import BaseAppException


class TooManySupaBaseRequest(BaseAppException):
    """Исключение большого количества запросов к SupaBase"""

    _CODE: int = status.HTTP_429_TOO_MANY_REQUESTS
    _DETAIL: str = "Превышен лимит запросов к SupaBase"
