from typing import TypeAlias, Callable

from dh_mood_tracker.events import BaseEvent

EventHandlerType: TypeAlias = Callable[[BaseEvent], None]