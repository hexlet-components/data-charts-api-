import sqlite3
from datetime import datetime, timedelta

import pytest

from app.server import app


def dict_factory(cursor, row):
    """Преобразует результаты SQLite в словарь"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@pytest.fixture
def client():
    """Фикстура для тестового клиента с SQLite в памяти"""
    # Создаем in-memory SQLite базу
    db = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = dict_factory

    # Создаем схему
    with db.cursor() as cur:
        cur.execute("""
            CREATE TABLE visits (
                id INTEGER PRIMARY KEY,
                datetime TIMESTAMP NOT NULL
                -- добавьте остальные поля
            )
        """)

        cur.execute("""
            CREATE TABLE registrations (
                id INTEGER PRIMARY KEY,
                datetime TIMESTAMP NOT NULL
                -- добавьте остальные поля
            )
        """)

        # Добавляем тестовые данные
        cur.execute("""
            INSERT INTO visits (datetime) VALUES
            (?), (?)
        """, (datetime.now(), datetime.now() - timedelta(days=1)))

        cur.execute("""
            INSERT INTO registrations (datetime) VALUES
            (?)
        """, (datetime.now(),))

        db.commit()

    # Подменяем подключение к БД в приложении
    def get_test_db():
        return db

    app.get_db = get_test_db

    with app.test_client() as client:
        yield client

    db.close()
