from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

button_text = KeyboardButton('Текстом')
button_file = KeyboardButton('Excel')
button_to_begin = KeyboardButton('Сначала')

greet_kb = ReplyKeyboardMarkup()
greet_kb.add(button_text)
greet_kb.add(button_file)
greet_kb.add(button_to_begin)

to_start_kb = ReplyKeyboardMarkup()
to_start_kb.add(button_to_begin)
