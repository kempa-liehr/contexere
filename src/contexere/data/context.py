import re

# Define the scheme with named groups
__pattern__ = re.compile(r'(?P<project>[a-zA-Z]*)(?P<date>[0-9]{2}[o-z][1-9A-V])(?P<step>[a-z]*)_?')

