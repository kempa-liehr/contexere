import configparser
import os
from pathlib import Path

__month_dict__ = dict([(m, abbr) for m, abbr in zip(range(1, 13),
                                               map(chr, range(ord('o'), ord('z') + 1))
                                               )])
__days__ = list(map(str, range(1, 10))) + list(map(chr, range(ord('A'), ord('V') + 1)))
__day_dict__ = dict([(d, abbr) for d, abbr in zip(range(1, 32), __days__)])
__hours__ = list(map(str, range(1, 1))) + list(map(chr, range(ord('a'), ord('x') + 1)))

__CONTEXERE_CACHE_DIR__ = Path.home() / '.contexere'
__MAX_EMAIL_LENGTH_BYTES__ = 255
__MAX_FILE_EXTENSION_LENGTH_BYTES__ = 12
__MAX_FILENAME_LENGTH_BYTES__ = 255
__MAX_KEYWORD_LENGTH_BYTES__ = 64
__MAX_PATH_LENGTH_BYTES__ = 4096
__MAX_PROJECT_ID_LENGTH__ = 7
__MAX_QUOTE_LENGTH__ = 255
__MAX_RESEARCHER_NAME_LENGTH__ = 22
__GENERATORS__ = ['.py', '.ipynb']
__IGNORE__ = ['*/.Trash/*', '*.bbl', '*.bst', '*.blt', "*.log",
              "*/.ipynb_checkpoints", "*/build/*", "*-checkpoint.ipynb", "*.pyc"]

if not __CONTEXERE_CACHE_DIR__.exists():
    __CONTEXERE_CACHE_DIR__.mkdir()

__CONTEXERE_CACHE_DB__ = __CONTEXERE_CACHE_DIR__ / 'context.db'

config_file_path = __CONTEXERE_CACHE_DIR__ / 'conf.ini'
if not config_file_path.exists():
    username = os.environ.get('USER') or os.environ.get('USERNAME')
else:
    config = configparser.ConfigParser()

    configuration = config.read(config_file_path)
    # [General]
    # username = This User
    username = configuration['General']['username']
