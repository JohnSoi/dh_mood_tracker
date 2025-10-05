# pylint: disable=global-statement
"""Модуль шины событий"""

__author__: str = "Digital Horizons"

from collections import defaultdict

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dh_mood_tracker.db import get_db_session
from dh_mood_tracker.events import BaseEvent, EventNames
from .types import EventHandlerType


class EventBus:
    """
    Класс шины событий

    :ivar _handlers: карта списков обработчиков по названию событий
    :type _handlers: dict[str, list[EventHandlerType]]
    :ivar _db_session: сессия подключения к БД
    :type _db_session: AsyncSession
    """
    def __init__(self, db_session: AsyncSession) -> None:
        """
        Инициализация шины событий приложения

        !!! Важно - использовать только через зависимость Depends

        :param db_session: сессия подключения к БД
        :type db_session: AsyncSession
        """
        self._handlers: dict[str, list[EventHandlerType]] = defaultdict(list)
        self._db_session: AsyncSession = db_session

    def subscribe(self, event_type: EventNames, handler: EventHandlerType) -> None:
        """
        Подписка на событие определенного типа

        !!! Важно - использовать имена только из EventNames

        :param event_type: тип события, описанный в константе EventNames
        :type event_type: EventNames
        :param handler: обработчик события
        :type handler: EventHandlerType

        .. code-block:: python
            from dh_mood_tracker.utils import EventBus
            from dh_mood_tracker.events import EventNames

            event_bus.subscribe(
                EventNames.SB_USER_CREATED,
                lambda event, db_connection: UserService(db_connection).create_user_by_supabase(event),
            )
        """
        print(f'✅ Добавлен обработчик события "{event_type}"')
        self._handlers[event_type].append(handler)

    async def publish(self, event: BaseEvent) -> None:
        """
        Публикация события. Запускает весь список обработчиков данного события

        :param event: экземпляр события
        :type event: BaseEvent

        .. code-block:: python
            from dh_mood_tracker.utils import EventBus, get_event_bus
            from dh_mood_tracker.events import SupaBaseUserCreate

            event_bus: EventBus = get_event_bus(session_db)
            event_bus.publish(SupaBaseUserCreate(UUID(supabase_data.user.id), other_data))
        """
        print(f'✅ Публикация события "{event.event_type}"')
        for handler in self._handlers[event.event_type]:
            await handler(event, self._db_session)


# Глобальный экземпляр шины событий
EVENT_BUS: EventBus | None = None


def get_event_bus(db_session: AsyncSession = Depends(get_db_session)) -> EventBus:
    """
    Метод для зависимости получения шины событий

    :param db_session: сессия подключения к БД
    :type db_session: AsyncSession
    :return: экземпляр класса шины событий
    :rtype: EventBus

    .. code-block:: python
        @asynccontextmanager
        async def lifespan(_: FastAPI):
            async with AsyncSessionLocal() as session:
                await users_events_subscribe(get_event_bus(session))
            yield
    """
    global EVENT_BUS

    if not EVENT_BUS:
        EVENT_BUS = EventBus(db_session)

    return EVENT_BUS
