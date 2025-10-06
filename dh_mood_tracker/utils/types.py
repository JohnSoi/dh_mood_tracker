# pylint: disable=invalid-name
"""Модуль типов данных"""

__author__: str = "Digital Horizons"

from typing import Callable, Coroutine, TypeAlias, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from dh_mood_tracker.events import BaseEvent

BaseEventType = TypeVar("BaseEventType", bound=BaseEvent)

# Тип данных для обработчика событий
EventHandlerType: TypeAlias = Callable[[BaseEventType, AsyncSession], Coroutine]
