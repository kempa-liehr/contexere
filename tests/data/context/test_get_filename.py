from contexere.data.context import get_filename

def test_get_filename_without_parameters():
    fn = get_filename()
    assert 'pytest' == fn

def test_get_filename_with_keyword():
    fn = get_filename('Test')
    assert 'pytest__Test' == fn

def test_get_filename_with_keywords():
    fn = get_filename('TestA', 'TestB')
    assert 'pytest__TestA__TestB' == fn

def test_get_filename_with_parameters():
    fn = get_filename(TestA=3, TestB='vier')
    assert 'pytest__TestA_3__TestB_vier' == fn

    fn = get_filename(**{'TestA': 3, 'Test B': 'vier'})
    assert fn == 'pytest__TestA_3__TestB_vier'

def test_get_filename_with_keywords_andparameters():
    fn = get_filename("A", "b c", TestA=3, TestB='vier')
    assert fn == 'pytest__A__b_c__TestA_3__TestB_vier'

