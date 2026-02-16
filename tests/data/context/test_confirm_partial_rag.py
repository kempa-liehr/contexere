from contexere.data.context import confirm_partial_rag

def test_confirm_partial_rag_match_complete():
    match, project, date, step = confirm_partial_rag('ERP26pGa')
    assert match is not None
    assert project == 'ERP'
    assert date == '26pG'
    assert step == 'a'

    match, project, date, step = confirm_partial_rag('ERP26pGa_')
    assert match is None

def test_confirm_partial_rag_match_counter():
    match, project, date, step = confirm_partial_rag('a')
    assert match is not None
    assert project is None
    assert date == ''
    assert step == 'a'

    match, project, date, step = confirm_partial_rag('aa')
    assert match is not None
    assert project is None
    assert date == ''
    assert step == 'aa'

    match, project, date, step = confirm_partial_rag('aaa')
    assert match is None

def test_confirm_partial_date_rag_match():
    match, project, date, step = confirm_partial_rag('Ga')
    assert match is not None
    assert project is None
    assert date == 'G'
    assert step == 'a'

    match, project, date, step = confirm_partial_rag('pGa')
    assert match is not None
    assert project is None
    assert date == 'pG'
    assert step == 'a'

    match, project, date, step = confirm_partial_rag('26pGa')
    assert match is not None
    assert project is None
    assert date == '26pG'
    assert step == 'a'