"""Константы пакета вспомогательных функций"""

__author__: str = "Digital Horizons"

from typing import Type

from dh_mood_tracker.core import BaseAppException

from .exceptions import TooManySupaBaseRequest
from ..users.exceptions import IncorrectEmail, EmailNotConfirmed

# Паттерн для валидации электронной почты
EMAIL_PATTERN: str = r"^(?!\.)(?!.*\.\.)([A-Za-z0-9\._%+-]+)@([A-Za-z0-9.-]+\.[A-Za-z]{2,})$"

# Карта исключений из SupaBase
EXCEPTION_MESSAGE_MAP: dict[str, Type[BaseAppException]] = {
    r"^Email address \"(.*)\" is invalid": IncorrectEmail,
    r"For security purposes, you can only request this after (.*) seconds.": TooManySupaBaseRequest,
    r"Email not confirmed": EmailNotConfirmed,
}
