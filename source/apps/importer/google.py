import os
import pickle
from datetime import datetime

from google.auth.transport.requests import Request

from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import Resource, build

import pandas as pd

from apps.equipments.models import Equipment, EquipmetRunningTime

from .files_id import FILE_ID


PATH = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRET_FILE = os.path.join(PATH, "client_secret.json")
API_NAME = "sheets"
API_VERSION = "v4"
SCOPES = ["https://www.googleapis.com/auth/drive"]


def create_service() -> Resource:
    credentials = get_cred_from_pickle()
    service = build(API_NAME, API_VERSION, credentials=credentials)
    return service


def get_cred_from_pickle():
    cred = None

    pickle_file = os.path.join(PATH, f'token_{API_NAME}_{API_VERSION}.pickle')

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    return cred


def connect_google_drive():
    service = create_service()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=FILE_ID, range='Лист3!A:C').execute()
    values = result.get('values', [])

    df = pd.DataFrame(values)

    df = df[1:]  # Убираем первую строку из данных

    df.columns = ['date', 'equipment_number', 'running_time']
    df.replace('', pd.NA, inplace=True)
    df = df.dropna(subset=['equipment_number'])

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
            EquipmetRunningTime.objects.get_or_create(
                equipment=equipment,
                date=date,
                defaults={'running_time': running_time},
                )
