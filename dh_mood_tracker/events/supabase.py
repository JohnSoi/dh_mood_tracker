"""Модуль события создания пользователя в SupaBase"""

__author__: str = "Digital Horizons"

from uuid import UUID
from typing import Any

from .base import BaseEvent
from .consts import EventNames


class SupaBaseUserCreate(BaseEvent):
    """
    Событие создания пользователя в SupaBase

    :ivar _data: данные о пользователе из регистрации
    :type _data: dict[str, Any]
    :ivar _user_supabase_uuid: UUID пользователя в SupaBase
    :type _user_supabase_uuid: UUID
    """

    def __init__(self, supabase_id: UUID, user_data: dict[str, Any]):
        """
        Инициализация события создания пользователя в SupaBase

        :param supabase_id: UUID пользователя в SupaBase
        :type supabase_id: UUID
        :param user_data: данные о пользователе из регистрации
        :type user_data: dict[str, Any]
        """
        self._data = user_data
        self._user_supabase_uuid = supabase_id

    @property
    def event_type(self) -> EventNames:
        return EventNames.SB_USER_CREATED

    def _get_data(self) -> dict[str, Any]:
        return {
            "UserData": self._data,
            "SupaBaseUuid": self._user_supabase_uuid,
        }
