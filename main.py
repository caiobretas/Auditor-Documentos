'''main class'''
import os

from controllers.drive import Drive
from controllers.pymupdf import BytesReader
from models.date_compiler import DateCompiler

os.system('clear')
os.system(f'export OPENAI_API_KEY={os.environ.get("OPENAI_API_KEY")}')
# os.system('pip install --upgrade -r requirements.txt')

file_id = '1QpYUQF0cjmYdVghoZ0n-mHjB4C60NLOv'

drive = Drive()
bytes_reader = BytesReader()

document_bytes, document_id = drive.get_file_media_by_id(file_id)

if not document_bytes:
    raise ValueError('Document not found')

document_str, document = bytes_reader.read_document(document_bytes)
date_compiler = DateCompiler(document_str, document_id)
date_compiler.compile_dates()




with open(f'documents/{document_id}.txt', 'w', encoding='utf8') as f:
    f.write(document_str)
