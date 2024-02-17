'''main class'''
import datetime
import logging

import fitz
import pandas

from controllers.drive import Drive
from controllers.gpt import GPT
from controllers.pymupdf import BytesReader
from models.compilers import DateCompiler
from models.system import System
from repositories.base import Repository
from repositories.document import Categories, Document, Vigency

# os.system('clear')
# os.system(f'export OPENAI_API_KEY={os.environ.get("OPENAI_API_KEY")}')

DOCUMENTS_PATH = 'documents/'

# vamos instanciar algumas classes úteis para a lógica
drive = Drive()  # classe responsável por interações com o Google Drive
compiler = DateCompiler()
bytes_reader = BytesReader()  # classe resonsável por interações com o PyMuPDF
system_reader = System()

session = Repository.start_session()  # sessão para o banco de dados
repositoryVigency = Vigency(session)  # classe de repositório
repositoryDocuments = Document(session)  # classe de repositório
repositoryCategory = Categories(session)

# abaixo, vamos definir alguns mappings úteis
docs_mapping = repositoryDocuments.get_mapper('googleid')
docs_vigency_mapping = repositoryVigency.get_mapper('googleid')
docs_categories_mapping = repositoryCategory.get_mapper('googleid')

downloaded_files_mapping = {
    google_id.split('.')[0]:
        system_reader.read_file(f'{DOCUMENTS_PATH + google_id}')
    for google_id in system_reader.get_files(DOCUMENTS_PATH)
}

result: list[dict] = []
for google_id, doc in docs_vigency_mapping.items():

    FILE_PATH = DOCUMENTS_PATH + f'{google_id}.txt'

    result_dict = {}
    result_dict['doc'] = doc
    result_dict['google_id'] = google_id
    result_dict['link'] = docs_mapping[google_id].weblink

    document, document_str, document_bytes = None, None, None

    # verifica se o arquivo ainda não foi baixado
    if google_id not in downloaded_files_mapping.keys():

        # extrai os bytes do arquivo
        document_bytes = drive.get_file_media_by_id(google_id)

        if not document_bytes:
            result_dict['result'] = 'document not found'
            result.append(result_dict)
            continue

        try:

            # tenta transformar os bytes em string
            document_str, document = bytes_reader.read_document(document_bytes)

            # salva o arquivo para não ter que baixar novamente
            with open(FILE_PATH, 'w', encoding='utf8') as f:
                f.write(document_str)

        # trata um erro de file data
        except fitz.FileDataError:
            # problems.append((document_str, google_id))
            result_dict['result'] = 'file data error'
            result.append(result_dict)
            continue

    document_str = System.read_file(FILE_PATH)

    # Estação de comparação de datas. O Compilador encontra a data na string.
    date, date_status = compiler.compile_date_regexp(document_str=document_str)

    if isinstance(date, datetime.date):
        if date != doc.data_assinatura:
            date_status = 'wrong date'


    # if not isinstance(date, datetime.date):
    #     result_dict['signature_date_result'] = date
    #     continue

    if doc.data_assinatura != date:
        result_dict['signature_date_result'] = 'wrong date'
        result.append(result_dict)
        continue

    # #  falta try catch
    # part = compiler.compile_part()

    result_dict['signature_date_result'] = 'ok'
    result.append(result_dict)

result_dataframe = pandas.DataFrame(result)
result_dataframe.to_excel('result.xlsx', index=False, engine='openpyxl')
print(result_dataframe)

# for document_str, document in problems:
#     print('-'*50)
#     print('problems')
#     print(f'ID: {document}', '\n', f'String: {document_str}')
