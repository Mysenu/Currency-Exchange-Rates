import datetime

from sqlalchemy import select, exists

from .configs import engine
from .create import currency_codes_table, value_currencies_table


def insertCurrencyCode(code: str, name: str):
    currency_code = {'code': code, 'name': name}

    with engine.connect() as conn:
        conn.execute(currency_codes_table.insert(), currency_code)
        conn.commit()


def checkValueData(data: str):
    with engine.connect() as conn:
        query = select(exists().where(value_currencies_table.c.data == data))
        res = conn.execute(query).scalar()
    return res


def insertValueCurrency(code: str, value: int, data: str):
    if checkValueData(data):
        return

    value_currency = {'code': code, 'value': value, 'data': data}

    with engine.connect() as conn:
        conn.execute(value_currencies_table.insert(), value_currency)
        conn.commit()


def getValueCurrency(code: str, data: str):
    with engine.connect() as conn:
        query = select(exists().where(value_currencies_table.c.data == data and value_currencies_table.c.code == code))
        res = conn.execute(query)
    return res


def checkCurrencyCode(code: str):
    with engine.connect() as conn:
        query = select(exists().where(currency_codes_table.c.code == code))
        res = conn.execute(query).scalar()
    return res


def checkCurrencyName(name: str):
    with engine.connect() as conn:
        query = select(exists().where(currency_codes_table.c.name == name))
        res = conn.execute(query).scalar()
    return res


start = datetime.datetime.strptime("2014-06-06", "%Y-%m-%d")
end = datetime.datetime.strptime("2015-07-07", "%Y-%m-%d")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

for date in date_generated:
    print(date.strftime("%Y-%m-%d"))