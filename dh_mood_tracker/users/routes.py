
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.util import await_only

from .schemas import CreateInUserSchema, UserLogin
from .service import UserService, get_user_service
from dh_mood_tracker.utils import email_validator, SupaBase, get_supabase

user_routes: APIRouter = APIRouter(prefix="/users", tags=["users"])
auth_routes: APIRouter = APIRouter(prefix="/auth", tags=["auth"])


@auth_routes.post("/login", description="Аутентификация пользователя")
async def user_login(login_data: UserLogin, user_service: UserService = Depends(get_user_service)) -> dict:
    if not await user_service.read_by_login(login_data.login):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Не найден пользователь по логину \"{login_data.login}\"")



@auth_routes.post("/register", description="Регистрация нового пользователя")
async def user_register(user_data: CreateInUserSchema, user_service: UserService = Depends(get_user_service), supabase: SupaBase = Depends(get_supabase)) -> bool:
    if not email_validator(user_data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный адрес электронной почты")

    if await user_service.read_by_email(user_data.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь с таким Email`ом существует")

    if await user_service.read_by_login(user_data.login):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Пользователь с таким логином уже существует")

    await supabase.create_user(user_data.email, user_data.password, user_data.model_dump())

    return True
