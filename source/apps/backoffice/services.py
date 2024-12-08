import psutil
import shutil

from django.db import connection


def get_db_size():
    # Открываем курсор для выполнения SQL-запроса
    with connection.cursor() as cursor:
        # Выполняем запрос на получение размера базы данных
        cursor.execute("SELECT pg_database_size(current_database());")
        # Получаем результат в байтах
        db_size = cursor.fetchone()[0]

    # Преобразуем размер в мегабайты
    db_size_mb = db_size / (1024 * 1024)

    return f"Размер базы данных: {db_size_mb:.2f} MB"


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
