"""Модуль базовых исключений"""

__author__: str = "Digital Horizons"

from fastapi import HTTPException, status


class BaseAppException(HTTPException):
    """
    Базовое исключение приложения

    :cvar _CODE: HTTP код исключения
    :type _CODE: int
    :cvar _DETAIL: текст сообщения об исключении
    :type _DETAIL: str
    """

    _CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    _DETAIL: str = "Внутренняя ошибка сервера"

    def __init__(self, detail: str | None = None) -> None:
        """
        Инициализация исключения

        :param detail: текст сообщения об исключении. Если не задан - берется из _DETAIL
        :type detail: str | None
        """
        super().__init__(status_code=self._CODE, detail=detail or self._DETAIL)


class BaseNotFoundAppException(BaseAppException):
    """Базовое исключение отсутствия сущности"""

    _CODE: int = status.HTTP_404_NOT_FOUND


class BaseNotAuthAppException(BaseAppException):
    """Базовое исключение отсутствия аутентификации"""

    _CODE: int = status.HTTP_401_UNAUTHORIZED


class BaseExistEntityError(BaseNotFoundAppException):
    """Базовое исключение дублирования сущности"""

    _CODE: int = status.HTTP_409_CONFLICT


class BaseBadRequestAppException(BaseAppException):
    """Базовое исключение ошибки в запросе"""

    _CODE: int = status.HTTP_400_BAD_REQUEST
