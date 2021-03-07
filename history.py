import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
from datetime import datetime, timedelta


"""
This module contains a make_graph function that creates and saves a graph based on data received from a user request. 
"""


def __draw_image(data: pd.DataFrame, message: str, cur1_name: str, cur2_name: str, user: int):
    plt.title(message.replace('/history ', ''))
    plt.xlabel('Date')
    plt.ylabel(f'Ratio {cur1_name}/{cur2_name}')

    plt.plot(data['date'], data['price'], color='Green')

    plt.savefig(f'resources/graphs/{user}.jpg')
    plt.close()


def make_graph(message: str, user: int):
    data = message.split()
    try:
        __check_data(data)
        count_days, cur1_name, cur2_name = __parse_command(data)
        data = __load_data(count_days, cur1_name, cur2_name)
        __draw_image(data, message, cur1_name, cur2_name, user)
        return True
    except Exception as e:
        print(e)


def __parse_command(data: list):
    count_days = int(data[-2])
    curs = data[1].split('/')
    return count_days, curs[0], curs[1]


def __check_data(data: list):
    if not (len(data) == 5 and data[-1] == 'days' and data[-3] == 'for'):
        raise Exception('Incorrect data')


def __load_data(count_days: int, cur1: str, cur2: str) -> pd.DataFrame:
    final_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=count_days)).strftime('%Y-%m-%d')

    link = \
        f'https://api.exchangeratesapi.io/history?start_at={start_date}&end_at={final_date}&base={cur1}&symbols={cur2}'

    content = requests.get(link).text
    rates = json.loads(content)['rates']

    df = pd.DataFrame({'date': [date for date in rates], 'price': [rates[date][cur2] for date in rates]})
    return df.sort_values(by='date')
