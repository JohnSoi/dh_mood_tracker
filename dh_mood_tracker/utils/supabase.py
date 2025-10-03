import re
from uuid import UUID
from typing import Any

from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from supabase import Client, create_client
from supabase_auth import AuthResponse
from supabase_auth.errors import AuthApiError

from dh_mood_tracker.db import get_db_session
from dh_mood_tracker.core.settings import settings
from dh_mood_tracker.events.supabase import SupaBaseUserCreate
from .consts import EXCEPTION_MESSAGE_MAP

from .event_bus import EventBus, get_event_bus


class SupaBase:
    def __init__(self, session_db: AsyncSession) -> None:
        self._client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_TOKEN)
        self._event_bus: EventBus = get_event_bus(session_db)

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
        for pattern, error_msg_code in EXCEPTION_MESSAGE_MAP.items():
            if bool(re.match(pattern, str(exception))):
                return error_msg_code

        return str(exception), status.HTTP_500_INTERNAL_SERVER_ERROR




def get_supabase(session_db: AsyncSession = Depends(get_db_session)) -> SupaBase:
    return SupaBase(session_db)
