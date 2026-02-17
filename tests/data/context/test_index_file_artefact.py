import pytest
from contexere.data.context import index_file_artefact
from contexere.data.interfaces.contextdb import ContextDB

@pytest.fixture()
def temp_dir(tmp_path_factory):
    # Create a named base directory for the session
    base = tmp_path_factory.mktemp("session_data")
    return base

@pytest.fixture
def db():
    in_memory_db = ContextDB(path='')
    in_memory_db.create_tables()
    return in_memory_db

def test_file_with_dependency(temp_dir, db):
    index_file_artefact(db, temp_dir / 'ERP26pBa_9b__example__value_1.txt',
                        'ERP', '26pB', 'a', '9b__example__value_1')
    tables = {table: db.select_all(table) for table in db.metadata.tables}
    for table, df in tables.items():
        if table in ['RAG', 'Keyword', 'KeywordIndex']:
            assert len(df) == 2
        else:
            assert len(df) == 1
        if table == 'RAG':
            assert df.loc[0, 'ID'] == 'ERP26pBa'
            assert df.loc[1, 'ID'] == 'ERP26p9b'
    assert tables['Project'].loc[0, 'Name'] == 'ERP'
    assert tables['RAG'].loc[0, 'Project'] == 'ERP'
    assert tables['RAG'].loc[0, 'Date'] == '26pB'
    assert tables['RAG'].loc[0, 'Step'] == 'a'
    assert tables['RAG'].loc[1, 'Project'] == 'ERP'
    assert tables['RAG'].loc[1, 'Date'] == '26p9'
    assert tables['RAG'].loc[1, 'Step'] == 'b'
    assert tables['KnowledgeGraph'].loc[0, 'Parent'] == 'ERP26p9b'
    assert tables['KnowledgeGraph'].loc[0, 'Child'] == 'ERP26pBa'
    assert tables['Path'].loc[0, 'Name'] == str(temp_dir)
    assert tables['Artefact'].loc[0, 'RAG'] == 'ERP26pBa'
    assert tables['Artefact'].loc[0, 'FileName'] == 'ERP26pBa_9b__example__value_1.txt'
    assert tables['Artefact'].loc[0, 'FileExtension'] == '.txt'
    assert tables['Artefact'].loc[0, 'Path'] == 1
    assert not tables['Artefact'].loc[0, 'IsGenerator']
    assert not tables['Artefact'].loc[0, 'IsDirectory']
    assert tables['Keyword'].loc[0, 'Keyword'] == 'example'
    assert tables['Keyword'].loc[1, 'Keyword'] == 'value'
    assert tables['KeywordIndex'].loc[0, 'RAG'] == 'ERP26pBa'
    assert tables['KeywordIndex'].loc[0, 'Keyword'] == 1
    assert tables['KeywordIndex'].loc[1, 'RAG'] == 'ERP26pBa'
    assert tables['KeywordIndex'].loc[1, 'Keyword'] == 2
    assert tables['KeyValueIndex'].loc[0, 'RAG'] == 'ERP26pBa'
    assert tables['KeyValueIndex'].loc[0, 'Keyword'] == 2
    assert tables['KeyValueIndex'].loc[0, 'Value'] == '1'
    assert tables['KeyValueIndex'].loc[0, 'IsNumeric']

def test_folder(temp_dir, db):
    rag_dir = temp_dir / 'ERP26pBa_test'
    rag_dir.mkdir()
    index_file_artefact(db, rag_dir,
                        'ERP', '26pB', 'a', 'test')
    tables = {table: db.select_all(table) for table in db.metadata.tables}
    for table, df in tables.items():
        print(table)
        if table in ['KnowledgeGraph', 'KeyValueIndex']:
            assert len(df) == 0
        else:
            assert len(df) == 1
        if table == 'RAG':
            assert df.loc[0, 'ID'] == 'ERP26pBa'
    assert tables['Project'].loc[0, 'Name'] == 'ERP'
    assert tables['RAG'].loc[0, 'Project'] == 'ERP'
    assert tables['RAG'].loc[0, 'Date'] == '26pB'
    assert tables['RAG'].loc[0, 'Step'] == 'a'
    assert tables['Path'].loc[0, 'Name'] == str(temp_dir)
    assert tables['Artefact'].loc[0, 'RAG'] == 'ERP26pBa'
    assert tables['Artefact'].loc[0, 'FileName'] == 'ERP26pBa_test'
    assert tables['Artefact'].loc[0, 'FileExtension'] == ''
    assert tables['Artefact'].loc[0, 'Path'] == 1
    assert not tables['Artefact'].loc[0, 'IsGenerator']
    assert tables['Artefact'].loc[0, 'IsDirectory']
    assert tables['Keyword'].loc[0, 'Keyword'] == 'test'
    assert tables['KeywordIndex'].loc[0, 'RAG'] == 'ERP26pBa'
    assert tables['KeywordIndex'].loc[0, 'Keyword'] == 1



