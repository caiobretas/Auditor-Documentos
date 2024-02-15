'''main class'''
import os

import fitz
import pandas

from controllers.drive import Drive
from controllers.pymupdf import BytesReader
from models.date_compiler import DateCompiler
from models.sys_reader import SystemReader
from repositories.base import Repository
from repositories.document import Document, Vigency

os.system('clear')
os.system(f'export OPENAI_API_KEY={os.environ.get("OPENAI_API_KEY")}')

DOCUMENTS_PATH = 'documents/'

# vamos instanciar algumas classes úteis para a lógica
drive = Drive()  # classe responsável por interações com o Google Drive
bytes_reader = BytesReader()  # classe resonsável por interações com o PyMuPDF
system_reader = SystemReader()

session = Repository.start_session()  # sessão para o banco de dados
repositoryVigency = Vigency(session)  # classe de repositório
repositoryDocuments = Document(session)  # classe de repositório

# abaixo, vamos definir alguns mappings úteis
docs_mapping = repositoryDocuments.get_mapper('googleid')
docs_vigency_mapping = repositoryVigency.get_mapper('googleid')

downloaded_files_mapping = {
    google_id.split('.')[0]:
        system_reader.read_file(f'{DOCUMENTS_PATH + google_id}')
    for google_id in system_reader.get_files(DOCUMENTS_PATH)
}

# docs_bytes_mapping = {
#     google_id: drive.get_file_media_by_id(google_id)
#     for google_id in docs_vigency_mapping.keys()
# }

result: list[dict] = []
for google_id, doc in docs_vigency_mapping.items():

    result_dict = {}
    result_dict['doc'] = doc
    result_dict['google_id'] = google_id
    result_dict['link'] = docs_mapping[google_id].weblink

    document, document_str, document_bytes = None, None, None

    # verifica se o arquivo ainda não foi baixado
    if google_id not in downloaded_files_mapping.keys():

        document_bytes = drive.get_file_media_by_id(google_id)

        if not document_bytes:
            result_dict['result'] = 'document not found'
            result.append(result_dict)
            continue

        try:

            document_str, document = bytes_reader.read_document(document_bytes)
            # salva o arquivo para não ter que baixar novamente
            with open(
                    f'{DOCUMENTS_PATH + google_id}.txt',
                    'w',
                    encoding='utf8') as f:
                f.write(document_str)

        except fitz.FileDataError:
            # problems.append((document_str, google_id))
            result_dict['result'] = 'file data error'
            result.append(result_dict)
            continue

    else:  # caso o arquivo já tenha sido baixado
        document_str = SystemReader.read_file(
            DOCUMENTS_PATH + google_id + '.txt'
        )

    date_compiler = DateCompiler(document_str, google_id)

    try:
        date = date_compiler.compile_date()
    except KeyError:
        # more_than_one_date.append((document_str, google_id))
        result_dict['result'] = 'more than one date'
        result.append(result_dict)
        continue

    if doc.data_assinatura != date:
        result_dict['result'] = 'wrong date'
        result.append(result_dict)
        continue

    result_dict['result'] = 'ok'
    result.append(result_dict)

result_dataframe = pandas.DataFrame(result)
result_dataframe.to_excel('result.xlsx', index=False, engine='openpyxl')
print(result_dataframe)

# for document_str, document in problems:
#     print('-'*50)
#     print('problems')
#     print(f'ID: {document}', '\n', f'String: {document_str}')
