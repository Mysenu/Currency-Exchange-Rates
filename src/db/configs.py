import os
from pathlib import Path

from sqlalchemy import create_engine

default_db_path = Path(__file__).parent / '..' / '..' / 'database' / 'currencies.db'
DB_PATH = Path(os.environ.get('CURRENCY_DB_PATH', default_db_path))

try:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
except OSError:
    raise

engine = create_engine(f'sqlite:///{DB_PATH}', future=True)
