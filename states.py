from aiogram.dispatcher.filters.state import StatesGroup, State


class NextStateHandler(StatesGroup):
    task_title = State()
    task_complete_id = State()
    photo = State()
    task_remove_id = State()
