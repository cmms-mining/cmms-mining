import pandas as pd

from .models import Warehouse


def from_file_to_db(excel_file):
    df = pd.read_excel(
        excel_file,
        skiprows=16,
        skipfooter=5,
        header=None,
        usecols='A, F',
        names=['Nomenclature', 'Code'],
        )

    df_nomenclature = df.iloc[::2].reset_index(drop=True)
    df_warehouse = df.iloc[1::2].reset_index(drop=True)

    df = pd.DataFrame({
        'Code': df_nomenclature['Code'],
        'Nomenclature': df_nomenclature['Nomenclature'],
        'Warehouse': df_warehouse['Nomenclature'],
    })

    # Создание DataFrame с уникальными значениями из столбца 'Warehouse'
    warehouses = df[['Warehouse']].drop_duplicates().reset_index(drop=True)

    # Сохранение уникальных значений складов в базу данных
    for _, row in warehouses.iterrows():
        Warehouse.objects.get_or_create(name=row['Warehouse'])  # Создание записи, если такой склад еще не существует

    print(df)
