import io
import logging
import os
from typing import Tuple, Union

from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from auth.google_auth import CREDS

KEY = os.environ.get('GOOGLE_DRIVE_KEY')


class Drive:
    '''classe responsável pelas requisições com a Google'''
    def __init__(self):
        self.service = build('drive', 'v3', credentials=CREDS)

    def get_file_media_by_id(self,
                             file_id: str) -> Union[None, io.BytesIO]:
        """Retorna um objeto ByteIO pelo seu ID."""
        try:
            request = self.service.files().get_media(
                fileId=file_id,
                supportsAllDrives=True
            )
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(
                    f"Document: {file_id}\n"
                    f"  download progress: {status.progress() * 100}"
                )

            fh.seek(0)
            return fh

        except HttpError as he:
            # logging.error(he)
            return None

    def get_files_by_folder_id(self, folder_id):
        """Listar todos os arquivos em um diretório e subdiretórios."""
        try:
            query = f"'{folder_id}' in parents"

            response = self.service.files().list(
                q=query,
                spaces='drive',
                fields='nextPageToken, files(*)',  # Retorna todos os campos
                pageToken=None,
                pageSize=1000,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True).execute()
            return response.get('files')

        except HttpError as he:
            logging.error(he)
