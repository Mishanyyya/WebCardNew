FROM python:3.12-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Установка pip-зависимостей
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Копирование исходников
COPY . .

# Установка переменной окружения для продакшена
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Сборка статики
RUN python manage.py collectstatic --noinput

# Выполнение миграций
RUN python manage.py migrate

# Открытие порта
EXPOSE 8000

# Запуск приложения
CMD ["gunicorn", "WebCardNew.wsgi:application", "--bind", "0.0.0.0:8000"]
