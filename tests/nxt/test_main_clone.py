import os
import subprocess
from pathlib import Path
import pytest
import sys

import os
from contexere.nxt import main
from contexere.scheme import abbreviate_date


@pytest.fixture()
def temp_dir(tmp_path_factory):
    base = tmp_path_factory.mktemp("session_data")
    return base


def fill_folder(path, *files):
    for fn in files:
        (path / fn).write_text('', encoding='utf-8')

def test_clone(temp_dir):
    fill_folder(temp_dir, 'notes.txt', 'ERP25pBa__example.txt')
    os.chdir(temp_dir)
    rag = 'ERP' + abbreviate_date(local=True) + 'a'

    main(['ERP25pBa__example.txt'])
    print(list(temp_dir.glob('*')))
    assert (temp_dir / (rag + '__example.txt')).exists()

def test_clone_with_reference_having_whitespace(temp_dir):
    fill_folder(temp_dir, 'notes.txt', 'ERP25pBa__example.txt')
    os.chdir(temp_dir)
    rag = 'ERP' + abbreviate_date(local=True) + 'a'

    main(['ERP25pBa__example.txt', '--keywords', 'test A'])
    print(list(temp_dir.glob('*')))
    assert (temp_dir / (rag + '__test_A.txt')).exists()

def test_clone_with_own_reference(temp_dir):
    fill_folder(temp_dir, 'notes.txt', 'ERP25pBa_Aa__example.txt')
    os.chdir(temp_dir)
    rag = 'ERP' + abbreviate_date(local=True) + 'a'

    main(['ERP25pBa_Aa__example.txt'])
    print(list(temp_dir.glob('*')))
    assert (temp_dir / (rag + '__example.txt')).exists()