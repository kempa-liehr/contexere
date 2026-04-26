from contexere.scheme import join_tokens

def test_nothing_to_join_here():
    assert join_tokens('ERP26rJa') == 'ERP26rJa'

def test_something_to_join_here():
    assert join_tokens('ERP26rJa', 'Ib') == 'ERP26rJa_Ib'
    assert join_tokens('ERP26rJa', ['Ib', 'Ha']) == 'ERP26rJa_Ib_Ha'

def test_something_different_to_join():
    assert join_tokens('ERP26rJa', 'keyword', glue='__') == 'ERP26rJa__keyword'
    result = join_tokens('ERP26rJa', ['keywordA', 'keywordB'], glue='__')
    assert result == 'ERP26rJa__keywordA__keywordB'