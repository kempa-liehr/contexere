# ccds_extensions.py
from jinja2 import Environment
from jinja2.ext import Extension


def _acronym(s: str) -> str:
    """Return the first letter of each word after replacing dashes and underscores with spaces."""
    return ''.join([word[0] for word in
                    s.replace('-', ' ').replace('_', ' ' ).split()])


class AcronymExtension(Extension):
    """Registers the `acronym` Jinja2 filter and global callable."""

    def __init__(self, environment: Environment):
        super().__init__(environment)
        # Register as both a filter  ({{ repo_name | acronym }})
        # and a global callable       ({{ acronym(repo_name) }})
        environment.filters["acronym"] = _acronym
        environment.globals["acronym"] = _acronym