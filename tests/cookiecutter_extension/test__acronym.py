from contexere.cookiecutter_extension import _acronym as acronym

def test_all_words():
    assert acronym("Example Research Project") == 'ERP'
    assert acronym("Example research Project") == 'ErP'
    assert acronym("example research project") == 'erp'

def test_underscores_and_dashes():
    assert acronym("Example-Research-Project") == 'ERP'
    assert acronym("Example-Research_Project") == 'ERP'
    assert acronym("Example_Research_Project") == 'ERP'
    assert acronym("Example Research_Project") == 'ERP'