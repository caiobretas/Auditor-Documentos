# pylint: disable=useless-super-delegation
'''módulo com as entidades repositorio Document '''
from abc import ABC, abstractmethod
from typing import Literal

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from entities import document

from .base import Repository


class DocumentRepository(ABC, Repository):
    '''classe base para as classes repositorio'''
    def __init__(self, session: Session):
        self._session = session

    @abstractmethod
    def get_all(self):
        '''retorna todos os objetos presentes'''
    @abstractmethod
    def get_by_id(self, document_id: str = ''):
        '''retorna um objeto Document'''
    @abstractmethod
    def get_mapper(self, pkey: Literal['id', 'googleid'] = 'id') -> dict:
        '''método abstrato - retorna o mapeamento dos objetos do repositorio'''


class Document(DocumentRepository):
    '''representa a tabela documents'''

    def __init__(self, session):
        super().__init__(session)

    def get_all(self):
        return self._session.query(document.Document).\
            where(document.Document.type == 'application/pdf').all()

    def get_by_id(self, document_id: str = ''):
        return self._session.get(Document, document_id)

    def get_mapper(self, pkey: Literal['id', 'googleid'] = 'id') -> dict:
        objs = self.get_all()

        if pkey == 'googleid':
            return {obj.googleid: obj for obj in objs}
        elif pkey == 'id':
            return {obj.id: obj for obj in objs}

    def get_googleid_mapping(self):
        '''retorna um mapping do id e google id'''
        mapping = self.get_mapper()
        return {obj.id: obj.googleid for obj in mapping.values()}


class Vigency(DocumentRepository):
    '''representa a tabela documents'''
    def __init__(self, session: Session):
        super().__init__(session)

    def get_all(self):
        return self._session.query(document.Vigency).all()

    def get_by_id(self, document_id: str = ''):
        return self._session.get(Vigency, document_id)

    def get_mapper(self, pkey: Literal['id', 'googleid'] = 'id') -> dict:
        objs = self.get_all()

        if pkey == 'googleid':
            googleid_mapping = Document(self._session).get_googleid_mapping()
            return {
                googleid_mapping[obj.id]: obj
                for obj in objs if obj.id in googleid_mapping.keys()
            }
        elif pkey == 'id':
            return {obj.id: obj for obj in objs}


class Categories(DocumentRepository):
    '''representa a tabela documents'''
    def __init__(self, session: Session):
        super().__init__(session)

    def get_all(self):
        return self._session.query(document.Category).all()

    def get_by_id(self, document_id: str = ''):
        return self._session.get(document.Category, document_id)

    def get_mapper(self, pkey: Literal['id', 'googleid'] = 'id') -> dict:
        objs = self.get_all()

        if pkey == 'googleid':
            googleid_mapping = Document(self._session).get_googleid_mapping()
            return {googleid_mapping[obj.id]: obj for obj in objs}
        elif pkey == 'id':
            return {obj.id: obj for obj in objs}
