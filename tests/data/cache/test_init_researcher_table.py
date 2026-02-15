import pytest
from contexere.data.cache import init_researcher_table
from contexere.data.interfaces.contextdb import ContextDB


@pytest.fixture
def db():
    in_memory_db = ContextDB(path='')
    in_memory_db.create_tables()
    return in_memory_db


def test_basic_in_memory_functionality(db):
    init_researcher_table(db, user='testuser')
    user = db.get_researchers().loc[0]
    assert user.ID == 1 and user.Name == 'testuser' and user.Email is None