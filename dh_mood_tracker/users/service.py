from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dh_mood_tracker.db import SessionManagerType, get_db_session
from dh_mood_tracker.events import BaseEvent
from dh_mood_tracker.core.service import BaseService

from .model import User as UserModel
from .schemas import CreateItemSchema


class UserService(BaseService[UserModel, CreateItemSchema]):
    _MODEL: UserModel = UserModel

    async def read_by_login(self, login: str) -> UserModel | None:
        return await self.scalar_or_none(login=login)

    async def read_by_email(self, email: str) -> UserModel | None:
        return await self.scalar_or_none(email=email)

    async def create_user_by_supabase(self, event: BaseEvent) -> None:
        event_data: dict = event.to_dict().get("data")
        user_db_data: CreateItemSchema = CreateItemSchema(
            **event_data.get("UserData"), supabase_id=event_data.get("SupaBaseUuid")
        )
        await self.create(user_db_data)


def get_user_service(session_db: AsyncSession = Depends(get_db_session)) -> UserService:
    return UserService(session_db)
