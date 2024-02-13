'''modulo base para as classes repositorio'''
import os

from sqlalchemy import create_engine


class Repository:
    '''classe base para as classes repositorio'''
    engine = create_engine(
            f"postgresql://{os.getenv('DB_USER')}:"
            f"{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}/"
            f"{os.getenv('DB_NAME')}"
        )
