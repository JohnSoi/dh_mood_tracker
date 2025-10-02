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
    )
}
