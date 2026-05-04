from contexere.data.context import confirm_project_identifier

def test_confirm_project_identifier():
    match, project = confirm_project_identifier('ERP')
    assert match is not None
    assert project == 'ERP'

    match, project = confirm_project_identifier('erp')
    assert match is not None
    assert project == 'erp'

def test_confirm_project_identifier_failed_too_short():
    match, project = confirm_project_identifier('E')
    assert match is None
    assert project is None
