import argparse
import logging
from pathlib import Path
import subprocess
import sys

from contexere import __version__
from contexere.clone import clone_file
from contexere.collect import summary
from contexere.conf import __CONTEXERE_CACHE_DB__, __COOKIECUTTER_PATH__
from contexere.data.context import confirm_partial_rag, confirm_project_identifier, confirm_rag
from contexere.data.cache import fill_cache
from contexere.data.interfaces.contextdb import ContextDB
from contexere.scheme import abbreviate_time, suggest_next

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
    parser = argparse.ArgumentParser(description="Suggest name for research artefact")
    parser.add_argument(
        "--version",
        action="version",
        version=f"contexere {__version__}",
    )
    parser.add_argument(
        "-g",
        "--group",
        dest="group",
        type=str,
        default='',
        help="Project identifier for which the next research artefact GROUP will be suggested",
        action="store"
    )
    parser.add_argument("-k",
                        "--keywords",
                        nargs="+",
                        dest="keywords",
                        help="Optional argument for --clone adding one or more keywords to the filename",
                        )
    parser.add_argument(
        "-l",
        "--local",
        dest="local",
        help="Inspect files in current working dir only",
        action="store_true"
    )
    parser.add_argument("-p",
                        "--project",
                        dest="project",
                        help="Create new project directory structure",
                        action="store_true")
    parser.add_argument("-r",
                        "--reference",
                        nargs="+",
                        dest="reference",
                        help="Optional argument for --clone referencing one or more search artefact groups",
                        )
    parser.add_argument(
        "-s",
        "--summary",
        dest="summary",
        help="Summarise files following the naming convention",
        action="store_true"
    )
    parser.add_argument(
        "-t",
        "--time",
        dest="time",
        help="add time abbreviation",
        action="store_true"
    )  
    parser.add_argument(
        "-u",
        "--utc",
        dest="utc",
        help="Generate timestamp with respect to UTC (default is local timezone)",
        action="store_true"
    )
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
    parser.add_argument(
        "target",
        nargs="?",
        help="Either a project identifier, filename, or folder"
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

def process_nxt(args):
    """
    Process the command line arguments while choosing the most sensible action.
    """
    cloned = False
    if args.target is None:
        group = args.group if args.group != '' else summary(Path.cwd(), recursive=~args.local).index[0]
        output = suggest_next(Path.cwd(), project=group, local=~args.utc, recursive=~args.local)
    else:
        path = Path.cwd() / args.target
        if path.is_dir():
            group = args.group if args.group != '' else summary(path, recursive=~args.local).index[0]
            output = suggest_next(path, project=group, local=~args.utc, recursive=~args.local)
        elif path.exists():
            match, project, date, step, remainder = confirm_rag(path.stem)
            if match:
                next_rag = suggest_next(path.parents[0], project=project, local=~args.utc, recursive=(not args.local))
                output, message = clone_file(path, next_rag, reference=args.reference, keywords=args.keywords)
                cloned = True
            else:
                fn = path.name
                raise ValueError(f'Filename `{fn}` does not start with a research artefact group identifier.')
        else:
            match, project = confirm_project_identifier(args.target)
            if match:
                output = suggest_next(Path.cwd(), project=project, local=~args.utc, recursive=~args.local)
            else:
                raise ValueError(f"`The argument `{args.target}` is neither a project identifier nor a filename.")

    if args.time and not cloned:
        output += abbreviate_time(local=~args.utc)
    return output

    return output


def main(args):
    args = parse_args(args)
    setup_logging(args.loglevel)
    if args.project:
        subprocess.call(["ccds", "--output-dir", args.path, str(__COOKIECUTTER_PATH__)])
    elif args.summary:
        _logger.debug("Start building context ...")
        try:
            print(summary(args.path, recursive=~args.local))
        except ValueError as error:
            _logger.warning(error)
    else:
        output = process_nxt(args)
        print(output)
    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
