import pytest

from contexere.clone import next_rag

def test_cyclic_reference():
    with pytest.raises(ValueError):
        next_rag('ERP26r7a', reference=['a'])

def test_wrong_reference():
    with pytest.raises(ValueError):
        next_rag('ERP26r7a', reference=['6'])

def test_one_reference():
    new_rag = next_rag('ERP26r7a', reference=['6a'])
    assert new_rag == 'ERP26r7a_6a'

    new_rag = next_rag('ERP26r7a', reference=['ERP26r6a'])
    assert new_rag == 'ERP26r7a_6a'

def test_two_references():
    new_rag = next_rag('ERP26r7a', reference=['q5a', '6b'])
    assert new_rag == 'ERP26r7a_6b_q5a'

    new_rag = next_rag('ERP26r7a', reference=['6b', 'q5a'])
    assert new_rag == 'ERP26r7a_6b_q5a'

def test_two_references_different_project():
    new_rag = next_rag('ERP26r7a', reference=['DS26q5a', '6b', 'q5a'])
    assert new_rag == 'ERP26r7a_6b_q5a_DS26q5a'

    new_rag = next_rag('ERP26r7a', reference=['XS25q5a', 'DS26q5a', '6b', 'q5a'])
    assert new_rag == 'ERP26r7a_6b_q5a_DS26q5a_XS25q5a'