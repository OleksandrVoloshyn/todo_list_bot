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
        user = list(cur.execute('select * from users where id == %s' % (user_id)))
        print(user)
        if not user:
            cur.execute("insert into users (id, username) values ('%s','%s')" % (user_id, user_name))


def create_task(user_id, title):
    with open_db() as cur:
        print(type(user_id))
        print(type(title))
        cur.execute("insert into tasks (title,user_id) values ('%s','%s')" % (title, user_id))


def get_users_task(user_id):
    with open_db() as cur:
        cur.execute('select * from tasks where user_id == %s' % (user_id))
        return [f'id:{i[0]} -- task:{i[1]} status:{"Done" if i[2] else "Not Done"}' for i in cur.fetchall()]


def complete_task(task_id, user_id):
    with open_db() as cur:
        task = list(cur.execute('select * from tasks where id == %s' % (task_id)))
        if task and task[-1][-1] == user_id:
            cur.execute('update tasks set status=1 where id == %s' % (task_id))
            return True

        return False


def remove_task(task_id, user_id):
    with open_db() as cur:
        task = list(cur.execute('select * from tasks where id = %s' % (task_id)))
        if task and task[-1][-1] == user_id:
            cur.execute('delete from tasks where id = %s' % (task_id))


def update_avatar(user_id, path):
    with open_db() as cur:
        cur.execute('update users set avatar="%s" where id = %s' % (path, user_id))


def get_avatar(user_id):
    with open_db() as cur:
        cur.execute('select avatar from users where id = %s' % (user_id))
        return cur.fetchall().pop()
