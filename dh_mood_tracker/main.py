from fastapi import FastAPI
from fastapi.params import Depends

from .core import SupaBase, get_supabase, settings

app: FastAPI = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)


@app.get("/")
async def root():
    return {"Hello": settings.REDIS_URL}


@app.post("/register")
async def register_user(supabase: SupaBase = Depends(get_supabase)) -> dict:
    return supabase.create_user("un.perso@yandex.ru", "RichardMorgan25")


@app.post("/login")
async def login_user(supabase: SupaBase = Depends(get_supabase)) -> dict:
    return supabase.login("un.perso@yandex.ru", "RichardMorgan25")
