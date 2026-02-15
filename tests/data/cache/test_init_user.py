import pytest
from contexere.data.interfaces.contextdb import ContextDB

@pytest.fixture
def db():
    in_memory_db = ContextDB(path='')
    in_memory_db.create_tables()
    return in_memory_db


def test_basic_in_memory_functionality(db):
    pass