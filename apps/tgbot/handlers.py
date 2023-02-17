from pathlib import Path

import requests
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from bot_states import BotState
from bot_kb import greet_kb, to_start_kb
from bot_cfg import bot

BASE_DIR = Path(__file__).resolve().parent.parent

# DOMAIN_URL = 'https://regalii-app.herokuapp.com/'
DOMAIN_URL = 'http://134-0-113-174.cloudvps.regruhosting.ru:8000/'


async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text="Привет, я буду делать регалии, каким образом вы хотите отправить мне данные?",
                           reply_markup=greet_kb)
    await BotState.howto.set()


async def get_howto(message: types.Message, state: FSMContext):
    await state.update_data(howto=message.text)

    data = await state.get_data()
    if data['howto'] == 'Текстом':
        await bot.send_message(chat_id=message.chat.id,
                               text='Введите регалию',
                               reply_markup=to_start_kb)
        await BotState.regalia.set()
    elif data['howto'] == 'Excel':
        await bot.send_message(chat_id=message.chat.id,
                               text='Пришлите файл с регалиями',
                               reply_markup=to_start_kb)
        await BotState.file.set()
    elif data['howto'] == 'Сначала':
        await start_command(message)

    else:
        await wrong_input_howto(message)


async def wrong_input_howto(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text="Некорректный ввод\nКаким образом вы будете отправлять мне данные?",
                           reply_markup=greet_kb)
    await BotState.howto.set()


async def get_file(message: types.Message, state: FSMContext):
    if message.text == 'Сначала':
        await start_command(message)
    else:
        destination = BASE_DIR / 'file.xlsx'
        await message.document.download(destination_file=destination)
        files = {'file': open(destination, 'rb')}
        res = requests.post(url=f'{DOMAIN_URL}regals/', files=files)
        await bot.send_message(chat_id=message.chat.id, text=f"Ваши регалии готовы, скачивайте: {res.json()['url']}\n\nначинаем сначала!")
        await start_command(message)


async def get_regalia(message: types.Message, state: FSMContext):
    if message.text == 'Сначала':
        await start_command(message)
    await state.update_data(regalia=message.text)
    data = await state.get_data()
    regalia = data['regalia'].split('\n')
    rank = regalia[0].strip()
    fio = regalia[1].strip()
    city = regalia[2].strip()
    full = f"{rank} {fio} ({city})"
    data_json = {'regalia': full,
                 'city': city,
                 'fio': fio}
    res = requests.post(url=f'{DOMAIN_URL}regals/', data=data_json)
    await bot.send_message(chat_id=message.chat.id, text=f"Ваши регалии готовы, скачивайте: {res.json()['url']}\n\nначинаем сначала!")
    await start_command(message)


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])
    dp.register_message_handler(get_howto, state=BotState.howto, content_types=['text'])
    dp.register_message_handler(get_file, state=BotState.file, content_types=[types.ContentType.DOCUMENT, 'text'])
    dp.register_message_handler(get_regalia, state=BotState.regalia, content_types=['text'])
