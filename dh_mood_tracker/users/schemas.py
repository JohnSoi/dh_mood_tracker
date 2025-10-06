# pylint: disable=unnecessary-ellipsis
"""Модуль схем данных пользователя"""

__author__: str = "Digital Horizons"

from uuid import UUID

from pydantic import Field, EmailStr
from pydantic import BaseModel as BaseSchema


class PublicUserData(BaseSchema):
    """
    Публичные данные пользователя

    :cvar email: адрес электронной почты пользователя
    :type email: EmailStr
    :cvar name: имя пользователя
    :type name: str
    :cvar surname: фамилия пользователя
    :type surname: str
    :cvar patronymic: отчество пользователя
    :type patronymic: str
    """

    email: EmailStr
    name: str = Field(..., max_length=50)
    surname: str = Field(..., max_length=50)
    patronymic: str | None = Field(..., max_length=50)


class UserLogin(BaseSchema):
    """
    Данные для аутентификации пользователя

    :cvar: login: логин пользователя
    :type login: str
    :cvar: password: пароль пользователя
    :type password: str
    """

    login: str = Field(..., max_length=50, min_length=4)
    password: str = Field(..., max_length=50, min_length=4)


class CreateInUserSchema(UserLogin, PublicUserData):
    """Схема для создания пользователя"""

    ...


class CreateItemSchema(CreateInUserSchema):
    """
    Схема данных для записи пользователя в БД

    :cvar supabase_id: UUID записи пользователя в SupaBase
    :type supabase_id: UUID
    """

    supabase_id: UUID
