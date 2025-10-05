from uuid import UUID

from pydantic import Field, EmailStr
from pydantic import BaseModel as BaseSchema


class PublicUserData(BaseSchema):
    email: EmailStr
    name: str = Field(..., max_length=50)
    surname: str = Field(..., max_length=50)
    patronymic: str | None = Field(..., max_length=50)


class UserLogin(BaseSchema):
    login: str = Field(..., max_length=50, min_length=4)
    password: str = Field(..., max_length=50, min_length=4)


class CreateInUserSchema(UserLogin, PublicUserData): ...


class CreateItemSchema(CreateInUserSchema):
    supabase_id: UUID
