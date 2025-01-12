import pandas as pd

from .models import Nomenclature, Warehouse


def from_file_to_db(excel_file):
    df = pd.read_excel(
        excel_file,
        skiprows=16,
        skipfooter=5,
        header=None,
        usecols='A, F',
        names=['nomenclature', 'code'],
        )

    df['code'] = df['code'].str.rstrip()

    df_nomenclature = df.iloc[::2].reset_index(drop=True)
    df_warehouse = df.iloc[1::2].reset_index(drop=True)

    df = pd.DataFrame({
        'code': df_nomenclature['code'],
        'nomenclature': df_nomenclature['nomenclature'],
        'warehouse': df_warehouse['nomenclature'],
    })

    warehouses = df[['warehouse']].drop_duplicates().reset_index(drop=True)

    Warehouse.objects.all().delete()
    for _, row in warehouses.iterrows():
        Warehouse.objects.create(name=row['warehouse'])

    Nomenclature.objects.all().delete()
    for _, row in df.iterrows():
        Nomenclature.objects.create(
            code=row['code'],
            name=row['nomenclature'],
            warehouse=Warehouse.objects.get(name=row['warehouse']),
        )
