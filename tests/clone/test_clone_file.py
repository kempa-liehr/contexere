import pytest

from contexere.scheme import abbreviate_date
from contexere.clone import clone_file

@pytest.fixture()
def temp_dir(tmp_path_factory):
    # Create a named base directory for the session
    base = tmp_path_factory.mktemp("session_data")
    return base

def fill_folder(path, *files):
    for fn in files:
        (path / fn).write_text('', encoding='utf-8')

def test_one_old_file_no_reference(temp_dir):
    fill_folder(temp_dir, 'notes.txt', 'ERP25pBa__example.txt')
    rag = 'ERP' + abbreviate_date(local=True) + 'a'
    path_to_clone, message = clone_file(temp_dir / 'ERP25pBa__example.txt', rag)
    assert (temp_dir / (rag + '__example.txt')).exists()

def test_file_without_rag(temp_dir):
    fill_folder(temp_dir, 'notes.txt', 'ERP25pBa__example.txt')
    rag = 'ERP' + abbreviate_date(local=True) + 'a'
    path_to_clone, message = clone_file(temp_dir / 'notes.txt', rag)
    assert (temp_dir / (rag + '.txt')).exists()

def test_file_without_rag_with_notes(temp_dir):
    fill_folder(temp_dir, 'notes_example.txt', 'ERP25pBa__example.txt')
    rag = 'ERP' + abbreviate_date(local=True) + 'a'
    path_to_clone, message = clone_file(temp_dir / 'notes_example.txt', rag)
    assert (temp_dir / (rag + '.txt')).exists()

def test_one_old_file_with_reference(temp_dir):
    fill_folder(temp_dir, 'notes.txt', 'ERP25pBa__example.txt')
    rag = 'ERP' + abbreviate_date(local=True) + 'a'
    path_to_clone, message = clone_file(temp_dir / 'ERP25pBa__example.txt', rag,
                                        references='25pBa', keywords=['testA', 'testB'])
    print(list(temp_dir.glob('*')))
    assert (temp_dir / (rag + '_25pBa__testA__testB.txt')).exists()

def test_one_old_file_having_reference(temp_dir):
    fill_folder(temp_dir, 'notes.txt', 'ERP25pBa_Aa__example.txt')
    rag = 'ERP' + abbreviate_date(local=True) + 'a'
    path_to_clone, message = clone_file(temp_dir / 'ERP25pBa_Aa__example.txt', rag)
    assert (temp_dir / (rag + '__example.txt')).exists()