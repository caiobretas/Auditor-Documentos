'''modulo base para as classes repositorio'''
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

ENV_PATH = Path(__file__).parent.parent / '.env'
load_dotenv(ENV_PATH)

class Repository:
    '''classe base para as classes repositorio'''

    _engine = None

    @staticmethod
    def start_session():
        '''inicia a sessao de conexao com o banco de dados'''
        if not Repository._engine:
            return Session(Repository.start_engine())
        return Session(Repository._engine)

    @staticmethod
    def start_engine() -> Engine:
        '''cria a engine de conexao com o banco de dados'''
        Repository._engine = create_engine(
                f"postgresql://{os.getenv('DB_USER')}:"
                f"{os.getenv('DB_PASSWORD')}@"
                f"{os.getenv('DB_HOST')}/"
                f"{os.getenv('DB_NAME')}"
            )
        return Repository._engine
