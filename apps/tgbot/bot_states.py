from aiogram.dispatcher.filters.state import State, StatesGroup


class BotState(StatesGroup):
    howto = State()
    file = State()
    regalia = State()
