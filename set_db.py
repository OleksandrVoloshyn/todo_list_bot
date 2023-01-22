from services import open_db


def create_tables():
    with open_db() as cur:
        query_users = """
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            avatar TEXT 
            )"""

        cur.execute(query_users)
        query_tasks = """
            CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            status INTEGER DEFAULT 0,
            user_id INTEGER
            CONSTRAINT user_id
            REFERENCES users
            ON DELETE CASCADE
            )"""
        cur.execute(query_tasks)
