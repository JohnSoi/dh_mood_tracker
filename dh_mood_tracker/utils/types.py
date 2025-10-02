from typing import Callable, Coroutine, TypeAlias, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from dh_mood_tracker.db import SessionManagerType
from dh_mood_tracker.events import BaseEvent

EventHandlerType: TypeAlias = Callable[[BaseEvent, SessionManagerType], Coroutine]
