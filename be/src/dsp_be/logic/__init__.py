from typing import List, Type

from peewee import DatabaseProxy, SqliteDatabase, Model

db_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = db_proxy


def test_database(tables: List[Type[Model]]):
    db = SqliteDatabase(':memory:')
    db_proxy.initialize(db)
    db_proxy.connect()
    db_proxy.create_tables(tables)
