"""CLI for the Research Artefact Group Database of the Contexere package"""

import argparse
import logging
from pathlib import Path
import sys

from contexere import __version__
from contexere.conf import __CONTEXERE_CACHE_DB__
from contexere.data.cache import fill_cache
from contexere.data.interfaces.contextdb import ContextDB

__author__ = "Andreas W. Kempa-Liehr"
__copyright__ = "Andreas W. Kempa-Liehr"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Research Artefact Group Database")
    parser.add_argument(
        "--version",
        action="version",
        version=f"contexere {__version__}",
    )
    parser.add_argument(
        "-i",
        "--init-cache",
        dest="init_cache",
        help="Init context cache",
        action="store_true"
    )
    parser.add_argument(dest="path",
                        help="Path to folder with research artefacts (default: current working dir)",
                        nargs='?',
                        type=Path,
                        default=Path.cwd())
    parser.add_argument("-d",
                        "--database",
                        dest="database",
                        help=f"Path to SQLite database (default: {__CONTEXERE_CACHE_DB__})",
                        type=Path,
                        default=__CONTEXERE_CACHE_DB__)
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Start building context...")
    if args.init_cache:
        db = ContextDB(path=args.database)
        fill_cache(db, root=args.path)

    # print(args.project + abbreviate_date() + ending)
    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
