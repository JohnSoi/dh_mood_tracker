"""Модуль сервиса пользователя"""

__author__: str = "Digital Horizons"

import uuid
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dh_mood_tracker.db import get_db_session
from dh_mood_tracker.core import BaseService
from dh_mood_tracker.events.supabase import SupaBaseUserCreate

from .model import User as UserModel
from .schemas import CreateItemSchema


class UserService(BaseService[UserModel, CreateItemSchema]):
    """Модуль сервиса пользователя"""

    _MODEL = UserModel

    async def read_by_login(self, login: str) -> UserModel | None:
        """
        Чтение пользователя по логину

        :param login: логин пользователя
        :type login: str
        :return: данные пользователя или None - если не найден

        .. code-block:: python
            from dh_mood_tracker.utils import SupaBase, get_supabase
            from dh_mood_tracker.users import UserService, get_user_service

            @auth_routes.post("/login", description="Аутентификация пользователя")
            async def user_login(
                response: Response,
                login_data: UserLogin,
                user_service: UserService = Depends(get_user_service),
                supabase: SupaBase = Depends(get_supabase),
            ) -> bool:
                if not (user_data := await user_service.read_by_login(login_data.login)):
                    raise UserNotFoundByLogin(login_data.login)

                return supabase.login(user_data.email, login_data.password, response)
        """
        return await self.scalar_or_none(login=login)

    async def read_by_email(self, email: str) -> UserModel | None:
        """
        Чтение пользователя по адресу электронной почты

        :param email: адрес электронной почты
        :type email: str
        :return: данные пользователя или None - если не найден

        .. code-block:: python
            from dh_mood_tracker.utils import SupaBase, get_supabase, email_validator
            from dh_mood_tracker.users import UserService, get_user_service

            @auth_routes.post("/register", description="Регистрация нового пользователя")
            async def user_register(
                user_data: CreateInUserSchema,
                user_service: UserService = Depends(get_user_service),
                supabase: SupaBase = Depends(get_supabase),
            ) -> bool:
                if not email_validator(user_data.email):
                    raise IncorrectEmail()

                if await user_service.read_by_email(user_data.email):
                    raise UserExistByEmail()

                return True
        """
        return await self.scalar_or_none(email=email)

    async def read_by_supabase_id(self, supabase_id: UUID) -> UserModel | None:
        """
        Чтение пользователя по UUID SupaBase

        :param supabase_id: UUID SupaBase
        :type supabase_id: UUID
        :return: данные пользователя или None - если не найден

        .. code-block:: python
            from dh_mood_tracker.utils import SupaBase, get_supabase
            from dh_mood_tracker.users import UserService, get_user_service

            async def user_by_supabase_id(
                user_service: UserService = Depends(get_user_service),
                supabase: SupaBase = Depends(get_supabase),
            ) -> UserModel:
                supabase_data: Session = supabase.get_session_data()
                user_supabase_id: UUID = UUID(supabase_data.user.id)

                user_data: UserModel = await user_service.read_by_supabase_id(user_supabase_id)

                return user_data
        """
        return await self.scalar_or_none(supabase_id=supabase_id)

    async def create_user_by_supabase(self, event: SupaBaseUserCreate) -> None:
        """
        Создание пользователя из события создания в SupaBase

        :param event: событие о создании в SupaBase
        :type event: SupaBaseUserCreate
        """
        event_data: dict = event.to_dict().get("data") or {}
        user_data: dict = event_data.get("UserData") or {}
        user_db_data: CreateItemSchema = CreateItemSchema(
            supabase_id=event_data.get("SupaBaseUuid", uuid.uuid4()),
            email=user_data.get("email", ""),
            name=user_data.get("name", ""),
            surname=user_data.get("surname", ""),
            patronymic=user_data.get("patronymic", ""),
            login=user_data.get("login", ""),
            password=user_data.get("password", ""),
        )
        await self.create(user_db_data)


def get_user_service(session_db: AsyncSession = Depends(get_db_session)) -> UserService:
    """
    Метод для зависимости работы с сервисом пользователей

    !!! Важно - нельзя использовать класс сервиса пользователей напрямую

    :param session_db: сессия подключения к БД
    :type session_db: AsyncSession
    :return: экземпляр сервиса для работы с пользователями
    :rtype: UserService

    .. code-block:: python
        from dh_mood_tracker.utils import SupaBase, get_supabase
        from dh_mood_tracker.users import UserService, get_user_service

        async def user_by_supabase_id(
            user_service: UserService = Depends(get_user_service),
            supabase: SupaBase = Depends(get_supabase),
        ) -> UserModel:
            supabase_data: Session = supabase.get_session_data()
            user_supabase_id: UUID = UUID(supabase_data.user.id)

            user_data: UserModel = await user_service.read_by_supabase_id(user_supabase_id)

            return user_data
    """
    return UserService(session_db)
