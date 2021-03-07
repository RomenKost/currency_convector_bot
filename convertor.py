"""
This module contains a convert function for converting one currency into another and supporting functions.
"""


def convert(message: str, rates: dict):
    data = message.split()
    try:
        __check_data(data)
        money, cur1_name, cur2_name = __parse_command(data)
        cur1, cur2 = rates[cur1_name], rates[cur2_name]

        return __view(money, cur1, cur2, cur2_name)
    except Exception as e:
        print(e)


def __parse_command(data: list):
    if '$' in data[1]:
        currency1 = 'USD'
        data[1].replace('$', '')
    else:
        currency1 = data[2]

    currency2 = data[-1]
    money = float(data[1])
    return money, currency1, currency2


def __view(money: float, cur1: float, cur2: float, cur2_name: str) -> str:
    res = f'{(money / cur1) * cur2 :.2f}'
    if cur2_name == 'USD':
        res = f'${res}'
    else:
        res = f'{res} {cur2_name}'
    return res


def __check_data(data: list):
    if not (4 <= len(data) <= 5 and data[-2] == 'to'):
        raise Exception('Incorrect data')
