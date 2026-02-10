from pathlib import Path
import pytest

from contexere.collect import build_context
@pytest.fixture()
def temp_dir(tmp_path_factory):
    # Create a named base directory for the session
    base = tmp_path_factory.mktemp("session_data")
    return base

def fill_folder(path, *files):
    print(type(temp_dir), temp_dir)
    for fn in files:
        (path / fn).write_text("x", encoding="utf-8")
def test_empty_directory(temp_dir):
    context, timeline = build_context(temp_dir)
    assert context == {} and timeline == {}

def test_unrelated_file(temp_dir):
    fill_folder(temp_dir, 'notes.txt')
    context, timeline = build_context(temp_dir)
    assert context == {} and timeline == {}

def test_unrelated_and_related_file(temp_dir):
    fill_folder(temp_dir, 'notes.txt', 'ERP26pBa_example.txt')
    context, timeline = build_context(temp_dir)
    assert context == {'ERP': {'26pB': {'a': [temp_dir / 'ERP26pBa_example.txt']}}}
    assert timeline == {'26pB': {'ERP': {'a': [temp_dir / 'ERP26pBa_example.txt']}}}

def test_two_related_files(temp_dir):
    fill_folder(temp_dir, 'ERP26pAa_example.txt', 'ERP26pBa_example.txt')
    context, timeline = build_context(temp_dir)
    assert context['ERP']['26pA']['a'] == [temp_dir / 'ERP26pAa_example.txt']
    assert context['ERP']['26pB']['a'] == [temp_dir / 'ERP26pBa_example.txt']
    assert timeline['26pA'] == {'ERP': {'a': [temp_dir / 'ERP26pAa_example.txt']}}
    assert timeline['26pB'] == {'ERP': {'a': [temp_dir / 'ERP26pBa_example.txt']}}
def test_three_related_files(temp_dir):
    fill_folder(temp_dir, 'ERP26pAa_example.txt', 'ERP26pBa_example.txt', 'ERP26pAa_data.csv')
    context, timeline = build_context(temp_dir)
    assert set(context['ERP']['26pA']['a']) == set([temp_dir / 'ERP26pAa_data.csv',
                                                   temp_dir / 'ERP26pAa_example.txt'])
    assert context['ERP']['26pB']['a'] == [temp_dir / 'ERP26pBa_example.txt']
    assert set(timeline['26pA']['ERP']['a']) == set([temp_dir / 'ERP26pAa_data.csv',
                                                    temp_dir / 'ERP26pAa_example.txt'])
    assert timeline['26pB'] == {'ERP': {'a': [temp_dir / 'ERP26pBa_example.txt']}}

def test_three_related_files_different_projects(temp_dir):
    fill_folder(temp_dir, 'ERP26pAa_example.txt', 'ERQ26pBa_example.txt', 'ERP26pAa_data.csv')
    context, timeline = build_context(temp_dir)
    assert set(context['ERP']['26pA']['a']) == set([temp_dir / 'ERP26pAa_data.csv',
                                                   temp_dir / 'ERP26pAa_example.txt'])
    assert context['ERQ']['26pB']['a'] == [temp_dir / 'ERQ26pBa_example.txt']
    assert set(timeline['26pA']['ERP']['a']) == set([temp_dir / 'ERP26pAa_data.csv',
                                                    temp_dir / 'ERP26pAa_example.txt'])
    assert timeline['26pB'] == {'ERQ': {'a': [temp_dir / 'ERQ26pBa_example.txt']}}
