import datetime
from jinja2 import Environment
from jinja2.ext import Extension
from tzlocal import get_localzone

from contexere.scheme import abbreviate_date

def _acronym(s):
    """Return the first letter of each word after replacing dashes and underscores with spaces."""
    return ''.join([word[0] for word in
                    s.replace('-', ' ').replace('_', ' ' ).split()])

def _abbrmonth():
    """Return the abbreviated year-month according to the contexere scheme."""
    return abbreviate_date(local=True)[:-1]

def _abbrdate():
    """Return the abbreviated date according to the contexere scheme."""
    return abbreviate_date(local=True)

def _month():
    """Return the month and year of the current date."""
    return datetime.datetime.now(tz=get_localzone()).strftime("%B %Y")

def _first_research_artefact_group():
    """Return the first research artefact group."""
    return _abbrdate() + 'a'

class AcronymExtension(Extension):
    """Registers the `acronym` Jinja2 filter and global callable."""

    def __init__(self, environment: Environment):
        super().__init__(environment)
        # Register as both a filter  ({{ repo_name | acronym }})
        # and a global callable       ({{ acronym(repo_name) }})
        environment.globals["abbrmonth"] = _abbrmonth
        environment.filters["acronym"] = _acronym
        environment.globals["acronym"] = _acronym
        environment.globals["firstRAG"] = _first_research_artefact_group
        environment.globals["month"] = _month
