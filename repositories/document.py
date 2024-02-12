'''módulo com as entidades repositorio Document '''
import os
from abc import ABC, abstractmethod
from typing import Literal

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from entities import document


class Repository:
    '''classe base para as classes repositorio'''
    engine = create_engine(
            f"postgresql://{os.getenv('DB_USER')}:"
            f"{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}/"
            f"{os.getenv('DB_NAME')}"
        )


class DocumentRepository(ABC, Repository):
    '''classe base para as classes repositorio'''
    @abstractmethod
    def get_mapper(self) -> dict:
        '''método abstrato - retorna o mapeamento dos objetos do repositorio'''
    @abstractmethod
    def get_by_id(self, document_id: str = ''):
        '''retorna um objeto Document'''
    @abstractmethod
    def get_all(self, document_id: str = ''):
        '''retorna todos os objetos presentes'''


class Document(DocumentRepository):
    '''representa a tabela documents'''
    def __init__(self):
        self.session = Session(self.engine)

    def get_by_id(self, document_id: str = ''):
        return self.session.get(Document, document_id)

    def get_all(self, document_id: str = ''):
        '''retorna todos os objetos presentes'''
        if document_id not in ('', None):
            r
        else:
            return self.session.query(Document).all()

    def get_mapper(self, pkey: Literal['id', 'googleid'] = 'id') -> dict:

        objs = self.get_document()

        if not objs:
            print('No Document found')
            return {}

        if pkey == 'googleid':
            return {obj.googleid: obj for obj in objs}

        elif pkey == 'id':
            return {obj.id: obj for obj in objs}

    def __repr__(self):
        attrs = ', '.join([f"{key}={value!r}"
                           for key, value in vars(self).items()
                           if not key.startswith('_')])
        return f'{self.__class__.__name__}({attrs})'
