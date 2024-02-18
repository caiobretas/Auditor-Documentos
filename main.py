# type:ignore
'''main class'''
import datetime
import os
import warnings
from typing import Dict

import fitz
import pandas

from controllers.drive import Drive
from controllers.pymupdf import BytesReader
from entities.contact import Contact as Ctt
from entities.document import Category as Cat
from entities.document import Document as Doc
from entities.document import Vigency as Vig
from models.compilers import DateCompiler, PartCompiler
from models.system import System
from repositories import contact as ctt
from repositories import document as doc
from repositories.base import Repository

os.system('clear')
warnings.filterwarnings('ignore', category=UserWarning)
# os.system(f'export OPENAI_API_KEY={os.environ.get("OPENAI_API_KEY")}')

DOCUMENTS_PATH = 'documents/'

# vamos instanciar algumas classes úteis para a lógica
drive = Drive()  # classe responsável por interações com o Google Drive
date_compiler = DateCompiler()
part_compiler = PartCompiler()
bytes_reader = BytesReader()  # classe resonsável por interações com o PyMuPDF
system_reader = System()

session = Repository.start_session()  # sessão para o banco de dados
repositoryVigency = doc.Vigency(session)  # classe de repositório
repositoryDocuments = doc.Document(session)
repositoryCategory = doc.Categories(session)
repositoryContacts = ctt.Contact(session)

# # abaixo, vamos definir alguns mappings úteis

# documentos
docs_mapping: Dict[str, Doc] = repositoryDocuments.\
    get_mapper('googleid')
docs_vigency_mapping: Dict[str, Vig] = repositoryVigency.\
    get_mapper('googleid')
docs_categories_mapping: Dict[str, Cat] = repositoryCategory.\
    get_mapper('googleid')

# contatos
contacts_mapping: Dict[str, Ctt] = repositoryContacts.get_mapper('id')

# arquivos salvos local
downloaded_files_mapping = {
    google_id.split('.')[0]:
        system_reader.read_file(f'{DOCUMENTS_PATH + google_id}')
    for google_id in system_reader.get_files(DOCUMENTS_PATH)
}

result: list[dict] = []
# iteração sobre todos os documentos que temos salvo em banco
for google_id, document in docs_vigency_mapping.items():

    FILE_PATH = DOCUMENTS_PATH + f'{google_id}.txt'

    result_dict = {}

    result_dict['google_id'] = google_id
    result_dict['link'] = docs_mapping[google_id].weblink

    document_str, document_bytes = None, None

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
            document_str = bytes_reader.read_document(document_bytes)[0]

            # salva o arquivo para não ter que baixar novamente
            with open(FILE_PATH, 'w', encoding='utf8') as f:
                f.write(document_str)

        # trata um erro de file data
        except fitz.FileDataError:
            result_dict['result'] = 'file data error'
            result.append(result_dict)
            continue

    # lê o arquivo e retorna a string dele
    document_str = System.read_file(FILE_PATH)

    # # Estação de comparação de datas.

    # Compilador encontra a data na string.
    date, date_status = '', ''
    date, date_status = date_compiler.\
        compile_date_regexp(document_str=document_str)

    if isinstance(date, datetime.date):
        if date != document.data_assinatura:
            date_status = 'wrong date'

    result_dict.update({
        'date': date,
        'date_status': date_status
    })

    # # Estação de verificação de parte.

    # O modelo AI verifica se a parte está correta

    saved_part_id = docs_categories_mapping[google_id].categoria5
    saved_part = contacts_mapping.get(saved_part_id)

    if saved_part:  # busca tanto o nome qto o nome amigável
        saved_part_names = [
            saved_part.nomeamigavel,
            saved_part.nome
        ]

    else:
        saved_part_names = [None, None]

    part, part_status = '', ''
    part, part_status = part_compiler.compile_part_model(
        FILE_PATH,
        *saved_part_names)

    if part == 'não':  # se não encontrar a parte no documento
        if not saved_part_id:  # e não tiver id da parte cadastrado no doc
            part, part_status = None, 'no part found'
        part, part_status = saved_part, 'wrong'

    result_dict.update({
        'part': part,
        'part_status': part_status
    })

    result.append(result_dict)

    result_str = ''.\
        join([f'\n{k}= {v}' for k, v in result_dict.items()])

    print(result_str)
result_dataframe = pandas.DataFrame(result)
result_dataframe.to_excel('result.xlsx', index=False, engine='openpyxl')
print(result_dataframe)
