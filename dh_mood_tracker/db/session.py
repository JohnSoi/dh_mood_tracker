# Создание базового класса для моделей
import contextlib

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, DeclarativeBase

from dh_mood_tracker.core import settings
from .types import SessionManagerType

BaseModel: DeclarativeBase = declarative_base()

# Создание асинхронного движка базы данных
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # Логирование SQL запросов
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


@contextlib.asynccontextmanager
async def get_db_session() -> SessionManagerType:
    """
    Асинхронный контекстный менеджер для работы с сессией БД.
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
