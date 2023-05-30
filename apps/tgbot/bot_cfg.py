import os

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

storage = MemoryStorage()
DOMAIN_URL = 'http://127.0.0.1:8000/'

API_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
