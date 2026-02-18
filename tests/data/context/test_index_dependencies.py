import pytest
from contexere.data.context import index_dependencies
from contexere.data.interfaces.contextdb import ContextDB

@pytest.fixture
def db():
    in_memory_db = ContextDB(path='')
    in_memory_db.create_tables()
    return in_memory_db

def test_file_with_embedded_partial_rag(db):
    in_memory_db = ContextDB(path='')
    filename = 'ERP26Ia_example_no_value'
    rag_id = db.upsert('RAG', dict(ID='ERP26Ia',
                                   Project='ERP', Date='26I', Step='a'))
    keywords = index_dependencies(in_memory_db, rag_id, 'example_no_value')
    tables = {table: db.select_all(table) for table in db.metadata.tables}
    assert len(tables['KnowledgeGraph']) == 0
    for actual, expected in zip(keywords, ['example', 'no', 'value']):
        assert actual == expected

def test_file_with_trailing_datestep_and_embedded_partial_rag(db):
    rag_id = db.upsert('RAG', dict(ID='ERP26pIb',
                                   Project='ERP', Date='26pI', Step='b'))
    keywords = index_dependencies(db, rag_id, 'Ha_example_no_value')
    tables = {table: db.select_all(table) for table in db.metadata.tables}
    assert len(tables['KnowledgeGraph']) == 1
    assert tables['KnowledgeGraph'].loc[0, 'Parent'] == 'ERP26pHa'
    assert tables['KnowledgeGraph'].loc[0, 'Child'] == 'ERP26pIb'
    for actual, expected in zip(keywords, ['example', 'no', 'value']):
        assert actual == expected

def test_file_with_trailing_step_and_embedded_partial_rag(db):
    rag_id = db.upsert('RAG', dict(ID='ERP26pIb',
                                   Project='ERP', Date='26pI', Step='b'))
    keywords = index_dependencies(db, rag_id, 'a_example_no_value')
    tables = {table: db.select_all(table) for table in db.metadata.tables}
    assert len(tables['KnowledgeGraph']) == 1
    assert tables['KnowledgeGraph'].loc[0, 'Parent'] == 'ERP26pIa'
    assert tables['KnowledgeGraph'].loc[0, 'Child'] == 'ERP26pIb'
    for actual, expected in zip(keywords, ['example', 'no', 'value']):
        assert actual == expected

