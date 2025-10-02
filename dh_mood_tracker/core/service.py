from typing import Any, Generic, TypeVar, Type

from pydantic import BaseModel as BaseSchema
from sqlalchemy import select

from dh_mood_tracker.db import SessionManagerType

ModelType = TypeVar("ModelType")
SchemaType = TypeVar("SchemaType", bound=BaseSchema)


class BaseService(Generic[ModelType, SchemaType]):
    _MODEL: Type[ModelType]

    def __init__(self, session_db: SessionManagerType) -> None:
        self.session_db: SessionManagerType = session_db

    async def scalar_or_none(self, **filters: Any):
        async with self.session_db as session:
            result = await session.scalar(select(self._MODEL).filter_by(**filters))
            await session.close()

        return result