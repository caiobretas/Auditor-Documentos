'''módulo com as entidades Document '''
# from typing import List, Optional
from datetime import date, datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    '''classe base para os mappings SQLALCHEMY'''


class Document(Base):
    '''representa a tabela documents'''

    __tablename__ = 'documents'
    __table_args__ = {'schema': 'legal'}

    id: Mapped[str] = mapped_column(primary_key=True)
    googleid: Mapped[str]
    name: Mapped[str]
    type: Mapped[str]
    drive: Mapped[str]
    path: Mapped[str]
    weblink: Mapped[str]
    createdtime: Mapped[datetime]
    modifiedtime: Mapped[datetime]
    parents: Mapped[str]
    trashed: Mapped[bool]

    def __repr__(self):
        attrs = ', '.join([f"{key}={value!r}"
                           for key, value in vars(self).items()
                           if not key.startswith('_')])
        return f'{self.__class__.__name__}({attrs})'


class DocumentVigency(Base):
    '''representa a tabela signatures'''

    __tablename__ = 'vigencies'
    __table_args__ = {'schema': 'legal'}

    id: Mapped[str] = mapped_column(primary_key=True)
    data_assinatura: Mapped[date]
    datainicial_vigencia: Mapped[date]
    datafinal_vigencia: Mapped[date]
    licenciamento: Mapped[bool]
    aprovacao_conselho: Mapped[bool]
    aprovacao_assembleia: Mapped[bool]
    clausula_exclusividade: Mapped[str]
    id_documento_original: Mapped[str]

    def __repr__(self):
        attrs = ', '.join([f"{key}={value!r}"
                           for key, value in vars(self).items()
                           if not key.startswith('_')])
        return f'{self.__class__.__name__}({attrs})'


class DocumentCategory(Base):
    '''representa a tabela categories'''

    __tablename__ = 'categories'
    __table_args__ = {'schema': 'legal'}

    id: Mapped[str] = mapped_column(primary_key=True)
    categoria1: Mapped[str]
    categoria2: Mapped[str]
    categoria3: Mapped[str]
    categoria4: Mapped[str]
    categoria5: Mapped[str]
    superados: Mapped[str]

    def __repr__(self):
        attrs = ', '.join([f"{key}={value!r}"
                           for key, value in vars(self).items()
                           if not key.startswith('_')])
        return f'{self.__class__.__name__}({attrs})'


if __name__ == '__main__':
    doc = Document(id=1)
    cat = DocumentCategory(id=1)
    vig = DocumentVigency(id=1)
    print(vars(doc))
    print(doc, cat, vig)
