"""Пакет для работы с пользователями"""

__author__: str = "Digital Horizons"

from .routes import auth_routes, user_routes
from .service import UserService, get_user_service
from .dependency import get_user_data
from .subscribes import users_events_subscribe
