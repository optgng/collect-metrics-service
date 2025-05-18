# Структура проекта Monitoring Service

``` bash
monitoring-service/
├── main.py                     # Точка входа (запуск FastAPI-приложения)
├── README.md                   # Документация
├── requirements.txt            # Зависимости Python
├── settings.toml               # Конфигурация Dynaconf (основные параметры)
├── .env                        # Переменные окружения для локальной разработки
├── alembic.ini                 # Конфиг Alembic для миграций
├── app/
│   ├── __init__.py             # Инициализация приложения
│   ├── core/
│   │   ├── config.py           # Загрузка настроек через Dynaconf
│   │   ├── logging.py          # Логирование (JSON-формат)
│   │   ├── feature_flags.py    # Флаги функциональности
│   │   ├── database.py         # Подключение к БД, миграции, сессии
│   │   ├── models/
│   │   │   └── device.py       # SQLAlchemy-модель устройства
│   │   ├── repositories/
│   │   │   └── device_repository.py # Репозиторий для устройств
│   │   ├── schemas/
│   │   │   ├── __init__.py     # Инициализация пакета схем
│   │   │   └── device.py       # Pydantic-схемы устройств
│   │   └── services/
│   │       └── device_service.py # Бизнес-логика для устройств
│   ├── api/
│   │   ├── __init__.py         # Инициализация API
│   │   └── v1/
│   │       ├── routers.py      # Основной роутер API v1
│   │       └── endpoints/
│   │           ├── health.py   # Эндпоинт проверки состояния
│   │           ├── metrics.py  # Эндпоинт экспонирования метрик Prometheus
│   │           └── devices.py  # CRUD для устройств мониторинга
│   ├── collector/
│   │   ├── collector.py        # Логика подключения и сбора метрик с устройств
│   │   ├── scheduler.py        # Планировщик сбора метрик (schedule + Prometheus)
│   │   └── metrics_script.py   # Скрипт для сбора метрик на удалённом сервере
│   ├── middleware.py           # Логирующий middleware для FastAPI
│   └── swagger/
│       └── swagger_info.py     # Кастомизация OpenAPI/Swagger
│   └── migrations/
│       ├── env.py              # Alembic env
│       ├── versions/           # Миграции Alembic
│       └── ...                 # Прочие alembic-файлы
├── ssh/
│   ├── ssh.key                 # Приватный ключ для SSH
│   └── ssh.pub                 # Публичный ключ для SSH
```

## Описание

- **app/core/** — ядро приложения: модели, схемы, репозитории, сервисы, настройки, логирование, работа с БД.
- **app/api/v1/** — реализация REST API (эндпоинты, роутеры).
- **app/collector/** — логика сбора метрик с устройств, планировщик, вспомогательные скрипты.
- **app/migrations/** — миграции Alembic для управления схемой БД.
- **settings.toml** — основная конфигурация приложения (используется Dynaconf).
- **.env** — переменные окружения для локальной разработки.
- **ssh/** — ключи для доступа к инфраструктуре (не включайте приватные ключи в публичные репозитории).

## Основные возможности

- **CRUD для устройств мониторинга** (`/api/v1/devices`)
- **Сбор и экспонирование метрик Prometheus** (`/api/v1/metrics`)
- **Планировщик автоматического сбора метрик** (app/collector/scheduler.py)
- **Проверка состояния сервиса** (`/api/v1/health`)
- **Swagger/OpenAPI** (`/openapi.json`, кастомизация через app/swagger/swagger_info.py)

## Важно

- Все устройства для мониторинга берутся из базы данных, а не из переменных окружения.
- Для production используйте секреты и не храните приватные ключи в публичных репозиториях.
- Для запуска миграций используйте Alembic (`alembic upgrade head`) или функцию `apply_migrations()`.

---
