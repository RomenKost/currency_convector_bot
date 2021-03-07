import json
import sqlite3
from datetime import datetime
import requests

"""
This module contains the get_rates function To obtain the current exchange rate and supporting functions.
"""


def __sql(query: str):
    try:
        database = sqlite3.connect('resources/database.sqlite')
        cursor = database.cursor()

        cursor.execute(query)
        result = cursor.fetchall()
        database.commit()

        database.close()
    except Exception as e:
        print(e)
        result = False
    return result


def __get_datetime():
    return __sql('SELECT * FROM datetimes')


def __update_datetime():
    __sql(f'DELETE FROM datetimes')
    __sql(f'INSERT INTO datetimes VALUES("{datetime.now().strftime("%Y.%m.%d %H:%M:%S")}")')


def __save_row(currency: str, price: float):
    __sql(f'INSERT INTO rates '
          f'VALUES("{currency}", {price})')


def __update_rates(rates: dict):
    __sql('DELETE FROM rates')
    __update_datetime()

    for rate in rates:
        __save_row(rate, rates[rate])


def __load_rates():
    rates = {}
    for rate in __sql('SELECT * FROM rates'):
        rates.update([(rate[0], float(rate[1]))])
    return rates


def get_rates():
    dt = datetime.strptime(__get_datetime()[0][0], '%Y.%m.%d %H:%M:%S')

    if (datetime.now() - dt).seconds > 600:
        content = requests.get('https://api.exchangeratesapi.io/latest?base=USD').text
        rates = json.loads(content)['rates']
        __update_rates(rates)
    else:
        rates = __load_rates()
    return rates
