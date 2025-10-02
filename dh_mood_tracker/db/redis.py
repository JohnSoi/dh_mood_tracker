import json

import redis

from dh_mood_tracker.core import settings


class RedisManager:
    """
    Менеджер для работы с Redis с удобными методами для кэширования
    """

    def __init__(self):
        self.client: redis.Redis = self._get_redis_client()

    def get_client(self) -> redis.Redis:
        return self.client

    async def set_key(self, key: str, value: str, expire_seconds: int = None) -> bool:
        """
        Установка ключа с возможным временем жизни
        """
        try:
            if expire_seconds:
                return await self.client.setex(key, expire_seconds, value)
            else:
                return await self.client.set(key, value)
        except redis.RedisError as e:
            print(f"Ошибка записи в Redis: {e}")
            return False

    async def get_key(self, key: str) -> str | None:
        """
        Получение значения по ключу
        """
        try:
            return await self.client.get(key)
        except redis.RedisError as e:
            print(f"Ошибка получения записи из Redis: {e}")

            return None

    async def delete_key(self, key: str) -> bool:
        """
        Удаление ключа
        """
        try:
            return bool(await self.client.delete(key))
        except redis.RedisError as e:
            print(f"Redis delete error: {e}")
            return False

    async def key_exists(self, key: str) -> bool:
        """
        Проверка существования ключа
        """
        try:
            return bool(await self.client.exists(key))
        except redis.RedisError as e:
            print(f"Ошибка получения существования ключа в Redis: {e}")
            return False

    async def set_json(self, key: str, data: dict, expire_seconds: int = None) -> bool:
        """
        Сохранение JSON данных в Redis
        """
        try:
            json_data = json.dumps(data, ensure_ascii=False)
            return await self.set_key(key, json_data, expire_seconds)
        except (TypeError, json.JSONEncodeError) as e:
            print(f"Ошибка кодировки JSON в строку: {e}")
            return False

    async def get_json(self, key: str) -> dict | None:
        """
        Получение JSON данных из Redis
        """
        try:
            data = await self.get_key(key)
            if data:
                return json.loads(data)
            return None
        except json.JSONDecodeError as e:
            print(f"Ошибка преобразования строки в JSON: {e}")
            return None

    async def increment_counter(self, key: str, amount: int = 1) -> int:
        """
        Инкремент счетчика
        """
        try:
            return await self.client.incrby(key, amount)
        except redis.RedisError as e:
            print(f"Ошибка инкрементации счетчика в Redis: {e}")
            return 0

    async def add_to_set(self, key: str, *values) -> int:
        """
        Добавление значений в set
        """
        try:
            return await self.client.sadd(key, *values)
        except redis.RedisError as e:
            print(f"Ошибка при добавлении в множество: {e}")
            return 0

    async def get_set_members(self, key: str) -> set:
        """
        Получение всех членов set
        """
        try:
            return await self.client.smembers(key)
        except redis.RedisError as e:
            print(f"Ошибка получения множества: {e}")
            return set()

    async def publish_message(self, channel: str, message: str) -> int:
        """
        Публикация сообщения в Redis channel
        """
        try:
            return await self.client.publish(channel, message)
        except redis.RedisError as e:
            print(f"Ошибка публикации сообщения в Redis: {e}")
            return 0

    @staticmethod
    def _get_redis_client() -> redis.Redis:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,  # Автоматическое декодирование из bytes в str
            socket_connect_timeout=5,
            socket_keepalive=True,
        )
        # Тестирование соединения
        try:
            redis_client.ping()
            print("✅ Подключение к Redis установлено")
        except redis.ConnectionError as e:
            print(f"❌ Не удалось подключиться к Redis: {e}")
            raise
        return redis_client


# Глобальный экземпляр менеджера Redis
redis_manager = RedisManager()


def get_redis_manager() -> RedisManager:
    return redis_manager
