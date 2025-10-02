from collections import defaultdict

from fastapi import Depends

from dh_mood_tracker.db import SessionManagerType, get_db_session
from dh_mood_tracker.events import BaseEvent

from .types import EventHandlerType


class EventBus:
    def __init__(self, db_session: SessionManagerType) -> None:
        self._handlers: dict[str, list[EventHandlerType]] = defaultdict(list)
        self._db_session: SessionManagerType = db_session

    def subscribe(self, event_type: str, handler: EventHandlerType) -> None:
        print(f'✅ Добавлен обработчик события "{event_type}"')
        self._handlers[event_type].append(handler)

    async def publish(self, event: BaseEvent) -> None:
        print(f'✅ Публикация события "{event.event_type}"')
        for handler in self._handlers[event.event_type]:
            await handler(event, self._db_session)


event_bus = None


def get_event_bus(db_session: SessionManagerType = Depends(get_db_session)) -> EventBus:
    global event_bus

    if not event_bus:
        event_bus = EventBus(db_session)

    return event_bus
