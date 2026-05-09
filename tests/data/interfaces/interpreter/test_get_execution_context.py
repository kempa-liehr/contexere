from contexere.data.interfaces.interpreter import get_execution_context

def test_Python_interpreter():
    context, name = get_execution_context()
    assert context == '.py'
    assert name == 'pytest'