"""Модуль для зависимостей при работе с пользователями"""

__author__: str = "Digital Horizons"

from uuid import UUID

from fastapi import Depends, Request
from supabase_auth import Session

from dh_mood_tracker.utils import SupaBase, get_supabase

from .model import User as UserModel
from .service import UserService, get_user_service
from .exceptions import NotValidUserData, NotValidAccessToken


def _get_access_token(request: Request) -> str | None:
    """
    Получение токена доступа из запроса

    :param request: запрос на сервер
    :type request: Request
    :return: токен доступа или None при его отсутствии
    :rtype: str | None
    """
    return request.cookies.get("AccessToken")


def _get_refresh_token(request: Request) -> str | None:
    """
    Получение токена обновления из запроса

    :param request: запрос на сервер
    :type request: Request
    :return: токен обновления или None при его отсутствии
    :rtype: str | None
    """
    return request.cookies.get("RefreshToken")


async def get_user_data(
    access_token: str = Depends(_get_access_token),
    refresh_token: str = Depends(_get_refresh_token),
    supabase: SupaBase = Depends(get_supabase),
    user_service: UserService = Depends(get_user_service),
) -> UserModel:
    """
    Получение данных пользователя по токену доступа

    !!! Важно - использовать только через зависимость

    :param access_token:
    :param refresh_token:
    :param supabase:
    :param user_service:
    :return: данные пользователя
    :rtype: UserModel

    .. code-block:: python
        from dh_mood_tracker.users import get_user_data

        @auth_routes.post(
            "/me",
            description="Получение информации о текущем пользователе",
            response_model=PublicUserData
        )
        def get_user_data(user: UserModel = Depends(get_user_data)):
            return user

    :exception NotValidAccessToken: при отсутсвии токена доступа или обновления
    :exception NotValidUserData: при отсутствии данных локального пользователя
    """
    if not access_token or not refresh_token:
        raise NotValidAccessToken()

    supabase.set_access_token(access_token, refresh_token)
    supabase_data: Session = supabase.get_session_data()
    user_supabase_id: UUID = UUID(supabase_data.user.id)

    user_data: UserModel = await user_service.read_by_supabase_id(user_supabase_id)

    if not user_data:
        raise NotValidUserData()

    return user_data
