from datetime import datetime

from django.core.files.uploadedfile import InMemoryUploadedFile

import pandas as pd

from apps.equipments.models import Equipment, EquipmetRunningTime

try:
    from .files_id import FILE_ID
except ImportError:
    FILE_ID = "ID"

from .google import create_service
from .models import Nomenclature, Warehouse


def load_nomenclature_and_warehouses_to_db(excel_file: InMemoryUploadedFile):
    """Обрабатывает Excel-файл, создаёт записи для складов и номенклатуры"""
    try:
        df = pd.read_excel(
            io=excel_file,
            skiprows=16,
            skipfooter=5,
            header=None,
            usecols='A, F',
            names=['nomenclature', 'code'],
        )
    except FileNotFoundError:
        raise ValueError(f"Файл {excel_file} не найден")
    except Exception as e:
        raise ValueError(f"Ошибка при чтении файла: {e}")

    if df.empty:
        raise ValueError("Файл не содержит данных или данные не соответствуют ожидаемому формату")

    df['code'] = df['code'].str.rstrip()
    df['nomenclature'] = df['nomenclature'].str.rstrip()

    df_nomenclature = df.iloc[::2].reset_index(drop=True)
    df_warehouse = df.iloc[1::2].reset_index(drop=True)

    df = pd.DataFrame({
        'code': df_nomenclature['code'],
        'nomenclature': df_nomenclature['nomenclature'],
        'warehouse': df_warehouse['nomenclature'],
    })

    warehouses = df[['warehouse']].drop_duplicates().reset_index(drop=True)

    for _, row in warehouses.iterrows():
        Warehouse.objects.get_or_create(name=row['warehouse'])

    Nomenclature.objects.all().delete()
    for _, row in df.iterrows():
        Nomenclature.objects.create(
            code=row['code'],
            name=row['nomenclature'],
            warehouse=Warehouse.objects.get(name=row['warehouse']),
        )


def load_running_time_to_db() -> list:
    """Делает запрос в гугл таблицу, создает записи наработки оборудования"""
    service = create_service()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=FILE_ID, range='Лист3!A:C').execute()
    values = result.get('values', [])

    df = pd.DataFrame(values)

    df = df[1:]  # Убираем первую строку из данных

    df.columns = ['date', 'equipment_number', 'running_time']
    df.replace('', pd.NA, inplace=True)
    df = df.dropna(subset=['equipment_number'])

    loaded_running_times = []
    for _index, row in df.iterrows():
        equipment_number = row.to_dict().get('equipment_number')

        if Equipment.objects.filter(number=equipment_number).exists():
            equipment = Equipment.objects.get(number=equipment_number)
            date_str: str = row.to_dict().get('date')
            date = datetime.strptime(date_str, "%d.%m.%Y").date()
            try:
                running_time = int(row.to_dict().get('running_time'))
            except (ValueError, TypeError) as e:
                print(e)
                continue
            obj, created = EquipmetRunningTime.objects.get_or_create(
                equipment=equipment,
                date=date,
                defaults={'running_time': running_time},
                )
            if created:
                loaded_running_times.append(obj)

    return loaded_running_times
