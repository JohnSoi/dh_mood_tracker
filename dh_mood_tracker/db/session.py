# pylint: disable=too-few-public-methods
"""Модуль для сессии подключения к PostgreSQL"""

__author__: str = "Digital Horizons"

from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, declarative_base, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from dh_mood_tracker.core import settings

from .types import SessionManagerType


class BaseModel(DeclarativeBase):
    """
    Базовая модель

    :cvar id: идентификатор записи
    :type id: int
    """

    id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)


# Создание асинхронного движка базы данных
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Логирование SQL запросов
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_recycle=3600,  # Пересоздание соединения каждый час
    pool_size=20,  # Размер пула соединений
    max_overflow=30,  # Максимальное количество соединений сверх pool_size
)

# Создание асинхронной фабрики сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_db_session() -> SessionManagerType:
    """
    Асинхронный контекстный менеджер для работы с сессией БД.

    .. code-block:: python
        from sqlalchemy.ext.asyncio import AsyncSession
        from dh_mood_tracker.db import get_db_session

        def get_event_bus(db_session: AsyncSession = Depends(get_db_session)) -> EventBus:
            return EventBus(db_session)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
