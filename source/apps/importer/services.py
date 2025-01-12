import pandas as pd

from .models import Nomenclature, Warehouse


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

    warehouses = df[['Warehouse']].drop_duplicates().reset_index(drop=True)

    Warehouse.objects.all().delete()
    for _, row in warehouses.iterrows():
        Warehouse.objects.create(name=row['Warehouse'])

    Nomenclature.objects.all().delete()
    for _, row in df.iterrows():
        Nomenclature.objects.create(
            code=row['Code'],
            name=row['Nomenclature'],
            warehouse=Warehouse.objects.get(name=row['Warehouse']),
        )
