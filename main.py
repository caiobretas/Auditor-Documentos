'''main class'''
import os

import fitz

from controllers.drive import Drive
from controllers.pymupdf import BytesReader
from models.date_compiler import DateCompiler

os.system('clear')
os.system(f'export OPENAI_API_KEY={os.environ.get("OPENAI_API_KEY")}')

from repositories.base import Repository
from repositories.document import Vigency

# os.system('pip install --upgrade -r requirements.txt')

drive = Drive()
bytes_reader = BytesReader()
session = Repository.start_session()
repositoryVigency = Vigency(session)

docs_mapping = repositoryVigency.get_mapper('googleid')

problems = []
more_than_one_date = []

for google_id, doc in docs_mapping.items():

    document, document_str, document_bytes = None, None, None

    document_bytes = drive.get_file_media_by_id(google_id)

    if not document_bytes:
        print(f'Document not found - {google_id}')
        continue
    try:
        document_str, document = bytes_reader.read_document(document_bytes)
    except fitz.FileDataError:
        problems.append((document_str, google_id))
        continue

    date_compiler = DateCompiler(document_str, google_id)
    try:
        date = date_compiler.compile_date()
    except KeyError:
        more_than_one_date.append((document_str, google_id))
        continue

    with open(f'documents/{date}:{google_id}.txt', 'w', encoding='utf8') as f:
        f.write(document_str)

for document_str, document in problems:
    print('-'*50)
    print('problems')
    print(f'ID: {document}', '\n', f'String: {document_str}')
