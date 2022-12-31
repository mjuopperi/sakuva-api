import os
from contextlib import contextmanager

import psycopg
from psycopg.conninfo import make_conninfo
from psycopg.rows import dict_row, RowFactory

from app.config import get_settings

settings = get_settings()


@contextmanager
def connect(autocommit: bool) -> psycopg.Connection:
    conninfo = make_conninfo(
        "",
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_username,
        password=settings.db_password,
    )
    with psycopg.connect(conninfo, autocommit=autocommit) as conn:
        yield conn


@contextmanager
def cursor(autocommit: bool = True, row_factory: RowFactory = dict_row) -> psycopg.Cursor:
    with connect(autocommit) as conn:
        with conn.cursor(row_factory=row_factory) as cur:
            yield cur


def create_tables(drop_before_create=False):
    with cursor() as cur:
        table_dir = os.path.join(os.path.dirname(__file__), "tables")
        for filename in os.listdir(table_dir):
            if filename.endswith(".sql"):
                path = os.path.join(table_dir, filename)
                with open(path, "r") as file:
                    content = file.read()
                    create, *rest = content.split(";")
                    if drop_before_create:
                        table_name = filename.replace(".sql", "")
                        cur.execute(f"drop table {table_name}")
                    cur.execute(create)
                    for more in [x.rstrip() for x in rest]:
                        if more:
                            cur.execute(more)
