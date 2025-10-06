"""Пакет базового функционала"""

__author__: str = "Digital Horizons"

from .service import BaseService
from .settings import Settings, settings
from .exceptions import (
    BaseAppException,
    BaseExistEntityError,
    BaseNotAuthAppException,
    BaseNotFoundAppException,
    BaseBadRequestAppException,
)
