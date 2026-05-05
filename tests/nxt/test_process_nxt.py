import os
import pytest

from contexere.nxt import parse_args, process_nxt
from contexere.scheme import abbreviate_date

@pytest.fixture()
def temp_dir(tmp_path_factory):
    # Create a named base directory for the session
    base = tmp_path_factory.mktemp("session_data")
    return base

def fill_folder(path, *files):
    for fn in files:
        (path / fn).write_text("x", encoding="utf-8")

def test_no_context(temp_dir):
    args = parse_args([])
    os.chdir(temp_dir)
    output = process_nxt(args)
    assert output == abbreviate_date(local=True) + 'a'

    args = parse_args(['--group', 'test'])
    os.chdir(temp_dir)
    output = process_nxt(args)
    assert output == 'test' + abbreviate_date(local=True) + 'a'

def test_one_old_file(temp_dir):
    fill_folder(temp_dir, 'notes.txt', 'ERP26pBa_example.txt')
    args = parse_args([])
    os.chdir(temp_dir)
    output = process_nxt(args)
    assert output == 'ERP' + abbreviate_date(local=True) +'a'

def test_recent_file(temp_dir):
    fill_folder(temp_dir, 'notes.txt', 'ERP' + abbreviate_date(local=True) + 'a_example.txt')
    args = parse_args([])
    os.chdir(temp_dir)
    output = process_nxt(args)
    assert output == 'ERP' + abbreviate_date(local=True) +'b'

def test_clone_file_one_underscore(temp_dir):
    fn = 'ERP' + abbreviate_date(local=True) + 'a_example.txt'
    fill_folder(temp_dir, 'notes.txt', fn)
    args = parse_args([fn])
    os.chdir(temp_dir)
    output = process_nxt(args)
    expected_output = temp_dir / ('ERP' + abbreviate_date(local=True) + 'b__example.txt')
    assert output == expected_output
    assert expected_output.exists()

def test_clone_file_two_underscores(temp_dir):
    fn = 'ERP' + abbreviate_date(local=True) + 'a__example.txt'
    fill_folder(temp_dir, 'notes.txt', fn)
    args = parse_args([fn])
    os.chdir(temp_dir)
    output = process_nxt(args)
    expected_output = temp_dir / ('ERP' + abbreviate_date(local=True) + 'b__example.txt')
    assert output == expected_output
    assert expected_output.exists()

def test_clone_file_one_keyword(temp_dir):
    fn = 'ERP' + abbreviate_date(local=True) + 'a__example.txt'
    fill_folder(temp_dir, 'notes.txt', fn)
    args = parse_args([fn, '--keywords', 'TestA'])
    os.chdir(temp_dir)
    output = process_nxt(args)
    expected_output = temp_dir / ('ERP' + abbreviate_date(local=True) + 'b__TestA.txt')
    assert output == expected_output
    assert expected_output.exists()

def test_clone_file_two_keywords(temp_dir):
    fn = 'ERP' + abbreviate_date(local=True) + 'a__example.txt'
    fill_folder(temp_dir, 'notes.txt', fn)
    args = parse_args([fn, '--keywords', 'TestA', '2nd'])
    os.chdir(temp_dir)
    output = process_nxt(args)
    expected_output = temp_dir / ('ERP' + abbreviate_date(local=True) + 'b__TestA__2nd.txt')
    assert output == expected_output
    assert expected_output.exists()

def test_clone_file_two_keywords(temp_dir):
    fn = 'ERP' + abbreviate_date(local=True) + 'a__example.txt'
    fill_folder(temp_dir, 'notes.txt', fn)
    args = parse_args([fn, '--keywords', 'TestA 2nd'])
    os.chdir(temp_dir)
    output = process_nxt(args)
    expected_output = temp_dir / ('ERP' + abbreviate_date(local=True) + 'b__TestA_2nd.txt')
    assert output == expected_output
    assert expected_output.exists()

def test_clone_file_one_keyword__reference_no_value(temp_dir):
    fn = 'ERP' + abbreviate_date(local=True) + 'a__example.txt'
    fill_folder(temp_dir, 'notes.txt', fn)
    args = parse_args([fn, '--keywords', 'TestA', '--reference'])
    os.chdir(temp_dir)
    output = process_nxt(args)
    expected_output = temp_dir / ('ERP' + abbreviate_date(local=True) + 'b_a__TestA.txt')
    assert output == expected_output
    assert expected_output.exists()