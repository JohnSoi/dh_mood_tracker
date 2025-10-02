from typing import TypeAlias, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

SessionManagerType: TypeAlias = AsyncGenerator[AsyncSession, None]
