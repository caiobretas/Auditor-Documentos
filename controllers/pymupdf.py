from io import IOBase

import fitz


class BytesReader:

    def __init__(self, bytes_obj: IOBase):
        self.bytes_obj = bytes_obj
        self.position = 0

    def read(self):
        fh: IOBase = self.bytes_obj
        pdf_document = fitz.open('pdf', fh.read())
        print(pdf_document)
