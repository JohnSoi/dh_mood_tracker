from fastapi import Depends
from sqlalchemy import select

from dh_mood_tracker.db import get_db_session, SessionManagerType
from .model import User as UserModel
from .schemas import CreateItemSchema
from ..core.service import BaseService
from ..events import BaseEvent


class UserService(BaseService[UserModel, CreateItemSchema]):
    _MODEL: UserModel = UserModel

    async def read_by_login(self, login: str) -> UserModel | None:
        return await self.scalar_or_none(login=login)

    async def read_by_email(self, email: str) -> UserModel | None:
        return await self.scalar_or_none(email=email)

    async def create_user_by_supabase(self, event: BaseEvent) -> None:
        event_data: dict = event.to_dict().get("data")
        user_db_data: CreateItemSchema = CreateItemSchema(**event_data.get("UserData"), supabase_id=event_data.get("SupaBaseUuid"))
        model_data: UserModel = UserModel(**user_db_data.model_dump(exclude=["password"]))

        async with self.session_db as session:
            session.add(model_data)
            await session.commit()
            session.refresh(model_data)


def get_user_service(session_db: SessionManagerType = Depends(get_db_session)) -> UserService:
    return UserService(session_db)