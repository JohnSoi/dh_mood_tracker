"""Константы пакета вспомогательных функций"""

__author__: str = "Digital Horizons"

from fastapi import status

# Паттерн для валидации электронной почты
EMAIL_PATTERN: str = r"^(?!\.)(?!.*\.\.)([A-Za-z0-9\._%+-]+)@([A-Za-z0-9.-]+\.[A-Za-z]{2,})$"

# Карта исключений из SupaBase
EXCEPTION_MESSAGE_MAP: dict[str, tuple[str, int]] = {
    r"^Email address \"(.*)\" is invalid": (
        "Некорректный Email",
        status.HTTP_400_BAD_REQUEST,
    ),
    r"For security purposes, you can only request this after (.*) seconds.": (
        "Превышен лимит запросов к SupaBase",
        status.HTTP_429_TOO_MANY_REQUESTS
    ),
    r"Email not confirmed": (
        "Подтвердите email",
        status.HTTP_401_UNAUTHORIZED,
    )
}
