import os
import shutil

from django.db import connection

import psutil


def get_db_size():
    # Определяем текущий движок базы данных
    db_engine = connection.settings_dict['ENGINE']

    if 'sqlite' in db_engine:
        # Если это SQLite, получаем размер файла базы данных
        db_path = connection.settings_dict['NAME']
        if os.path.exists(db_path):
            db_size = os.path.getsize(db_path)
            db_size_mb = db_size / (1024 * 1024)
            return f"Размер базы данных (SQLite): {db_size_mb:.2f} MB"
        else:
            return "Файл базы данных SQLite не найден."

    elif 'postgresql' in db_engine:
        # Если это PostgreSQL, используем SQL-запрос
        with connection.cursor() as cursor:
            cursor.execute("SELECT pg_database_size(current_database());")
            db_size = cursor.fetchone()[0]
            db_size_mb = db_size / (1024 * 1024)
            return f"Размер базы данных (PostgreSQL): {db_size_mb:.2f} MB"

    else:
        return "Неподдерживаемый тип базы данных."


def get_disk_space():
    # Получаем информацию о диске, на котором находится база данных
    total, used, free = shutil.disk_usage("/")

    # Преобразуем размер в гигабайты
    total_gb = total / (1024 * 1024 * 1024)
    used_gb = used / (1024 * 1024 * 1024)
    free_gb = free / (1024 * 1024 * 1024)

    return f"Всего места: {total_gb:.2f} GB, Использовано: {used_gb:.2f} GB, Свободно: {free_gb:.2f} GB"


def get_memory_info():
    mem = psutil.virtual_memory()
    total_memory = round(mem.total / (1024 ** 3), 2)  # Получение объёма памяти в гигабайтах
    available_memory = round(mem.available / (1024 ** 3), 2)  # Доступная память в гигабайтах
    return f'Всего памяти: {total_memory}, Доступной памяти: {available_memory}'
