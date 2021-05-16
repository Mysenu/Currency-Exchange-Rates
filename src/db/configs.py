import os
from pathlib import Path

from sqlalchemy import create_engine, event

from .functions import Median, dateID

default_db_path = Path(__file__).parent / '..' / '..' / 'database' / 'currencies.db'
DB_PATH = Path(os.environ.get('CURRENCY_DB_PATH', default_db_path))

try:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
except OSError:
    raise

engine = create_engine(f'sqlite:///{DB_PATH}', future=True)


@event.listens_for(engine, 'connect')
def registerFunction(dbapi_connection, connection_record):
    dbapi_connection.create_aggregate('median', 1, Median)
    dbapi_connection.create_function('dateid', 3, dateID)
