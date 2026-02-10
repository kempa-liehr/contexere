from pathlib import Path
from contexere.collect import grow_context

def test_grow_context_empty_dict():
    context = dict()
    grow_context(context, 'test', '26p4', 'a', Path.home())
    assert context['test']['26p4']['a'] == [Path.home()]

    grow_context(context, 'test', '26p4', 'a', Path.home())
    assert context['test']['26p4']['a'] == [Path.home(), Path.home()]

    grow_context(context, 'test', '26p4', 'b', Path.home())
    assert context['test']['26p4']['b'] == [Path.home()]


