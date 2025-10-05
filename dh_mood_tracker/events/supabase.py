from uuid import UUID
from typing import Any

from .base import BaseEvent
from .consts import EventNames


class SupaBaseUserCreate(BaseEvent):
    def __init__(self, supabase_id: UUID, user_data: dict[str, Any]):
        self._data = user_data
        self._user_supabase_uuid = supabase_id

    @property
    def event_type(self) -> str:
        return EventNames.SB_USER_CREATED

    def _get_data(self) -> dict[str, Any]:
        return {
            "UserData": self._data,
            "SupaBaseUuid": self._user_supabase_uuid,
        }
