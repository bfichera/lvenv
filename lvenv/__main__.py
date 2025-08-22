from venv import create
from pathlib import Path
import argparse


parser = argparse.ArgumentParser(
    prog='lvenv',
    description=(
        'Creates virtual Python environments in'
        ' one or more target directories. Overrides the root logger in such'
        ' away that all logging.info, logging.warnings, ... calls are written'
        ' to a file in the project directory / .log'
    )
)
parser.add_argument(
    'ENV_DIR',
    help='A directory to create the environment in.'
)
parser.add_argument(
    '--system-site-packages',
    action='store_true',
    help='Give the virtual environment access to the system site-packages dir.'
)
group = parser.add_mutually_exclusive_group()
group.add_argument(
    '--symlinks',
    action='store_true',
    help=(
        'Try to use symlinks rather than copies, when symlinks are not the'
        ' default for the platform.'
    )
)
group.add_argument(
    '--copies',
    action='store_true',
    help=(
        'Try to use copies rather than symlinks, even when symlinks are the'
        ' default for the platform.'
    )
)
parser.add_argument(
    '--clear',
    action='store_true',
    help=(
        'Delete the contents of the environment directory if it already'
        ' exists, before environment creation.'
    )
)
parser.add_argument(
    '--upgrade',
    action='store_true',
    help=(
        'Upgrade the environment directory to use this version of Python,'
        ' assuming Python has been upgraded in-place.'
    )
)
parser.add_argument(
    '--without-pip',
    action='store_true',
    help=(
        'Skips installing or upgrading pip in the virtual environment (pip is'
        ' bootstrapped by default)'
    )
)
parser.add_argument(
    '--prompt',
    metavar='PROMPT',
    help='Provides an alternative prompt prefix for this environment.'
)
parser.add_argument(
    '--upgrade-deps',
    action='store_true',
    help=(
        'Upgrade core dependencies: pip setuptools to the latest version in'
        ' PyPI'
    )
)

cfg = parser.parse_args()

symlinks = cfg.symlinks and not cfg.copies

try:
    create(
        cfg.ENV_DIR,
        system_site_packages=cfg.system_site_packages,
        clear=cfg.clear,
        symlinks=symlinks,
        with_pip=not cfg.without_pip,
        prompt=cfg.prompt,
        upgrade_deps=cfg.upgrade_deps,
    )
except Exception:
    create(
        cfg.ENV_DIR,
        system_site_packages=cfg.system_site_packages,
        clear=cfg.clear,
        symlinks=True,
        with_pip=not cfg.without_pip,
        prompt=cfg.prompt,
        upgrade_deps=cfg.upgrade_deps,
    )

sitecustomize_py_text = r"""import logging
from pathlib import Path
from datetime import datetime
import socket
import sys
import atexit
import subprocess
from pip._internal.operations.freeze import freeze


def get_git_hash():
    r = subprocess.run(
        ['git', 'rev-parse', 'HEAD'],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        return
    return r.stdout.strip()


def makelog():
    now = datetime.now()
    datefmt = (
        f'{now.year}_{now.month:02d}_{now.day:02d}_{now.hour:02d}'
        f'_{now.minute:02d}_{now.second:02d}_{now.microsecond}'
    )
    hostname = socket.gethostname()
    logdir = Path.cwd() / '.log'
    if not logdir.exists():
        logdir.mkdir()
    c = len(list(logdir.glob(datefmt+'*'+'.log')))+1
    logpath = logdir / f'{datefmt}_{hostname}_{c:04d}.log'
    return logpath


def getfilepath():
    return Path(sys.argv[0]).absolute()


def getargs():
    return sys.argv[1:]


def getfilecontents():
    path = getfilepath()
    with open(path, 'r') as fh:
        return fh.read()


def fmtfreeze():
    return '    \n'.join(freeze())


if sys.argv[0] and not sys.argv[0].startswith('-'):

    startmsg = (
        f'\nInitialized python call.\n'
        f'FILENAME: {getfilepath().as_posix()}\n'
        f'COMMIT: {get_git_hash()}\n'
        f'ARGV: {getargs()}\n'
        f'REQUIREMENTS:\n{fmtfreeze()}\n'
        f'FILE CONTENTS:\n{getfilecontents()}'
    )

    logpath = makelog()
    filehandler = logging.FileHandler(logpath)
    formatter = logging.Formatter(
        fmt=(
            '***START RECORD***\n'
            'LEVEL: %(levelname)s\n'
            'DATETIME: %(asctime)s\n'
            'NAME: %(name)s\n'
            'PATH: %(pathname)s\n'
            'LINENO: %(lineno)d\n'
            'MESSAGE: \n%(message)s\n'
            '***END RECORD***\n'
        ),
    )
    filehandler.setFormatter(formatter)
    filehandler.setLevel(logging.DEBUG)
    rootlogger = logging.getLogger()
    rootlogger.setLevel(logging.INFO)
    rootlogger.addHandler(filehandler)
    rootlogger.info(startmsg)

    def on_exit():
        rootlogger.info('Exiting')

    atexit.register(on_exit)"""

for site_packages in Path.cwd().glob(
    cfg.ENV_DIR+'/lib'+'/python*'+'/site-packages'
):
    with open(site_packages / 'sitecustomize.py', 'w') as fh:
        fh.write(sitecustomize_py_text)
