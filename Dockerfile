# Stage 1: Build binary with PyInstaller
FROM python:3.11-slim as builder

RUN apt-get update && \
  apt-get install -y gcc libpq-dev ssh build-essential && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pyinstaller

COPY . .

# Собираем бинарник main с помощью PyInstaller
RUN pyinstaller --onefile --name monitoring_service main.py --add-data "alembic.ini:."

# Stage 2: Minimal runtime image
FROM python:3.11-slim

WORKDIR /app

# Копируем бинарник из builder-стадии
COPY --from=builder /app/dist/monitoring_service /app/monitoring_service

# Копируем необходимые файлы (например, настройки, миграции, ssh-ключи)
COPY settings.toml .
COPY app/migrations ./app/migrations
COPY app/ssh ./app/ssh
COPY alembic.ini .

# Открываем порт для приложения
EXPOSE 8000

# Запуск бинарника
CMD ["./monitoring_service"]
