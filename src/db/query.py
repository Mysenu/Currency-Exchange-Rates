import datetime

from sqlalchemy import select, exists

from .configs import engine
from .create import currency_table, rate_table


def insertCurrencyCode(code: str, name: str):
    currency_code = {'code': code, 'name': name}

    with engine.connect() as conn:
        conn.execute(currency_table.insert().prefix_with('OR IGNORE'), currency_code)
        conn.commit()


def dateExists(date: datetime):
    with engine.connect() as conn:
        query = select(exists().where(rate_table.c.date == date))
        res = conn.execute(query).scalar()
    return res


def insertValueCurrency(code: str, value: int, date: datetime):
    value_currency = {'code': code, 'value': value, 'date': date}

    with engine.connect() as conn:
        conn.execute(rate_table.insert(), value_currency)
        conn.commit()
