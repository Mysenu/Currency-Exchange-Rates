from sqlalchemy import MetaData, Table, Column, INTEGER, TEXT, ForeignKey

from .configs import engine, DB_PATH


metadata = MetaData(engine)

currency_codes_table = Table(
    'currency_codes', metadata,
    Column('code', TEXT, primary_key=True, nullable=False),
    Column('name', TEXT, nullable=False)
)

value_currencies_table = Table(
    'value_currencies', metadata,
    Column('code', TEXT, ForeignKey('currency_codes.code'), nullable=False),
    Column('value', INTEGER, nullable=False),
    Column('date', TEXT, nullable=False)
)

if not DB_PATH.exists() or DB_PATH.stat().st_size == 0:
    metadata.create_all()
