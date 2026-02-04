from pathlib import Path
from contexere.discover import extend_timeline

def test_extend_timeline_empty_dict():
    timeline = dict()
    extend_timeline(timeline, '26p4', 'test', 'a', Path.home())
    assert timeline['26p4']['test']['a'] == [Path.home()]

    extend_timeline(timeline, '26p4', 'test', 'a', Path.home())
    assert timeline['26p4']['test']['a'] == [Path.home(), Path.home()]

    extend_timeline(timeline, '26p4', 'test', 'b', Path.home())
    assert timeline['26p4']['test']['b'] == [Path.home()]


