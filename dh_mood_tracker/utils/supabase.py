import re
from typing import Any
from uuid import UUID

from fastapi import Depends, HTTPException, status
from supabase import create_client, Client
from supabase_auth import AuthResponse
from supabase_auth.errors import AuthApiError

from .event_bus import EventBus, get_event_bus
from dh_mood_tracker.core.settings import settings
from dh_mood_tracker.events.supabase import SupaBaseUserCreate
from dh_mood_tracker.db import get_db_session


class SupaBase:
    def __init__(self) -> None:
        self._client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_TOKEN)
        self._event_bus: EventBus = get_event_bus(get_db_session())

    async def create_user(self, email: str, password: str, other_data: dict[str, Any]) -> bool:
        try:
            supabase_data: AuthResponse = self._client.auth.sign_up({"email": email, "password": password})
        except AuthApiError as ex:
            detail, status_code = self._exception_adapter(ex)
            raise HTTPException(status_code=status_code, detail=detail)

        await self._event_bus.publish(SupaBaseUserCreate(UUID(supabase_data.user.id), other_data))

        return True

    def login(self, email: str, password: str) -> AuthResponse:
        return self._client.auth.sign_in_with_password({"email": email, "password": password})

    @staticmethod
    def _exception_adapter(exception: Exception) -> tuple[str, int]:
        EXCEPTION_MESSAGE_MAP: dict[str, tuple[str, int]] = {
            r"^Email address \"(.*)\" is invalid": (
                "Некорректный Email",
                status.HTTP_400_BAD_REQUEST,
            )
        }

        for pattern, error_msg_code in EXCEPTION_MESSAGE_MAP.items():
            if bool(re.match(r"^Email address \"(.*)\" is invalid", str(exception))):
                return error_msg_code

        return str(exception), status.HTTP_500_INTERNAL_SERVER_ERROR


supabase: SupaBase | None = None


def get_supabase() -> SupaBase:
    global supabase

    if supabase is None:
        supabase = SupaBase()

    return supabase
