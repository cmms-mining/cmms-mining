import os
import pickle

from google.auth.transport.requests import Request

from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import Resource, build


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
