from dh_mood_tracker.core import (
    BaseExistEntityError,
    BaseNotAuthAppException,
    BaseNotFoundAppException,
    BaseBadRequestAppException,
)


class UserNotFoundByLogin(BaseNotFoundAppException):
    def __init__(self, login: str) -> None:
        super().__init__(f'Не найден пользователь по логину "{login}"')


class UserExistByLogin(BaseExistEntityError):
    _DETAIL: str = "Пользователь с таким логином уже существует"


class UserExistByEmail(BaseExistEntityError):
    _DETAIL: str = "Пользователь с таким Email`ом существует"


class IncorrectEmail(BaseBadRequestAppException):
    _DETAIL: str = "Неверный адрес электронной почты"


class NotValidAccessToken(BaseNotAuthAppException):
    _DETAIL: str = "Нет активного токена доступа"


class NotValidUserData(BaseNotAuthAppException):
    _DETAIL: str = "Нет данных о пользователе. Обратитесь в техническую поддержку"


class EmailNotConfirmed(BaseNotAuthAppException):
    _DETAIL: str = "Для доступа в систему подтвердите адрес электронной почты"
