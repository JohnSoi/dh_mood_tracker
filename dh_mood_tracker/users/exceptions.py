"""Модуль исключений при работе с пользователями"""

__author__: str = "Digital Horizons"

from dh_mood_tracker.core import (
    BaseExistEntityError,
    BaseNotAuthAppException,
    BaseNotFoundAppException,
    BaseBadRequestAppException,
)


class UserNotFoundByLogin(BaseNotFoundAppException):
    """Исключение при отсутствии пользователя при поиске по логину"""

    def __init__(self, login: str) -> None:
        super().__init__(f'Не найден пользователь по логину "{login}"')


class UserExistByLogin(BaseExistEntityError):
    """Исключение при создании, что данный логин уже используется"""

    _DETAIL: str = "Пользователь с таким логином уже существует"


class UserExistByEmail(BaseExistEntityError):
    """Исключение при создании, что данный адрес электронной почты уже используется"""

    _DETAIL: str = "Пользователь с таким Email`ом существует"


class IncorrectEmail(BaseBadRequestAppException):
    """Исключение при неправильном адресе электронной почты"""

    _DETAIL: str = "Неверный адрес электронной почты"


class NotValidAccessToken(BaseNotAuthAppException):
    """Исключение при отсутствии токена доступа"""

    _DETAIL: str = "Нет активного токена доступа"


class NotValidUserData(BaseNotAuthAppException):
    """Исключение при отсутствии локального пользователя по токену доступа"""

    _DETAIL: str = "Нет данных о пользователе. Обратитесь в техническую поддержку"


class EmailNotConfirmed(BaseNotAuthAppException):
    """Исключение при попытке входа с неподтвержденным адресом электронной почты"""

    _DETAIL: str = "Для доступа в систему подтвердите адрес электронной почты"
