import pytest
from contexere.data.cache import init_researcher_table
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

def fill_folder(path, *files):
    for fn in files:
        (path / fn).write_text("x", encoding="utf-8")

def test_file_without_dependency_known_researcher(temp_dir, db):
    init_researcher_table(db, user='testuser')
    index_file_artefact(db, temp_dir / 'ERP26pBa_9b__example__value_1.txt',
                        'ERP', '26pB', 'a', '9b__example__value_1.txt', 'testuser')
    tables = {table: db.select_all(table) for table in db.metadata.tables}
    print(tables)
    for table, df in tables.items():
        print(table)
        print(df)
        if table in ['RAG', 'Keyword', 'KeywordIndex']:
            assert len(df) == 2
        elif table in ['MarkupFile', 'Note']:
            assert len(df) == 0
        else:
            assert len(df) == 1
        if table == 'RAG':
            assert df.loc[0, 'ID'] == 'ERP26pBa'
            assert df.loc[1, 'ID'] == 'ERP26p9b'
        elif table not in ['MarkupFile', 'Note']:
            assert df.loc[0, 'ID'] == 1
    assert tables['Researcher'].loc[0, 'Name'] == 'testuser'
    assert tables['Project'].loc[0, 'Name'] == 'ERP'
    assert tables['RAG'].loc[0, 'Project'] == 'ERP'
    assert tables['RAG'].loc[0, 'Date'] == '26pB'
    assert tables['RAG'].loc[0, 'Step'] == 'a'
    assert tables['RAG'].loc[0, 'ResearcherID'] == 1
    assert tables['RAG'].loc[1, 'Project'] == 'ERP'
    assert tables['RAG'].loc[1, 'Date'] == '26p9'
    assert tables['RAG'].loc[1, 'Step'] == 'b'
    assert tables['RAG'].loc[1, 'ResearcherID'] == 1
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



