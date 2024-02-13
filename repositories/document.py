'''módulo com as entidades repositorio Document '''
import os
from abc import ABC, abstractmethod
from typing import Dict, Literal

from base import Repository
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from entities import document


class DocumentRepository(ABC, Repository):
    '''classe base para as classes repositorio'''
    @abstractmethod
    def get_mapper(self, pkey: Literal['id', 'googleid'] = 'id') -> dict:
        '''método abstrato - retorna o mapeamento dos objetos do repositorio'''
    @abstractmethod
    def get_all(self):
        '''retorna todos os objetos presentes'''
    @abstractmethod
    def get_by_id(self, document_id: str = ''):
        '''retorna um objeto Document'''


class Document(DocumentRepository):
    '''representa a tabela documents'''
    def __init__(self):
        self.session = Session(self.engine)

    def get_all(self):
        return self.session.query(document.Document).all()

    def get_by_id(self, document_id: str = ''):
        return self.session.get(Document, document_id)

    def get_mapper(self, pkey: Literal['id', 'googleid'] = 'id') -> dict:
        objs = self.get_all()
        if pkey == 'googleid':
            return {obj.googleid: obj for obj in objs}
        elif pkey == 'id':
            return {obj.id: obj for obj in objs}


class Document(DocumentRepository):
    '''representa a tabela documents'''
    def __init__(self):
        self.session = Session(self.engine)

    def get_all(self):
        return self.session.query(document.Document).all()

    def get_by_id(self, document_id: str = ''):
        return self.session.get(Document, document_id)

    def get_mapper(self, pkey: Literal['id', 'googleid'] = 'id') -> dict:
        objs = self.get_all()
        if pkey == 'googleid':
            return {obj.googleid: obj for obj in objs}
        elif pkey == 'id':
            return {obj.id: obj for obj in objs}