import pytest
from contexere.data.cache import fill_cache
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

def test_unrelated_and_related_file(db, temp_dir):
    fill_folder(temp_dir, 'notes.txt', 'ERP26pBa_9b__example__value_1.txt')
    with open(temp_dir / 'logbook.org', 'w') as f:
        f.write('Title\n* ERP26p9b -- Extracted note\n')

    fill_cache(db, root=temp_dir)
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

def count(col):
    values = col.tolist()
    return {v: values.count(v) for v in set(values)}

def test_three_related_files(db, temp_dir):
    fill_folder(temp_dir, 'ERP26pAa_example.txt', 'ERP26pBa_example.txt', 'ERP26pAa_data.csv')

    fill_cache(db, root=temp_dir)
    tables = {table: db.select_all(table) for table in db.metadata.tables}
    for table, df in tables.items():
        if table in ['RAG', 'Keyword']:
            assert len(df) == 2
        elif table in ['KnowledgeGraph', 'KeyValueIndex']:
            assert len(df) == 0
        elif table in ['Artefact', 'KeywordIndex']:
            assert len(df) == 3
        else:
            assert len(df) == 1
        if table == 'RAG':
            assert set(df['ID'].values) == {'ERP26pAa', 'ERP26pBa'}
    assert tables['Project'].loc[0, 'Name'] == 'ERP'
    assert tables['RAG']['Project'].unique() == ['ERP']
    assert set(tables['RAG']['Date'].values) == {'26pA', '26pB'}
    assert tables['RAG']['Step'].unique() == ['a']
    assert tables['Path'].loc[0, 'Name'] == str(temp_dir)
    assert count(tables['Artefact']['RAG']) == {'ERP26pAa': 2, 'ERP26pBa': 1}
    assert set(tables['Artefact']['FileName'].values) == {'ERP26pAa_example.txt',
                                                          'ERP26pBa_example.txt', 'ERP26pAa_data.csv'}
    assert count(tables['Artefact']['FileExtension']) == {'.txt': 2, '.csv': 1}
    assert tables['Artefact']['Path'].unique() == [1]
    assert tables['Artefact']['IsGenerator'].sum() == 0
    assert tables['Artefact']['IsDirectory'].sum() == 0
    assert set(tables['Keyword']['Keyword'].values) == {'example', 'data'}
    assert count(tables['KeywordIndex']['RAG']) == {'ERP26pAa': 2, 'ERP26pBa': 1}

def test_three_related_files_different_projects(db, temp_dir):
    fill_folder(temp_dir, 'ERP26pAa_example.txt', 'ERQ26pBa_example.txt', 'ERP26pAa_data.csv')

    fill_cache(db, root=temp_dir)
    tables = {table: db.select_all(table) for table in db.metadata.tables}
    for table, df in tables.items():
        if table in ['RAG', 'Keyword', 'Project']:
            assert len(df) == 2
        elif table in ['KnowledgeGraph', 'KeyValueIndex']:
            assert len(df) == 0
        elif table in ['Artefact', 'KeywordIndex']:
            assert len(df) == 3
        else:
            assert len(df) == 1
        if table == 'RAG':
            assert set(df['ID'].values) == {'ERP26pAa', 'ERQ26pBa'}
    assert count(tables['Project']['Name']) == {'ERP': 1, 'ERQ': 1}
    assert count(tables['RAG']['Project']) == {'ERP': 1, 'ERQ': 1}
    assert set(tables['RAG']['Date'].values) == {'26pA', '26pB'}
    assert tables['RAG']['Step'].unique() == ['a']
    assert tables['Path'].loc[0, 'Name'] == str(temp_dir)
    assert count(tables['Artefact']['RAG']) == {'ERP26pAa': 2, 'ERQ26pBa': 1}
    assert set(tables['Artefact']['FileName'].values) == {'ERP26pAa_example.txt',
                                                          'ERQ26pBa_example.txt', 'ERP26pAa_data.csv'}
    assert count(tables['Artefact']['FileExtension']) == {'.txt': 2, '.csv': 1}
    assert tables['Artefact']['Path'].unique() == [1]
    assert tables['Artefact']['IsGenerator'].sum() == 0
    assert tables['Artefact']['IsDirectory'].sum() == 0
    assert set(tables['Keyword']['Keyword'].values) == {'example', 'data'}
    assert count(tables['KeywordIndex']['RAG']) == {'ERP26pAa': 2, 'ERQ26pBa': 1}

def test_three_files_different_projects_and_folders(db, temp_dir):
    fill_folder(temp_dir, 'ERP26pAa_example.txt', 'ERQ26pBa_example.txt')
    sub_dir = temp_dir / 'sub_dir'
    sub_dir.mkdir()
    fill_folder(sub_dir, 'ERP26pAa_data.csv')
    fill_cache(db, root=temp_dir)
    tables = {table: db.select_all(table) for table in db.metadata.tables}
    for table, df in tables.items():
        if table in ['RAG', 'Keyword', 'Project', 'Path']:
            assert len(df) == 2
        elif table in ['KnowledgeGraph', 'KeyValueIndex']:
            assert len(df) == 0
        elif table in ['Artefact', 'KeywordIndex']:
            assert len(df) == 3
        else:
            assert len(df) == 1
        if table == 'RAG':
            assert set(df['ID'].values) == {'ERP26pAa', 'ERQ26pBa'}
    assert count(tables['Project']['Name']) == {'ERP': 1, 'ERQ': 1}
    assert count(tables['RAG']['Project']) == {'ERP': 1, 'ERQ': 1}
    assert set(tables['RAG']['Date'].values) == {'26pA', '26pB'}
    assert tables['RAG']['Step'].unique() == ['a']
    assert set(tables['Path']['Name'].values) == {str(temp_dir), str(temp_dir / 'sub_dir')}
    assert count(tables['Artefact']['RAG']) == {'ERP26pAa': 2, 'ERQ26pBa': 1}
    assert set(tables['Artefact']['FileName'].values) == {'ERP26pAa_example.txt',
                                                          'ERQ26pBa_example.txt', 'ERP26pAa_data.csv'}
    assert count(tables['Artefact']['FileExtension']) == {'.txt': 2, '.csv': 1}
    assert len(set(tables['Artefact']['Path'].values)) == 2
    assert tables['Artefact']['IsGenerator'].sum() == 0
    assert tables['Artefact']['IsDirectory'].sum() == 0
    assert set(tables['Keyword']['Keyword'].values) == {'example', 'data'}
    assert count(tables['KeywordIndex']['RAG']) == {'ERP26pAa': 2, 'ERQ26pBa': 1}