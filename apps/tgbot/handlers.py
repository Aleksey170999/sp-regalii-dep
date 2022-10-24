from pathlib import Path

import requests
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from bot_states import BotState
from bot_kb import greet_kb
from bot_cfg import bot

BASE_DIR = Path(__file__).resolve().parent.parent


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
                               reply_markup=types.ReplyKeyboardRemove())
        await BotState.regalia.set()
    elif data['howto'] == 'Файлом':
        await bot.send_message(chat_id=message.chat.id,
                               text='Пришлите файл с регалиями',
                               reply_markup=types.ReplyKeyboardRemove())
        await BotState.file.set()

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

    destination = BASE_DIR / 'file.xlsx'
    await message.document.download(destination_file=destination)
    files = {'file': open(destination, 'rb')}
    res = requests.post(url='http://127.0.0.1:8000/regals/', files=files)
    await bot.send_message(chat_id=message.chat.id, text=res.json()['url'])


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
    res = requests.post(url='http://127.0.0.1:8000/regals/', data=data_json)
    await bot.send_message(chat_id=message.chat.id, text=res.json()['url'])
    await start_command(message)


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])
    dp.register_message_handler(get_howto, state=BotState.howto, content_types=['text'])
    dp.register_message_handler(get_file, state=BotState.file, content_types=types.ContentType.DOCUMENT)
    dp.register_message_handler(get_regalia, state=BotState.regalia, content_types=['text'])
