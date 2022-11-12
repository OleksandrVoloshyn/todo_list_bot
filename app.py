from aiogram import executor

from handlers import dp
from services import set_default_commands
from set_db import create_tables


async def on_startup(dispatch):
    create_tables()
    await set_default_commands(dispatch)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
