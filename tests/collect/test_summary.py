import pytest

from contexere.collect import summary
@pytest.fixture()
def temp_dir(tmp_path_factory):
    # Create a named base directory for the session
    base = tmp_path_factory.mktemp("session_data")
    return base

def fill_folder(path, *files):
    for fn in files:
        (path / fn).write_text("x", encoding="utf-8")

def test_three_related_files_different_projects_and_folder_non_recursive(temp_dir):
    fill_folder(temp_dir, 'ERP26pAa_example.txt', 'ERQ26pBa_example.txt', 'ERP26pAa_data.csv')
    sub_dir = temp_dir / 'sub_dir'
    sub_dir.mkdir()
    fill_folder(sub_dir, 'ERP26pAa_example.png')
    summary_df = summary(temp_dir)
    print(summary_df)
    assert len(summary_df) == 2
    assert (summary_df.index == ['ERQ', 'ERP']).sum() == 2
    assert (summary_df['RAGs'] == [1, 1]).sum() == 2
    assert (summary_df['Files'] == [1, 2]).sum() == 2
    assert (summary_df['Latest'] == ['26pBa', '26pAa']).sum() == 2

def test_buffered_context():
    buffer = {'ERP': {'26pA': {'a': ['ERP26pAa_data.csv', 'ERP26pAa_example.txt']}},
              'ERQ': {'26pB': {'a': ['ERQ26pBa_example.txt']}}
              }
    summary_df = summary(temp_dir, buffered_context=buffer)
    print(summary_df)
    assert len(summary_df) == 2
    assert (summary_df.index == ['ERQ', 'ERP']).sum() == 2
    assert (summary_df['RAGs'] == [1, 1]).sum() == 2
    assert (summary_df['Files'] == [1, 2]).sum() == 2
    assert (summary_df['Latest'] == ['26pBa', '26pAa']).sum() == 2
def test_three_related_files_different_projects_and_folder_recursive(temp_dir):
    fill_folder(temp_dir, 'ERP26pAa_example.txt', 'ERQ26pBa_example.txt', 'ERP26pAa_data.csv')
    sub_dir = temp_dir / 'sub_dir'
    sub_dir.mkdir()
    fill_folder(sub_dir, 'ERP26pAa_example.png')
    summary_df = summary(temp_dir, recursive=True)
    assert len(summary_df) == 2
    assert (summary_df.index == ['ERQ', 'ERP']).sum() == 2
    assert (summary_df['RAGs'] == [1, 1]).sum() == 2
    assert (summary_df['Files'] == [1, 3]).sum() == 2
    assert (summary_df['Latest'] == ['26pBa', '26pAa']).sum() == 2

def test_three_related_files_different_projects_and_folder_recursive__filter_ERP(temp_dir):
    fill_folder(temp_dir, 'ERP26pAa_example.txt', 'ERQ26pBa_example.txt', 'ERP26pAa_data.csv')
    sub_dir = temp_dir / 'sub_dir'
    sub_dir.mkdir()
    fill_folder(sub_dir, 'ERP26pAa_example.png')
    summary_df = summary(temp_dir, recursive=True, project_filter='ERP')
    assert len(summary_df) == 1
    assert summary_df.index == ['ERP']
    assert (summary_df['RAGs'] == [1]).sum() == 1
    assert (summary_df['Files'] == [3]).sum() == 1
    assert (summary_df['Latest'] == ['26pAa']).sum() == 1

def test_error_on_folder_without_context(temp_dir):
    fill_folder(temp_dir, 'test.txt')
    with pytest.raises(ValueError):
        summary(temp_dir)