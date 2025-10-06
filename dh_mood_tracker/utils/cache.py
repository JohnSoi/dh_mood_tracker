"""Модуль для работы с кешированием"""

__author__: str = "Digital Horizons"

from redis import RedisError

from dh_mood_tracker.db import RedisManager


def cache_result(key_pattern: str, expire_seconds: int = 300):
    """
    Декоратор кеширования результат работы функции

    :param key_pattern: паттерн для создания ключа кеша
    :type key_pattern: str
    :param expire_seconds: время истечения жизни кеша
    :type expire_seconds: int

    .. code-block:: python
        from dh_mood_tracker.utils import cache_result

        # Кеширование чтения пользователя на 15 минут
        @cache_result(f"user_id: {}", 900)
        def read_user(user_id: int):
            ...
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Генерация ключа на основе аргументов
            cache_key = key_pattern.format(*args, **kwargs)

            # Попытка получить из кэша
            redis_manager = RedisManager()
            cached_result = await redis_manager.get_json(cache_key)
            if cached_result is not None:
                return cached_result

            # Выполнение функции и сохранение в кэш
            result = await func(*args, **kwargs)
            await redis_manager.set_json(cache_key, result, expire_seconds)

            return result

        return wrapper

    return decorator


async def invalidate_cache_pattern(pattern: str) -> None:
    """
    Инвалидация записей кеша по паттерну ключа

    :param pattern: паттерн ключа кеша
    :type pattern: str
    """
    try:
        redis_manager = RedisManager()
        client = redis_manager.get_client()
        keys = await client.keys(pattern)

        if keys:
            await client.delete(*keys)

    except RedisError as e:
        print(f"Ошибка инвалидации кеша: {e}")
