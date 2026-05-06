from contexere.data.context import clean_up_remainder

def test_no_reference_in_remainder():
    result = clean_up_remainder('simple_remainder')
    assert result == 'simple_remainder'

def test_one_reference_in_remainder():
    result = clean_up_remainder('a__simple_remainder')
    assert result == 'simple_remainder'

def test_two_references_in_remainder():
    result = clean_up_remainder('a_Ba__simple_remainder')
    assert result == 'simple_remainder'

def test_one_reference_in_remainder_with_two_keywords():
    result = clean_up_remainder('a__simple_remainder__another')
    assert result == 'simple_remainder__another'

def test_no_remainder():
    result = clean_up_remainder('')
    assert result == ''