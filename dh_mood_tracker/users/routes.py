from fastapi import Depends, Response, APIRouter

from dh_mood_tracker.utils import SupaBase, get_supabase, email_validator

from .model import User as UserModel
from .schemas import UserLogin, PublicUserData, CreateInUserSchema
from .service import UserService, get_user_service
from .dependency import get_user_data
from .exceptions import IncorrectEmail, UserExistByEmail, UserExistByLogin, UserNotFoundByLogin

user_routes: APIRouter = APIRouter(prefix="/users", tags=["users"])
auth_routes: APIRouter = APIRouter(prefix="/auth", tags=["auth"])


@auth_routes.post("/login", description="Аутентификация пользователя")
async def user_login(
    response: Response,
    login_data: UserLogin,
    user_service: UserService = Depends(get_user_service),
    supabase: SupaBase = Depends(get_supabase),
) -> str:
    if not (user_data := await user_service.read_by_login(login_data.login)):
        raise UserNotFoundByLogin(login_data.login)

    return supabase.login(user_data.email, login_data.password, response)


@auth_routes.post("/register", description="Регистрация нового пользователя")
async def user_register(
    user_data: CreateInUserSchema,
    user_service: UserService = Depends(get_user_service),
    supabase: SupaBase = Depends(get_supabase),
) -> bool:
    if not email_validator(user_data.email):
        raise IncorrectEmail()

    if await user_service.read_by_email(user_data.email):
        raise UserExistByEmail()

    if await user_service.read_by_login(user_data.login):
        raise UserExistByLogin()

    await supabase.create_user(user_data.email, user_data.password, user_data.model_dump())

    return True


@auth_routes.post("/me", description="Получение информации о текущем пользователе", response_model=PublicUserData)
def get_user_data(user: UserModel = Depends(get_user_data)):
    return user


@user_routes.get("/email_confirm", description="Подтверждения адрес электронной почты")
async def email_confirm(access_token: str, supabase: SupaBase = Depends(get_supabase)) -> bool:
    print(await supabase.confirm_email(access_token))

    return True
