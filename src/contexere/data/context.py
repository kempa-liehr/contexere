import re

# Define the scheme with named groups
__pattern__ = re.compile(r'^(?P<project>[a-zA-Z]+)(?P<date>[0-9]{2}[o-z][1-9A-V])(?P<step>[a-z]+)(?:_+(?P<kwds>.+))?_*')

def confirm_rag(token, pattern=__pattern__):
    match = pattern.match(token)
    if match:
        project = match.group('project')
        date = match.group('date')
        step = match.group('step')
        keywords = match.group('kwds')
    else:
        project, date, step, keywords = None, None, None, None
    return match, project, date, step, keywords
