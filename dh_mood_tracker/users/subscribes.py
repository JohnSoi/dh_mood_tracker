"""Модуль подписок на события для пользователей"""

__author__: str = "Digital Horizons"

from dh_mood_tracker.utils import EventBus
from dh_mood_tracker.events import EventNames

from .service import UserService


async def users_events_subscribe(event_bus: EventBus) -> None:
    """
    Подписка на событие создания пользователя в SupaBase. Создает локального пользователя в БД

    :param event_bus: шина событий
    :type event_bus: EventBus
    """
    event_bus.subscribe(
        EventNames.SB_USER_CREATED,
        lambda event, db_connection: UserService(db_connection).create_user_by_supabase(event),
    )
