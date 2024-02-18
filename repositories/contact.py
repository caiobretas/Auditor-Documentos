# pylint: disable=useless-super-delegation
'''módulo com as entidades repositorio Contact '''
from abc import ABC, abstractmethod
from typing import Literal

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from entities import contact

from .base import Repository


class ContactRepository(ABC, Repository):
    '''classe base para as classes repositorio'''
    def __init__(self, session: Session):
        self._session = session

    @abstractmethod
    def get_all(self):
        '''retorna todos os objetos presentes'''
    @abstractmethod
    def get_by_id(self, contact_id: str = ''):
        '''retorna um objeto Contact'''
    @abstractmethod
    def get_mapper(self, pkey: Literal['id', 'googleid'] = 'id') -> dict:
        '''método abstrato - retorna o mapeamento dos objetos do repositorio'''


class Contact(ContactRepository):
    '''representa a tabela contacts'''

    def __init__(self, session):
        super().__init__(session)

    def get_all(self):
        return self._session.query(contact.Contact).all()

    def get_by_id(self, contact_pkey: str = ''):
        return self._session.get(Contact, contact_pkey)

    def get_mapper(self, pkey: Literal['id', 'googleid'] = 'id') -> dict:
        objs = self.get_all()
        return {obj.id: obj for obj in objs}
