import os

from googleapiclient.discovery import Resource, build

from auth.google_auth import CREDS

KEY = os.environ.get('GOOGLE_DRIVE_KEY')

class Drive:
    '''classe responsável pelas requisições com a Google'''
    def __init__(self):
        self.client: Resource = build('drive', 'v3', credentials=CREDS)


drive = Drive()
