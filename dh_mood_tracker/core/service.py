"""Модуль базового сервиса"""

__author__: str = "Digital Horizons"

from typing import Any, Type, Generic, TypeVar

from pydantic import BaseModel as BaseSchema
from sqlalchemy import select

from dh_mood_tracker.db import SessionManagerType

ModelType = TypeVar("ModelType")
SchemaType = TypeVar("SchemaType", bound=BaseSchema)


class BaseService(Generic[ModelType, SchemaType]):
    """
    Базовый сервис, реализующий CRUD операции и базовые обработчики
    Запрещается использовать напрямую, предназначен только для наследования

    :cvar _MODEL: класс модели сущности
    :type _MODEL: Type[ModelType]
    :ivar session_db: менеджер сессий подключения к БД
    :type session_db: SessionManagerType

    .. code-block:: python
        from dh_mood_tracker.core.service import BaseService

        from .model import User as UserModel
        from .schemas import CreateItemSchema


        class UserService(BaseService[UserModel, CreateItemSchema]):
            _MODEL: UserModel = UserModel


        def get_user_service(session_db: SessionManagerType = Depends(get_db_session)) -> UserService:
            return UserService(session_db)

    """

    _MODEL: Type[ModelType]

    def __init__(self, session_db: SessionManagerType) -> None:
        """
        Инициализация сервиса

        :param session_db: менеджер сессий подключения к БД
        :type session_db: SessionManagerType
        """
        self.session_db: SessionManagerType = session_db

    async def scalar_or_none(self, **filters: Any) -> ModelType | None:
        """
        Получить запись по фильтрам или None, если не найдена

        :param filters: фильтры для запроса сущности
        :type filters: Any
        :return: модель или None
        :rtype: ModelType | None

        .. code-block:: python

            async def read_by_login(self, login: str) -> UserModel | None:
                return await UserService.scalar_or_none(login=login)
        """
        async with self.session_db as session:
            result = await session.scalar(select(self._MODEL).filter_by(**filters))
            await session.close()

        return result
