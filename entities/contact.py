'''módulo com as entidades Document '''
from datetime import date, datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    '''classe base para os mappings SQLALCHEMY'''


class Contact(Base):
    '''representa a tabela documents'''

    __tablename__ = 'contacts'
    __table_args__ = ({'schema': 'h_resources'})

    id: Mapped[str] = mapped_column(primary_key=True)
    idpessoa: Mapped[str]
    nome: Mapped[str]
    cpfcnpj: Mapped[str]
    nomefantasia: Mapped[str]
    logradouro: Mapped[str]
    nro: Mapped[str]
    complemento: Mapped[str]
    bairro: Mapped[str]
    cep: Mapped[str]
    cidade: Mapped[str]
    uf: Mapped[str]
    nomepais: Mapped[str]
    ativo: Mapped[bool]
    email: Mapped[str]
    telefone: Mapped[str]
    cliente: Mapped[bool]
    fornecedor: Mapped[bool]
    sexo: Mapped[str]
    rg: Mapped[str]
    orgaoemissorrg: Mapped[str]
    ufemissorrg: Mapped[str]
    clientedesde: Mapped[str]
    idclassificacaopreferencial: Mapped[str]
    idcentrocustopreferencial: Mapped[str]
    observacoes: Mapped[str]
    chavepix: Mapped[str]
    tipochavepix: Mapped[str]
    emailsecundario: Mapped[str]
    nomeamigavel: Mapped[str]
    datanascimento: Mapped[datetime]

    def __repr__(self):
        attrs = ', '.join([f"{key}={value!r}"
                           for key, value in vars(self).items()
                           if not key.startswith('_')])
        return f'{self.__class__.__name__}({attrs})'
