from services import open_db


def create_tables():
    with open_db() as cur:
        query_users = """
                create table if not exists users
                (
                    id integer primary key,
                    username TEXT    not null,
                    avatar  TEXT
                )
        """

        cur.execute(query_users)
        query_tasks = """
                    create table if not exists tasks
                (
                    id integer primary key,
                    title   text not null,
                    status  integer default 0,
                    user_id integer
                        constraint user_id
                            references users
                            on delete cascade
                )
        """
        cur.execute(query_tasks)
