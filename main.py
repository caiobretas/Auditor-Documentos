'''main class'''
import os

from controllers.drive import Drive
from controllers.pymupdf import BytesReader
from models.date_compiler import DateCompiler

os.system('clear')
os.system(f'export OPENAI_API_KEY={os.environ.get("OPENAI_API_KEY")}')
# os.system('pip install --upgrade -r requirements.txt')

# file_id = '1Cf47MCZInGnhGXzGbdBeXelfamZ9PU81'
# file_id = '1ZUuB2vZlELOVxo2heZfxK_yBa5MLtZRU'
# file_id = '1zsTrCG1hPGZFjlzJeSA6m7JEPRBDpd38'
# file_id = '1ZKaPqJHjOW9mzwYEVwr6eR35p5Jn-nHk'
# file_id = '1ZdyzJYrMPEv-sVXdx1LCooP4V5CjZFjw'
# file_id = '1ZblEw5EYcmLiW3QDqvR5btIEC41wLcaa'
file_id = '1QpYUQF0cjmYdVghoZ0n-mHjB4C60NLOv'
# https://drive.google.com/file/d/1QpYUQF0cjmYdVghoZ0n-mHjB4C60NLOv/view?usp=drivesdk

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
