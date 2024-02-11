'''módulo de auth'''
import os.path
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

TOKEN_PATH = f'{Path(__file__).parent}/' + 'token.json'
CREDS_PATH = f'{Path(__file__).parent}/' + 'credentials.json'
# Se modificar os SCOPES, delete token.json
SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/gmail.modify',
        'https://www.googleapis.com/auth/gmail.compose',
        'https://www.googleapis.com/auth/gmail.send',
        'https://mail.google.com/',
        'https://www.googleapis.com/auth/documents',        
        'https://www.googleapis.com/auth/documents.readonly',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive.readonly',
        'https://www.googleapis.com/auth/drive.appdata',
        'https://www.googleapis.com/auth/drive.metadata',
        'https://www.googleapis.com/auth/drive.metadata.readonly',
        'https://www.googleapis.com/auth/drive.photos.readonly',
    ]


def main():
    """Responsável pelo Flow de Auth"""
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    # se não tiver credencial, o usuário faz login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=8080)
    # Save the credentials for the next run
    with open(TOKEN_PATH, "w", encoding='utf8') as token:
        token.write(creds.to_json())
    return creds


CREDS = main()
