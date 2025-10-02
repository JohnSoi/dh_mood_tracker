"""Модуль основного приложения"""

__author__: str = "Digital Horizons"

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import get_db_session
from .users import auth_routes, user_routes, users_events_subscribe
from .utils import get_event_bus
from .core.settings import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Жизненный цикл приложения"""
    await users_events_subscribe(get_event_bus(get_db_session()))
    yield


app: FastAPI = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, lifespan=lifespan)


@app.get("/health", description="Проверка состояния системы")
def health_check() -> bool:
    """
    Роут для проверки состояния приложения

    :return: готовность приложения
    :rtype: bool
    """
    return True


app.include_router(auth_routes)
app.include_router(user_routes)
