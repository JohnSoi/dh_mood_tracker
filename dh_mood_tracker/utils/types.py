"""Модуль типов данных"""

__author__: str = "Digital Horizons"

from typing import Callable, Coroutine, TypeAlias

from sqlalchemy.ext.asyncio import AsyncSession

from dh_mood_tracker.db import SessionManagerType
from dh_mood_tracker.events import BaseEvent

# Тип данных для обработчика событий
EventHandlerType: TypeAlias = Callable[[BaseEvent, AsyncSession], Coroutine]
