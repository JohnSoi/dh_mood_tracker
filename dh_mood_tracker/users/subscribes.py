from dh_mood_tracker.events import EventNames
from dh_mood_tracker.users.service import UserService
from dh_mood_tracker.utils import EventBus


async def users_events_subscribe(event_bus: EventBus) -> None:
    event_bus.subscribe(
        EventNames.SB_USER_CREATED,
        lambda event, db_connection: UserService(db_connection).create_user_by_supabase(event),
    )
