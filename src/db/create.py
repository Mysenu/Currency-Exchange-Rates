from sqlalchemy import MetaData, Table, Column, INTEGER, TEXT, ForeignKey

from .configs import engine, DB_PATH

metadata = MetaData(engine)

currency_table = Table(
    'currency', metadata,
    Column('code', TEXT, primary_key=True, nullable=False),
    Column('name', TEXT, nullable=False)
)

rate_table = Table(
    'rate', metadata,
    Column('code', TEXT, ForeignKey('currency.code'), nullable=False),
    Column('value', INTEGER, nullable=False),
    Column('date', TEXT, nullable=False)
)

if not DB_PATH.exists() or DB_PATH.stat().st_size == 0:
    metadata.create_all()
