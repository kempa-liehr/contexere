import configparser
import os
from pathlib import Path

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