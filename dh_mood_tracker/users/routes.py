"""Модуль роутинга пользователей"""

__author__: str = "Digital Horizons"

from fastapi import Depends, Response, APIRouter

from dh_mood_tracker.utils import SupaBase, get_supabase, email_validator

from .model import User as UserModel
from .schemas import UserLogin, PublicUserData, CreateInUserSchema
from .service import UserService, get_user_service
from .dependency import get_user_data
from .exceptions import IncorrectEmail, UserExistByEmail, UserExistByLogin, UserNotFoundByLogin

# Роутинг работы с пользователями
user_routes: APIRouter = APIRouter(prefix="/users", tags=["users"])
# Роутинг для аутентификации
auth_routes: APIRouter = APIRouter(prefix="/auth", tags=["auth"])


@auth_routes.post("/login", description="Аутентификация пользователя")
async def user_login(
    response: Response,
    login_data: UserLogin,
    user_service: UserService = Depends(get_user_service),
    supabase: SupaBase = Depends(get_supabase),
) -> bool:
    """Аутентификация пользователя"""
    # Так как SupaBase принимает на вход email пользователя -
    # сначала найдем его по логину, а уже потом сходим в SupaBase
    if not (user_data_db := await user_service.read_by_login(login_data.login)):
        raise UserNotFoundByLogin(login_data.login)

    return supabase.login(user_data_db.email, login_data.password, response)


@auth_routes.post("/register", description="Регистрация нового пользователя")
async def user_register(
    user_data_in: CreateInUserSchema,
    user_service: UserService = Depends(get_user_service),
    supabase: SupaBase = Depends(get_supabase),
) -> bool:
    """Регистрация нового пользователя"""
    # Проверим, что email похож на него
    if not email_validator(user_data_in.email):
        raise IncorrectEmail()

    # Посмотрим, что у нас уже не используется данный email
    if await user_service.read_by_email(user_data_in.email):
        raise UserExistByEmail()

    # Что нет такого же логина
    if await user_service.read_by_login(user_data_in.login):
        raise UserExistByLogin()

    # Создадим пользователя в SupaBase и по событию создадим локального пользователя
    await supabase.create_user(user_data_in.email, user_data_in.password, user_data_in.model_dump())

    return True


@auth_routes.post("/me", description="Получение информации о текущем пользователе", response_model=PublicUserData)
def user_data(user: UserModel = Depends(get_user_data)):
    """Получение информации о текущем пользователе"""
    return user


@user_routes.get("/email_confirm", description="Подтверждения адрес электронной почты")
def email_confirm(access_token: str, supabase: SupaBase = Depends(get_supabase)) -> bool:
    """Подтверждения адрес электронной почты"""
    supabase.confirm_email(access_token)

    return True
