# Финальный образ
FROM python:3.13-slim

# Устанавливаем системные зависимости для runtime
RUN apt-get update && apt-get install -y libpq5 curl postgresql postgresql-contrib gcc g++ libpq-dev

# Создаем директорию приложения
WORKDIR /dh-mood-tracker

# Копируем код приложения
COPY . .

# Добавляем локальные пакеты в PATH
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/dh-mood-tracker

# Переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Открываем порт
EXPOSE 8000

RUN cd /dh-mood-tracker && pip install poetry && poetry install

# Команда запуска
CMD ["poetry", "run", "uvicorn", "dh_mood_tracker.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
