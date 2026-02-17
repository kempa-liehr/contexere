import os
import pytest

from contexere.data.interfaces.contextdb import ContextDB

@pytest.fixture()
def temp_dir(tmp_path_factory):
    # Create a named base directory for the session
    base = tmp_path_factory.mktemp("session_data")
    return base

def test_create_in_memory():
    db = ContextDB(path='')
    assert isinstance(db, ContextDB)

def test_create_in_memory():
    db = ContextDB(path=':memory:')
    assert isinstance(db, ContextDB)

def test_create_with_absolute_path(temp_dir):
    db = ContextDB(path=temp_dir/'test.db')
    assert isinstance(db, ContextDB)

def test_create_with_absolute_path(temp_dir):
    db = ContextDB(path=temp_dir/'test.db')
    assert isinstance(db, ContextDB)

def test_create_with_relative_path(temp_dir):
    sub_dir = temp_dir / 'subdir'
    sub_dir.mkdir()
    os.chdir(temp_dir)
    db = ContextDB(path="test.db")
    assert isinstance(db, ContextDB)
    db = ContextDB(path="./subdir/test.db")
    assert isinstance(db, ContextDB)
