import logging

from aiogram import executor

from bot_cfg import dp
from handlers import register_handlers_common

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    register_handlers_common(dp)
    executor.start_polling(dp, skip_updates=True)
