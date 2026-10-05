from contexere.data.context import confirm_stage

def test_stage_confirmed():
    date, step = confirm_stage('26x6a')
    assert date == '26x6'
    assert step == 'a'

    date, step = confirm_stage('2026x6a')
    assert date is None and step is None


