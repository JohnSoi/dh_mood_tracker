from collections import defaultdict

from dh_mood_tracker.core.types import EventHandlerType
from dh_mood_tracker.events import BaseEvent


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandlerType]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: EventHandlerType) -> None:
        self._handlers[event_type].append(handler)

    def publish(self, event: BaseEvent) -> None:
        for handler in self._handlers[event.event_type]:
            handler(event)


event_bus = EventBus()


def get_event_bus() -> EventBus:
    return event_bus
