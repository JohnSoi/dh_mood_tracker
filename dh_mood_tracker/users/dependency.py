from uuid import UUID

from fastapi import Request, Depends
from supabase_auth import AuthResponse, Session

from .exceptions import NotValidAccessToken, NotValidUserData
from .service import UserService, get_user_service
from .model import User as UserModel
from dh_mood_tracker.utils import SupaBase, get_supabase



def get_access_token(request: Request) -> str | None:
    return request.cookies.get("AccessToken")


def get_refresh_token(request: Request) -> str | None:
    return request.cookies.get("RefreshToken")

async def get_user_data(access_token: str = Depends(get_access_token), refresh_token: str = Depends(get_refresh_token), supabase: SupaBase = Depends(get_supabase), user_service: UserService = Depends(get_user_service)) -> UserModel:
    if not access_token or not refresh_token:
        raise NotValidAccessToken()

    supabase.set_access_token(access_token, refresh_token)
    supabase_data: Session = supabase.get_session_data()
    user_supabase_id: UUID = UUID(supabase_data.user.id)

    user_data: UserModel = await user_service.read_by_supabase_id(user_supabase_id)

    if not user_data:
        raise NotValidUserData()

    return user_data

