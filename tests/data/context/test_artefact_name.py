from contexere.data.context import artefact_name

def test_artefact_name_without_parameters():
    fn = artefact_name()
    assert 'pytest' == fn

def test_artefact_name_with_keyword():
    fn = artefact_name('Test')
    assert 'pytest__Test' == fn

def test_artefact_name_with_keywords():
    fn = artefact_name('TestA', 'TestB')
    assert 'pytest__TestA__TestB' == fn

def test_artefact_name_with_parameters():
    fn = artefact_name(TestA=3, TestB='vier')
    assert 'pytest__TestA_3__TestB_vier' == fn

    fn = artefact_name(**{'TestA': 3, 'Test B': 'vier'})
    assert fn == 'pytest__TestA_3__TestB_vier'

def test_artefact_name_with_keywords_andparameters():
    fn = artefact_name("A", "b c", TestA=3, TestB='vier')
    assert fn == 'pytest__A__b_c__TestA_3__TestB_vier'

