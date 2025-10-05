"""Модуль для работы с SupaBase"""

__author__: str = "Digital Horizons"

import re
from uuid import UUID
from typing import Any, NoReturn

from fastapi import Depends, Response
from supabase import Client, create_client
from supabase_auth import Session, AuthResponse
from supabase_auth.errors import AuthApiError
from sqlalchemy.ext.asyncio import AsyncSession

from dh_mood_tracker.db import get_db_session
from dh_mood_tracker.core import settings, BaseAppException
from dh_mood_tracker.events import SupaBaseUserCreate

from .consts import EXCEPTION_MESSAGE_MAP
from .event_bus import EventBus, get_event_bus


class SupaBase:
    """
    Класс для взаимодействия с сервисом SupaBase. Является фасадом для взаимодействия.

    !!! Важно - использовать только через зависимость как в примере

    :ivar _client: клиент подключения к Supabase
    :type _client: SupaBase
    :ivar _event_bus: шина событий приложений
    :type _event_bus: SupaBase
    """

    def __init__(self, session_db: AsyncSession) -> None:
        """
        Инициализация фасада для работы с SupaBase

        :param session_db: сессия для подключения к БД
        :type session_db: AsyncSession
        """
        self._client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_TOKEN)
        self._event_bus: EventBus = get_event_bus(session_db)

    async def create_user(self, email: str, password: str, other_data: dict[str, Any]) -> bool:
        """
        Создание пользователя в SupaBase.
        Отправляет событие SupaBaseUserCreate после создания с UUID пользователя в SupaBase и other_data

        !!! Важно - нет проверки на наличия пользователя в БД. Нужно выполнить вручную

        :param email: почта пользователя
        :type email: str
        :param password: пароль пользователя
        :type password: str
        :param other_data: дополнительные данные для создания локального пользователя
        :type other_data: dict[str, Any]
        :return: признак создания пользователя
        :rtype: bool

        :event SupaBaseUserCreate: событие создания пользователя в SupaBase с UUID пользователя в SupaBase и other_data

        :exception IncorrectEmail: передан некорректный email
        :exception TooManySupaBaseRequest: слишком много запросов к SupaBase
        :exception BaseAppException: неопределенная ошибка

        .. code-block:: python
            from dh_mood_tracker.utils import SupaBase, get_supabase


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

                if await user_service.read_by_login(user_data.login):
                    raise UserExistByLogin()

                await supabase.create_user(user_data.email, user_data.password, user_data.model_dump())
        """
        try:
            supabase_data: AuthResponse = self._client.auth.sign_up(
                {
                    "email": email,
                    "password": password,
                    "options": {
                        "email_redirect_to": "http://localhost:8000/email_confirm",
                    },
                }
            )
        except AuthApiError as ex:
            self._exception_adapter(ex)

        await self._event_bus.publish(SupaBaseUserCreate(UUID(supabase_data.user.id), other_data))

        return True

    def login(self, email: str, password: str, response: Response) -> bool:
        """
        Аутентификация пользователя по электронной почте и паролю через SupaBase

        :param email: адрес электронной почты пользователя
        :type email: str
        :param password: пароль, введенный пользователем
        :type password: str
        :param response: экземпляр ответа
        :type response: Response
        :return: успешность аутентификации
        :rtype: bool

        :exception IncorrectEmail: передан некорректный email
        :exception EmailNotConfirmed: адрес электронной почты не подтвержден
        :exception TooManySupaBaseRequest: слишком много запросов к SupaBase
        :exception BaseAppException: неопределенная ошибка

        .. code-block:: python
            from dh_mood_tracker.utils import SupaBase, get_supabase


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
        try:
            auth_data: AuthResponse = self._client.auth.sign_in_with_password({"email": email, "password": password})
            response.set_cookie("AccessToken", auth_data.session.access_token)
            response.set_cookie("RefreshToken", auth_data.session.refresh_token)
            return True
        except AuthApiError as ex:
            self._exception_adapter(ex)

    def confirm_email(self, access_token: str) -> bool:
        """
        Подтверждение почты по токену

        :param access_token: токен подтверждения доступа
        :type access_token: str
        :return: успешность подтверждения
        :rtype: bool

        .. code-block:: python
            from dh_mood_tracker.utils import SupaBase, get_supabase

            @user_routes.get("/email_confirm", description="Подтверждения адрес электронной почты")
            def email_confirm(access_token: str, supabase: SupaBase = Depends(get_supabase)) -> bool:
                supabase.confirm_email(access_token)

                return True
        """
        self._client.auth.verify_otp(
            {
                "type": "email",
                "token_hash": access_token,
            }
        )

        return True

    def get_session_data(self) -> Session:
        """
        Получение данных сессии текущего пользователя

        :return: данные сессии
        :rtype: Session

        .. code-block:: python
            from uuid import UUID
            from supabase_auth import Session
            from dh_mood_tracker.utils import SupaBase, get_supabase

            async def get_user_supabase_uuid(supabase: SupaBase = Depends(get_supabase)) -> UUID:
                supabase_data: Session = supabase.get_session_data()
                user_supabase_id: UUID = UUID(supabase_data.user.id) # UUID пользователя из SupaBase

                return user_supabase_id
        """
        return self._client.auth.get_session()

    def set_access_token(self, access_token: str, refresh_token: str) -> None:
        """
        Установка данных сессии пользователя в SupaBase

        :param access_token: токен доступа
        :type access_token: str
        :param refresh_token: токен обновления
        :type refresh_token: str

        .. code-block:: python
            from dh_mood_tracker.utils import SupaBase, get_supabase

            async def set_user_token(supabase: SupaBase = Depends(get_supabase)) -> None:
                if not access_token or not refresh_token:
                    raise NotValidAccessToken()

                supabase.set_access_token(access_token, refresh_token)
        """
        return self._client.auth.set_session(access_token, refresh_token)

    @staticmethod
    def _exception_adapter(exception: Exception) -> NoReturn:
        """
        Адаптер для исключений при взаимодействии с SupaBase

        :param exception: исключение из SupaBase
        :type exception: Exception
        """
        for pattern, exception_class in EXCEPTION_MESSAGE_MAP.items():
            if bool(re.match(pattern, str(exception))):
                raise exception_class

        raise BaseAppException()


def get_supabase(session_db: AsyncSession = Depends(get_db_session)) -> SupaBase:
    """
    Метод для получения экземпляра SupaBase.

    !!! Важно - использовать через Depends и все взаимодействие с SupaBase начинается через данный метод

    :param session_db: сессия подключения к БД
    :type session_db: AsyncSession
    :return: экземпляр SupaBase
    :rtype: SupaBase

    .. code-block:: python
        from dh_mood_tracker.utils import SupaBase, get_supabase

        async def set_user_token(supabase: SupaBase = Depends(get_supabase)) -> None:
            supabase.set_access_token(access_token, refresh_token)
    """
    return SupaBase(session_db)
