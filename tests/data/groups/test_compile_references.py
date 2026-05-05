import pytest

from contexere.data.groups import compile_references


def test_one_past_reference():
    assert ['a'] == compile_references('ERP26s5b', ['a'])
    assert ['a'] == compile_references('ERP26s5b', ['ERP26s5a'])

def test_invalid_reference():
    with pytest.raises(ValueError):
        compile_references('ERP26s5a', ['a'])

    with pytest.raises(ValueError):
        compile_references('ERP26s5a', ['b'])

def test_two_past_references():
    expected = ['a', '4b']
    assert expected == compile_references('ERP26s5b', ['a', 's4b'])
    assert expected == compile_references('ERP26s5b', ['ERP26s5a', 's4b'])
    assert expected == compile_references('ERP26s5b', ['a', 'ERP26s4b'])
    assert expected == compile_references('ERP26s5b', ['ERP26s4b', 'ERP26s5a'])

def test_two_past_references_differnt_month():
    expected = ['a', 'r4b']
    assert expected == compile_references('ERP26s5b', ['a', 'r4b'])
    assert expected == compile_references('ERP26s5b', ['ERP26s5a', 'r4b'])
    assert expected == compile_references('ERP26s5b', ['a', 'ERP26r4b'])
    assert expected == compile_references('ERP26s5b', ['ERP26r4b', 'ERP26s5a'])

def test_two_past_references_different_year():
    expected = ['a', '25r4b']
    assert expected == compile_references('ERP26s5b', ['a', '25r4b'])
    assert expected == compile_references('ERP26s5b', ['ERP26s5a', '25r4b'])
    assert expected == compile_references('ERP26s5b', ['a', 'ERP25r4b'])
    assert expected == compile_references('ERP26s5b', ['ERP25r4b', 'ERP26s5a'])

def test_three_past_references_different_month_different_project():
    expected = ['a', 'r4b', 'ABC26s5a']
    assert expected == compile_references('ERP26s5b', ['a', 'r4b', 'ABC26s5a'])
    assert expected == compile_references('ERP26s5b', ['ERP26s5a', 'ABC26s5a', 'r4b'])
    assert expected == compile_references('ERP26s5b', ['ABC26s5a', 'a', 'ERP26r4b'])
    assert expected == compile_references('ERP26s5b', ['ERP26r4b', 'ERP26s5a', 'ABC26s5a'])

def test_three_past_references_different_month_different_projects():
    expected = ['a', 'r4b', 'ABC26s5a', 'BBC26s5a']
    assert expected == compile_references('ERP26s5b', ['a', 'r4b', 'BBC26s5a', 'ABC26s5a'])
    assert expected == compile_references('ERP26s5b', ['BBC26s5a', 'ERP26s5a', 'ABC26s5a', 'r4b'])
    assert expected == compile_references('ERP26s5b', ['ABC26s5a', 'BBC26s5a', 'a', 'ERP26r4b'])
    assert expected == compile_references('ERP26s5b', ['ERP26r4b', 'BBC26s5a', 'ERP26s5a', 'ABC26s5a'])

def test_three_past_references_different_month_different_projects_temporal_error():
    with pytest.raises(ValueError):
        compile_references('ERP26s5b', ['a', 'r4b', 'ABC26s5a', 'ABC26s6a'])
        compile_references('ERP26s5b', ['a', 'r4b', 'BBC26s5a', 'ABC26s6a'])

