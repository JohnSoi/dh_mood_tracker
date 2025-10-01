from supabase import create_client, Client
from supabase_auth import AuthResponse

from dh_mood_tracker.core.settings import settings


class SupaBase:
    def __init__(self) -> None:
        self._client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_TOKEN)

    def create_user(self, email: str, password: str) -> AuthResponse:
        return self._client.auth.sign_up({
            "email": email,
            "password": password
        })

    def login(self, email: str, password: str) -> AuthResponse:
        return self._client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })


supabase: SupaBase = SupaBase()


def get_supabase() -> SupaBase:
    return supabase
