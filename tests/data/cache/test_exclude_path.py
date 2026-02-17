from pathlib import Path

from contexere.data.cache import exclude_path

def test_exclude_path_keyword():
    result = exclude_path(Path('/Users/testuser/.Trash/DS24sGd'),
                          ignore=['*/.Trash/*'])
    assert result == True