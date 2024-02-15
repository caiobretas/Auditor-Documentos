from io import IOBase

from fitz import Document, fitz


class BytesReader:
    '''Classe responsável por ler os bytes de um documento pdf
    Retorna o objeto e sua String correspondente'''
    def __init__(self):
        self.position = 0

    def read_document(self, bytes_obj: IOBase) -> tuple[str, Document]:

        pdf_document: Document = fitz.open('pdf', bytes_obj.read())
        text = ''
        for page in pdf_document:
            text += page.get_text()
        return text, pdf_document
    