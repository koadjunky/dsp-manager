from contextvars import ContextVar
from typing import List, Type

from fastapi import Depends
from peewee import DatabaseProxy, SqliteDatabase, Model, _ConnectionState

db_proxy = DatabaseProxy()

# After https://fastapi.tiangolo.com/advanced/sql-databases-peewee/
db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(_ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


class DspModel(Model):
    class Meta:
        database = db_proxy


def test_database(tables: List[Type[Model]]):
    db = SqliteDatabase('test.db', check_same_thread=False)
    db._state = PeeweeConnectionState()
    db_proxy.initialize(db)
    db_proxy.connect()
    db_proxy.create_tables(tables)


def production_database(tables: List[Type[Model]]):
    db = SqliteDatabase('production.db', check_same_thread=False)
    db._state = PeeweeConnectionState()
    db_proxy.initialize(db)
    db_proxy.connect()
    db_proxy.create_tables(tables)


def close_database():
    db_proxy.close()


async def reset_db_state():
    db_proxy.obj._state._state.set(db_state_default.copy())
    db_proxy.obj._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        db_proxy.connect()
        yield
    finally:
        if not db_proxy.is_closed():
            db_proxy.close()
