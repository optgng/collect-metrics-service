from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic import command
from alembic.config import Config
import os
import logging
import sys

from app.core.models.device import Base  # Добавлено для создания таблиц

DB_HOST = settings.DB_HOST
DB_PORT = settings.DB_PORT
DB_NAME = settings.DB_NAME
DB_USER = settings.DB_USER
DB_PASSWORD = settings.DB_PASSWORD
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Принудительное создание таблиц, если их нет
Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def apply_migrations():
    # Определяем путь к alembic.ini для PyInstaller и обычного запуска
    if hasattr(sys, '_MEIPASS'):
        alembic_ini_path = os.path.join(sys._MEIPASS, 'alembic.ini')
    else:
        alembic_ini_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../alembic.ini'))
    alembic_cfg = Config(alembic_ini_path)
    logging.info("Начинаю миграцию....")
    try:
        command.upgrade(alembic_cfg, 'head')
        logging.info("Миграции успешно применены.")
    except Exception as e:
        logging.error(f"Ошибка при применении миграций: {e}")
        raise