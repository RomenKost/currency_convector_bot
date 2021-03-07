from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from rates import get_rates
from os import remove

from convertor import convert
from history import make_graph


TOKEN = ''


bot = Bot(TOKEN)
db = Dispatcher(bot)


@db.message_handler(commands=['start', 'help'])
async def info(message: Message):
    await bot.send_message(message.chat.id, """This bot is designed to track major currencies. It сan do:

- Show all available currencies and their rate against the dolar (/list or /lst) ;
- Convert CUR1 to CUR2 (/exchange PRICE CUR1 to CUR2)
- The history of CUR1-CUR2 relations in the last X days (/history CUR1/CUR2 for X days)""")


@db.message_handler(commands=['list', 'lst'])
async def rates_list(message: Message):
    rates, text = get_rates(), ''
    for rate in rates:
        text += f'{rate}: {rates[rate]:.2f}\n'
    await bot.send_message(message.chat.id, text)


@db.message_handler(commands=['exchange'])
async def convertor(message: Message):
    text = convert(message.text, get_rates())
    if text is not None:
        await bot.send_message(message.chat.id, text)


@db.message_handler(commands=['history'])
async def history(message: Message):
    if make_graph(message.text, message.chat.id):
        await bot.send_photo(message.chat.id, open(f'resources/graphs/{message.chat.id}.jpg', 'rb'))
        remove(f'resources/graphs/{message.chat.id}.jpg')


if __name__ == '__main__':
    try:
        executor.start_polling(dispatcher=db)
    except Exception as e:
        input(e)
