# type:ignore
"""main class"""
import logging
import os
import warnings
from typing import Dict

import fitz

from controllers.drive import Drive
from controllers.pymupdf import BytesReader
from entities.contact import Contact as Ctt
from entities.document import Category as Cat
from entities.document import Document as Doc
from entities.document import Vigency as Vig
from models.system import System
from repositories import contact as ctt
from repositories import document as doc
from repositories.base import Repository

# os.system('clear')
# os.system(f'export OPENAI_API_KEY={os.environ.get("OPENAI_API_KEY")}')
warnings.filterwarnings("ignore", category=UserWarning)

DOCUMENTS_PATH = "documents/"

# vamos instanciar algumas classes úteis para a lógica
drive = Drive()  # classe responsável por interações com o Google Drive
bytes_reader = BytesReader()  # classe resonsável por interações com o PyMuPDF
system_reader = System()

session = Repository.start_session()  # sessão para o banco de dados

# vamos inicializar os reposotórios
repositoryVigency = doc.Vigency(session)  # classe de repositório
repositoryDocuments = doc.Document(session)
repositoryCategory = doc.Categories(session)
repositoryContacts = ctt.Contact(session)

# # abaixo, vamos definir alguns mappings úteis

# documentos
docs_mapping: Dict[str, Doc] = repositoryDocuments.get_mapper("googleid")
docs_vigency_mapping: Dict[str, Vig] = repositoryVigency.get_mapper("googleid")
docs_categories_mapping: Dict[str, Cat] = repositoryCategory.get_mapper("googleid")

# contatos
contacts_mapping: Dict[str, Ctt] = repositoryContacts.get_mapper("id")

# arquivos salvos localmente
downloaded_files_mapping = {
    google_id.split(".")[0]: system_reader.read_file(f"{DOCUMENTS_PATH + google_id}")
    for google_id in system_reader.get_files(DOCUMENTS_PATH)
}

result: list[dict] = []
# iteração sobre todos os documentos que temos salvo em banco
for google_id, document in docs_vigency_mapping.items():

    FILE_PATH = DOCUMENTS_PATH + f"{google_id}.txt"

    document_str, document_bytes = None, None

    # verifica se o arquivo ainda não foi baixado
    if google_id not in downloaded_files_mapping.keys():

        # extrai os bytes do arquivo
        document_bytes = drive.get_file_media_by_id(google_id)

        if not document_bytes:
            continue

        try:

            # tenta transformar os bytes em string
            document_str = bytes_reader.read_document(document_bytes)[0]

            if not document_str:
                print("Empty document", google_id)
                continue

            # salva o arquivo para não ter que baixar novamente
            with open(FILE_PATH, "w", encoding="utf8") as f:
                f.write(document_str)
                print("Written document", google_id)

        # trata um erro de file data
        except fitz.FileDataError:
            logging.error("file data error")
            continue
