"""Модуль модели пользователя"""

__author__: str = "Digital Horizons"

import uuid

from sqlalchemy import UUID, String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from dh_mood_tracker import db


class User(db.BaseModel):
    """
    Модель пользователя

    :cvar id: идентификатор записи
    :cvar email: адрес электронной почты
    :cvar login: логин
    :cvar name: имя
    :cvar surname: фамилия
    :cvar patronymic: отчество
    :cvar is_active: признак активной записи
    :cvar supabase_id: UUID пользователя из SupaBase
    """

    __tablename__: str = "users"

    id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    login: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    surname: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    patronymic: Mapped[str | None] = mapped_column(String(50), unique=True, index=True, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    supabase_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False, index=True)

    @property
    def full_name(self) -> str:
        """
        Полное ФИО пользователя

        :return: полное ФИО
        :rtype: str
        """
        result: str = f"{self.surname} {self.name}"

        if self.patronymic:
            result += f" {self.patronymic}"

        return result

    @property
    def short_full_name(self) -> str:
        """
        Полное ФИО пользователя в коротком формате

        :return: полное ФИО в виде Фамилия И.О.
        :rtype: str
        """
        result: str = f"{self.surname} {self.name[0]}."

        if self.patronymic:
            result += f"{self.patronymic[0]}."

        return result
