import pytest

from contexere.scheme import abbreviate_date, suggest_next

@pytest.fixture()
def temp_dir(tmp_path_factory):
    # Create a named base directory for the session
    base = tmp_path_factory.mktemp("session_data")
    return base

def fill_folder(path, *files):
    for fn in files:
        (path / fn).write_text("x", encoding="utf-8")

def test_one_old_file(temp_dir):
    fill_folder(temp_dir, 'notes.txt', 'ERP26pBa_example.txt')
    next_rag = suggest_next(temp_dir, project='ERP')
    assert next_rag == 'ERP' + abbreviate_date(local=True) +'a'

def test_one_recent_file(temp_dir):
    rag = abbreviate_date(local=True)
    fill_folder(temp_dir, 'notes.txt', 'ERP' + rag + 'a_example.txt')
    next_rag = suggest_next(temp_dir, project='ERP')
    assert next_rag == 'ERP' + abbreviate_date(local=True) +'b'

def test_no_previous_RAGs(temp_dir):
    fill_folder(temp_dir, 'notes.txt')
    next_rag = suggest_next(temp_dir, project='ERP')
    assert next_rag == 'ERP' + abbreviate_date(local=True) +'a'

def test_missing_project_error(temp_dir):
    fill_folder(temp_dir, 'notes.txt')
    with pytest.raises(ValueError):
        suggest_next(temp_dir)

def test_several_old_RAGs_and_no_project(temp_dir):
    rag = abbreviate_date(local=True)
    fill_folder(temp_dir, 'notes.txt', 'ERP26pBa_example.txt', 'ERP' + rag + 'a_example.txt',
                'ERQ26pBa_example.txt')
    next_rag = suggest_next(temp_dir)
    assert next_rag == 'ERP' + abbreviate_date(local=True) +'b'