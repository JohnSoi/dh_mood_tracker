"""Модуль типизации подключений к БД"""

__author__: str = "Digital Horizons"

from typing import TypeAlias, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

# Тип для менеджера сессий подключений
SessionManagerType: TypeAlias = AsyncGenerator[AsyncSession, None]
