"""Модуль для работы с Redis"""

__author__: str = "Digital Horizons"

import json

import redis

from dh_mood_tracker.core import settings


class RedisManager:
    """
    Менеджер для работы с Redis с удобными методами для кэширования

    !!! Важно - можно использовать через зависимость Depends

    :ivar client: клиент подключения к Redis
    :type client: redis.Redis
    """

    def __init__(self):
        self.client: redis.Redis = self._get_redis_client()

    def get_client(self) -> redis.Redis:
        """
        Получение клиента подключения к Redis

        :return: клиент подключения к Redis
        :rtype: redis.Redis
        """
        return self.client

    async def set_key(self, key: str, value: str, expire_seconds: int | None = None) -> bool:
        """
        Установка ключа с возможным временем жизни

        :param key: ключ записи
        :type key: str
        :param value: значение для записи
        :type value: str
        :param expire_seconds: время жизни записи в секундах
        :type expire_seconds: int | None
        :return: успешность операции
        :rtype: bool

        .. code-block:: python
            from dh_mood_tracker.db import RedisManager

            manager: RedisManager = RedisManager()
            manager.set_key("user_name", "JohnDoe", 900)
        """
        try:
            if expire_seconds:
                return await self.client.setex(key, expire_seconds, value)

            return await self.client.set(key, value)
        except redis.RedisError as e:
            print(f"Ошибка записи в Redis: {e}")
            return False

    async def get_key(self, key: str) -> str | None:
        """
        Получение значения по ключу

        :param key: ключ записи для получения
        :type key: str
        :return: данные записи или None - если ее нет
        :rtype: str | None

        .. code-block:: python
            from dh_mood_tracker.db import RedisManager

            manager: RedisManager = RedisManager()
            manager.get_key("user_name") # "JohnDoe"
        """
        try:
            return await self.client.get(key)
        except redis.RedisError as e:
            print(f"Ошибка получения записи из Redis: {e}")

            return None

    async def delete_key(self, key: str) -> bool:
        """
        Удаление ключа из данных

        :param key: ключ записи
        :type key: str
        :return: успешность удаления
        :rtype: bool

        .. code-block:: python
            from dh_mood_tracker.db import RedisManager

            manager: RedisManager = RedisManager()
            manager.delete_key("user_name")
        """
        try:
            return bool(await self.client.delete(key))
        except redis.RedisError as e:
            print(f"Ошибка при удалении из Redis: {e}")
            return False

    async def key_exists(self, key: str) -> bool:
        """
        Проверка существования ключа

        :param key: ключ записи для проверки
        :type key: str
        :return: флаг существования ключа в Redis
        :rtype: bool

        .. code-block:: python
            from dh_mood_tracker.db import RedisManager

            manager: RedisManager = RedisManager()
            manager.set_key("user_name", "JohnDoe", 900)
            manager.key_exists("user_name") # True
            manager.delete_key("user_name")
            manager.key_exists("user_name") # False
        """
        try:
            return bool(await self.client.exists(key))
        except redis.RedisError as e:
            print(f"Ошибка получения существования ключа в Redis: {e}")
            return False

    async def set_json(self, key: str, data: dict, expire_seconds: int | None = None) -> bool:
        """
        Сохранение JSON данных в Redis

        :param key: ключ записи
        :type key: str
        :param data: значение для записи в виде словаря
        :type data: dict
        :param expire_seconds: время жизни записи в секундах
        :type expire_seconds: int | None
        :return: успешность операции
        :rtype: bool

        .. code-block:: python
            from dh_mood_tracker.db import RedisManager

            manager: RedisManager = RedisManager()
            manager.set_json("user_data", {"name": "JohnDoe", "age": 25}, 900)
        """
        try:
            json_data = json.dumps(data, ensure_ascii=False)
            return await self.set_key(key, json_data, expire_seconds)
        except TypeError as e:
            print(f"Ошибка кодировки JSON в строку: {e}")
            return False

    async def get_json(self, key: str) -> dict | None:
        """
        Получение JSON данных из Redis

        :param key: ключ записи
        :type key: str
        :return: данные в виде словаря или None - если ключа нет
        :rtype: dict | None

        .. code-block:: python
            from dh_mood_tracker.db import RedisManager

            manager: RedisManager = RedisManager()
            manager.get_json("user_data") # {"name": "JohnDoe", "age": 25}
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
        Инкремент счетчика в Redis

        :param key: ключ счетчика
        :type key: str
        :param amount: значение инкремента
        :type amount: int
        :return: значение счетчика
        :rtype: int

        .. code-block:: python
            from dh_mood_tracker.db import RedisManager

            manager: RedisManager = RedisManager()
            manager.increment_counter("user_count") # 1
            manager.increment_counter("user_count", 2) # 3
        """
        try:
            return await self.client.incrby(key, amount)
        except redis.RedisError as e:
            print(f"Ошибка инкрементации счетчика в Redis: {e}")
            return 0

    async def add_to_set(self, key: str, *values) -> int:
        """
        Добавление значений в set

        :param key: ключ множества с данными
        :type key: str
        :param values: данные для вставки
        :return: количество данных в множестве
        :rtype: int

        .. code-block:: python
            from dh_mood_tracker.db import RedisManager

            manager: RedisManager = RedisManager()
            manager.add_to_set("user_count", 1) # 1
            manager.add_to_set("user_count", 2, 3, 4) # 4
        """
        try:
            return await self.client.sadd(key, *values)
        except redis.RedisError as e:
            print(f"Ошибка при добавлении в множество: {e}")
            return 0

    async def get_set_members(self, key: str) -> set:
        """
        Получение всех членов set

        :param key: ключ множества с данными
        :type key: str
        :return: множество данных
        :rtype: set

        .. code-block:: python
            from dh_mood_tracker.db import RedisManager

            manager: RedisManager = RedisManager()
            manager.get_set_members("user_count") # 1, 2, 3, 4
        """
        try:
            return await self.client.smembers(key)
        except redis.RedisError as e:
            print(f"Ошибка получения множества: {e}")
            return set()

    async def publish_message(self, channel: str, message: str) -> int:
        """
        Публикация сообщения в Redis channel

        :param channel: название канала
        :type channel: str
        :param message: сообщение в канал
        :type message: str
        :return: количество сообщений в канале
        :rtype: int

        .. code-block:: python
            from dh_mood_tracker.db import RedisManager

            manager: RedisManager = RedisManager()
            manager.publish_message("user", "add") # 1
        """
        try:
            return await self.client.publish(channel, message)
        except redis.RedisError as e:
            print(f"Ошибка публикации сообщения в Redis: {e}")
            return 0

    @staticmethod
    def _get_redis_client() -> redis.Redis:
        """
        Создание клиента Redis с проверкой работы

        :return: клиент Redis с корректным подключением
        :rtype: redis.Redis
        """
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
    """
    Метод для зависимости для подключения Redis

    :return: менеджер для работы с Redis
    :rtype: RedisManager
    """
    return redis_manager
