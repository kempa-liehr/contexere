from contexere.data.context import get_file_stem

def test_get_file_stem_without_parameters():
    fn = get_file_stem()
    assert 'pytest' == fn

def test_get_file_stem_with_keyword():
    fn = get_file_stem('Test')
    assert 'pytest__Test' == fn

def test_get_file_stem_with_keywords():
    fn = get_file_stem('TestA', 'TestB')
    assert 'pytest__TestA__TestB' == fn

def test_get_file_stem_with_parameters():
    fn = get_file_stem(TestA=3, TestB='vier')
    assert 'pytest__TestA_3__TestB_vier' == fn

    fn = get_file_stem(**{'TestA': 3, 'Test B': 'vier'})
    assert fn == 'pytest__TestA_3__TestB_vier'

def test_get_file_stem_with_keywords_andparameters():
    fn = get_file_stem("A", "b c", TestA=3, TestB='vier')
    assert fn == 'pytest__A__b_c__TestA_3__TestB_vier'

