from pathlib import Path

from contexere.clone import next_filename

def test_next_filename_from_template_no_reference():
    fn = next_filename(Path('00_ERP_template.ipynb'), 'ERP26r7a')
    assert fn == 'ERP26r7a.ipynb'

    fn = next_filename(Path('00_ERP_template.ipynb'), 'ERP26r7a', keywords=['test'])
    assert fn == 'ERP26r7a__test.ipynb'

    fn = next_filename(Path('00_ERP_template.ipynb'), 'ERP26r7a', keywords=['test', 'AB'])
    assert fn == 'ERP26r7a__test__AB.ipynb'

def test_next_filename_from_rag():
    fn = next_filename(Path('ERP26r6b_template.ipynb'), 'ERP26r7a')
    assert fn == 'ERP26r7a_6b.ipynb'

def test_next_filename_dublicated_ref():
    fn = next_filename(Path('ERP26r6b_template.ipynb'), 'ERP26r7a', reference=['6b'])
    assert fn == 'ERP26r7a_6b.ipynb'