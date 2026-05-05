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
    assert message == "Cloned from ERP25pBa__example.txt."

def test_one_old_file_with_reference(temp_dir):
    fill_folder(temp_dir, 'notes.txt', 'ERP25pBa__example.txt')
    rag = 'ERP' + abbreviate_date(local=True) + 'a'
    path_to_clone, message = clone_file(temp_dir / 'ERP25pBa__example.txt', rag,
                                        references='25pBa', keywords=['testA', 'testB'])
    print(list(temp_dir.glob('*')))
    assert (temp_dir / (rag + '_25pBa__testA__testB.txt')).exists()
    assert message == "Cloned from ERP25pBa__example.txt."