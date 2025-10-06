# pylint: disable=unnecessary-ellipsis
"""Модуль класса базового события"""

__author__: str = "Digital Horizons"

import json
from abc import ABC, abstractmethod
from typing import Any
from datetime import UTC, datetime

from dh_mood_tracker.events.consts import EventNames


class BaseEvent(ABC):
    """Базовое событие"""

    @property
    @abstractmethod
    def event_type(self) -> EventNames:
        """
        Тип события из константы

        :return: название события
        :rtype: EventNames
        """
        ...

    @property
    def timestamp(self) -> datetime:
        """
        Метка времени события

        :return: метка времени
        :rtype: datetime
        """
        return datetime.now(UTC)

    def to_dict(self) -> dict[str, Any]:
        """
        Преобразования события в dict

        :return: событие в виде словаря
        :rtype: dict[str, Any]
        """
        return {
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "data": self._get_data(),
        }

    @abstractmethod
    def _get_data(self) -> dict[str, Any]:
        """
        Получение данных для события

        :return: данные события
        :rtype: dict[str, Any]
        """
        ...

    def to_json(self) -> str:
        """
        Преобразование события в строку JSON

        :return:  событие в виде строки JSON
        :rtype: str
        """
        return json.dumps(self.to_dict())
