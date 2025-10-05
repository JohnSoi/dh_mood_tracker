from fastapi import HTTPException, status


class BaseAppException(HTTPException):
    _CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    _DETAIL: str = "Внутренняя ошибка сервера"

    def __init__(self, detail: str | None = None) -> None:
        super().__init__(status_code=self._CODE, detail=detail or self._DETAIL)


class BaseNotFoundAppException(BaseAppException):
    _CODE: int = status.HTTP_404_NOT_FOUND


class BaseNotAuthAppException(BaseAppException):
    _CODE: int = status.HTTP_401_UNAUTHORIZED


class BaseExistEntityError(BaseNotFoundAppException):
    _CODE: int = status.HTTP_409_CONFLICT


class BaseBadRequestAppException(BaseAppException):
    _CODE: int = status.HTTP_400_BAD_REQUEST
