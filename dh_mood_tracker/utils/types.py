from typing import TypeAlias, Callable, AsyncGenerator, Coroutine

from sqlalchemy.ext.asyncio import AsyncSession

from dh_mood_tracker.db import SessionManagerType
from dh_mood_tracker.events import BaseEvent

EventHandlerType: TypeAlias = Callable[[BaseEvent, SessionManagerType], Coroutine]
