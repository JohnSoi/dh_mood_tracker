import json
from abc import ABC, abstractmethod
from datetime import datetime, UTC
from typing import Any


class BaseEvent(ABC):
    @property
    @abstractmethod
    def event_type(self) -> str: ...

    @property
    def timestamp(self) -> datetime:
        return datetime.now(UTC)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "data": self._get_data(),
        }

    @abstractmethod
    def _get_data(self) -> dict[str, Any]: ...

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
