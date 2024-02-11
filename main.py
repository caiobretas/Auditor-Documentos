'''main class'''
import os
import re

from controllers.drive import Drive
from controllers.pymupdf import BytesReader

os.system('clear')
os.system(f'export OPENAI_API_KEY={os.environ.get("OPENAI_API_KEY")}')

file_id = '1Cf47MCZInGnhGXzGbdBeXelfamZ9PU81'
document_bytes, document_id = Drive().get_file_media_by_id(file_id)

if document_bytes:
    document_str, document = BytesReader().read_document(document_bytes)
    with open(f'documents/{document_id}.txt', 'w', encoding='utf8') as f:
        f.write(document_str)

padroes = [
    # Para o formato "DD/MM/YYYY"
    r"Rio de Janeiro,"
    r"\s+(\d{2}/\d{2}/\d{4})",
    # Para o formato "DD de mês de YYYY"
    r"Rio de Janeiro,"
    r"\s+(\d{1,2})\s+de\s+(janeiro|fevereiro|março|abril|maio|junho|"
    r"julho|agosto|setembro|outubro|novembro|dezembro)\s+de\s+(\d{4})"
]

padroes_compilados = [re.compile(padrao, re.IGNORECASE) for padrao in padroes]
datas_encontradas = []
for pc in padroes_compilados:
    datas_encontradas.extend(pc.findall(document_str))
print(datas_encontradas)
