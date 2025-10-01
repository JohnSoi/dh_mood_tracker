from uuid import UUID

from pydantic import BaseModel as BaseSchema, Field, EmailStr


class CreateInUserSchema(BaseSchema):
    login: str = Field(..., max_length=50, min_length=4)
    password: str = Field(..., max_length=50, min_length=4)
    email: EmailStr
    name: str = Field(..., max_length=50)
    surname: str = Field(..., max_length=50)
    patronymic: str | None = Field(..., max_length=50)


class CreateItemSchema(CreateInUserSchema):
    supabase_id: UUID
