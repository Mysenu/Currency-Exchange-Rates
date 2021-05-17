import datetime
import json

import requests

from .configs import CURRENCY_API_TOKEN
from ..db import dateExists, insertValueCurrency, insertCurrencyCode


def getValueCurrenciesOnDate(date: datetime):
    query = f'https://openexchangerates.org/api/historical/{date}.json?app_id={CURRENCY_API_TOKEN}'
    res = requests.get(query)
    value_currency = json.loads(res.text)['rates']
    return value_currency


def getCurrencyCodes():
    res = requests.get('https://openexchangerates.org/api/currencies.json')
    currency_codes = json.loads(res.text)
    return currency_codes


def insertCurrencyCodesInDB():
    currency_codes = getCurrencyCodes()

    for code, name in currency_codes.items():
        insertCurrencyCode(code, name)


def insertValueCurrencyInDB(start_date: str, end_date: str):
    start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]

    for date in date_generated:
        date = date.date()

        if dateExists(date):
            continue

        value_currencies = getValueCurrenciesOnDate(date)
        for code, value in value_currencies.items():
            insertValueCurrency(code, value, date)
