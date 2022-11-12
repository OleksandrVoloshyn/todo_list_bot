from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states import NextStateHandler
from services import register_user, create_task, get_users_task, complete_task, update_avatar, get_avatar, remove_task


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    user_name = message.from_user.first_name
    msg = f'Hello {user_name}, I\'m a test bot'
    register_user(message.from_id, user_name)
    await message.answer(msg)


@dp.message_handler(commands=['my_tasks'])
async def command_my_task(message: types.Message):
    tasks = get_users_task(message.from_id)
    for task in tasks:
        await message.answer(task)


@dp.message_handler(commands=['create_task'])
async def command_create_task(message: types.Message):
    await message.answer('Title of your task ?')
    await NextStateHandler.task_title.set()


@dp.message_handler(state=NextStateHandler.task_title)
async def get_task(message: types.Message, state: FSMContext):
    answer = message.text
    create_task(message.from_id, message.text)
    await message.answer(f'title of your task -- {answer}')
    await state.finish()


@dp.message_handler(commands=['complete_task'])
async def command_complete_task(message: types.Message):
    await message.answer('task id?')
    await NextStateHandler.task_complete_id.set()


@dp.message_handler(state=NextStateHandler.task_complete_id)
async def get_task(message: types.Message, state: FSMContext):
    answer = message.text
    result = complete_task(answer, message.from_id)
    if result:
        await message.answer(f'this task has been done')
    else:
        await message.answer(f'Error')

    await state.finish()


@dp.message_handler(commands=['remove_task'])
async def command_remove_task(message: types.Message):
    await message.answer('Title of your task ?')
    await NextStateHandler.task_remove_id.set()


@dp.message_handler(state=NextStateHandler.task_remove_id)
async def delete_task(message: types.Message, state: FSMContext):
    remove_task(message.text, message.from_id)
    await message.answer(f'your task has been removed')
    await state.finish()


@dp.message_handler(commands=['add_avatar'])
async def command_add_avatar(message: types.Message):
    await message.answer('send avatar?')
    await NextStateHandler.photo.set()


@dp.message_handler(state=NextStateHandler.photo, content_types=types.ContentType.PHOTO)
async def set_avatar(message: types.Message, state: FSMContext):
    img = message.photo.pop()
    if img:
        media_path = f'media/{img.file_unique_id}.jpg'
        await message.photo[-1].download(media_path)
        update_avatar(message.from_id, media_path)
        await message.reply('we get your new avatar')
    else:
        await message.reply('Error')
    await state.finish()


@dp.message_handler(commands=['avatar'])
async def command_avatar(message: types.Message):
    path = get_avatar(message.from_id)
    if path:
        photo_bytes = types.InputFile(path_or_bytesio=path[0])
        await message.answer_photo(photo_bytes, caption='krasunchyk')
    else:
        await message.answer('Error')


@dp.message_handler()
async def command_error(message: types.Message):
    await message.answer(f'command {message.text} not found')
