from contextlib import contextmanager

import sqlite3
from aiogram import types


@contextmanager
def open_db():
    con = sqlite3.connect('test.db')
    try:
        cur = con.cursor()
        yield cur
    finally:
        con.commit()
        con.close()


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Start this beautiful bot'),
        types.BotCommand('my_tasks', 'get all tasks'),
        types.BotCommand('create_task', 'Create new task'),
        types.BotCommand('complete_task', 'Complete task'),
        types.BotCommand('remove_task', 'Remove task'),
        types.BotCommand('add_avatar', 'Add avatar to my profile'),
        types.BotCommand('avatar', 'Check my face'),
    ])


def register_user(user_id, user_name):
    with open_db() as cur:
        user = list(cur.execute('SELECT * FROM users WHERE id == (?,)', (user_id,)))
        if not user:
            cur.execute("INSERT INTO users (id, username) VALUES (?, ?)", (user_id, user_name))


def create_task(user_id, title):
    with open_db() as cur:
        cur.execute("INSERT INTO tasks (title, user_id) VALUES (?, ?)", (title, user_id))


def get_users_task(user_id):
    with open_db() as cur:
        cur.execute('SELECT * FROM tasks WHERE user_id == (?,)', (user_id,))
        return [f'id:{i[0]} -- task:{i[1]} status:{"Done" if i[2] else "Not Done"}' for i in cur.fetchall()]


def complete_task(task_id, user_id):
    with open_db() as cur:
        task = list(cur.execute('SELECT * FROM tasks WHERE id == (?,)', (task_id,)))
        if task and task[-1][-1] == user_id:  # task[-1][-1] -> owner_id
            cur.execute('UPDATE tasks SET status=1 WHERE id == (?,)', (task_id,))
            return True


def remove_task(task_id, user_id):
    with open_db() as cur:
        task = list(cur.execute('SELECT * FROM tasks WHERE id = (?,)', (task_id,)))
        if task and task[-1][-1] == user_id:  # task[-1][-1] -> owner_id
            cur.execute('DELETE FROM tasks WHERE id = (?, )', (task_id,))


def update_avatar(user_id, path):
    with open_db() as cur:
        cur.execute(f'UPDATE users SET avatar="{path}" WHERE id = {user_id}')


def get_avatar(user_id):
    with open_db() as cur:
        cur.execute('SELECT avatar FROM users WHERE id = (?,)', (user_id,))
        return cur.fetchall().pop()
