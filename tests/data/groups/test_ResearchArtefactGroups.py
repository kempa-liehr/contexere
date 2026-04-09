import pytest

from contexere.data.groups import ResearchArtefactGroup

def test_initialization():
    group = ResearchArtefactGroup('ERP26rAa')
    assert isinstance(group, ResearchArtefactGroup)
    assert group.project == 'ERP'
    assert group.date == '26rA'
    assert group.step == 'a'

    with pytest.raises(ValueError):
        group = ResearchArtefactGroup('26rAa')

def test_AttributeError():
    group = ResearchArtefactGroup('ERP26rAa')

    with pytest.raises(AttributeError):
        print(group.no_attribute)

def test_common():
    group = ResearchArtefactGroup('ERP26rAa')

    assert 'ERP26rAa' == group.common('ERP26rAa')
    assert 'ERP26rA' == group.common('ERP26rAb')
    assert 'ERP26r' == group.common('ERP26r9a')
    assert 'ERP26' == group.common('ERP26q9a')
    assert 'ERP' == group.common('ERP25q9a')

def test_frozen_attributes():
    group = ResearchArtefactGroup('ERP26rAa')
    
    with pytest.raises(AttributeError):
        group.project = 'test'