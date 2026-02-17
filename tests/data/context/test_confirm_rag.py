from contexere.data.context import confirm_rag

def test_confirm_rag_match():
    match, project, date, step, keywords = confirm_rag('ERP26pGa')
    assert match is not None
    assert project == 'ERP'
    assert date == '26pG'
    assert step == 'a'
    assert keywords is None

    match, project, date, step, keywords = confirm_rag('ERP26pGa_')
    assert match is not None
    assert project == 'ERP'
    assert date == '26pG'
    assert step == 'a'
    assert keywords is None

def test_confirm_rag_match_with_dependency():
    match, project, date, step, remainder = confirm_rag('ERP26pGa_9a__test.ipynb')
    assert match is not None
    assert project == 'ERP'
    assert date == '26pG'
    assert step == 'a'
    assert remainder == '9a__test.ipynb'

def test_confirm_rag_match_with_keywords():
    match, project, date, step, keywords = confirm_rag('ERP26pGa_test')
    assert match is not None
    assert project == 'ERP'
    assert date == '26pG'
    assert step == 'a'
    assert keywords == 'test'

    match, project, date, step, keywords = confirm_rag('ERP26pGa__test')
    assert match is not None
    assert project == 'ERP'
    assert date == '26pG'
    assert step == 'a'
    assert keywords == 'test'

    match, project, date, step, keywords = confirm_rag('ERP26pGaa__test')
    assert match is not None
    assert project == 'ERP'
    assert date == '26pG'
    assert step == 'aa'
    assert keywords == 'test'

    match, project, date, step, keywords = confirm_rag('ERP26pGa__test=2')
    assert match is not None
    assert project == 'ERP'
    assert date == '26pG'
    assert step == 'a'
    assert keywords == 'test=2'

def test_confirm_rag_with_spaces_in_filename():
    match, project, date, step, keywords = confirm_rag('ERP26pGa test=2')
    assert match is not None
    assert project == 'ERP'
    assert date == '26pG'
    assert step == 'a'
    assert keywords is None

def test_confirm_rag_no_match_missing_project():
    match, project, date, step, keywords = confirm_rag('26pGa__test=2')
    assert match is None
    assert project is None
    assert date is None
    assert step is None
    assert keywords is None

def test_confirm_rag_no_match_year_too_long():
    match, project, date, step, keywords = confirm_rag('ERP2026pGa__test=2')
    assert match is None
    assert project is None
    assert date is None
    assert step is None
    assert keywords is None

def test_confirm_rag_no_match_month_wrong():
    match, project, date, step, keywords = confirm_rag('ERP2026lGa__test=2')
    assert match is None
    assert project is None
    assert date is None
    assert step is None
    assert keywords is None

def test_confirm_rag_no_match_day_wrong():
    match, project, date, step, keywords = confirm_rag('ERP2026lZa__test=2')
    assert match is None
    assert project is None
    assert date is None
    assert step is None
    assert keywords is None
