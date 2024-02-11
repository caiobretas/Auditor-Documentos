import os

from googleapiclient.discovery import build

KEY = os.environ.get('GOOGLE_DRIVE_KEY')

class Drive:
    '''classe responsável pelas requisições com a Google'''
    def __init__(self):
        self.client = build('drive', 'v3', developerKey=KEY)
