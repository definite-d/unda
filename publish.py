"""
Build script for unda.

Usage:
publish.py [-h] [--upload_to UPLOAD_TO] task

`task` may be `build` (builds the project only),
    `upload` (uploads the project to `UPLOAD_TO` only),
    or `complete` (does both).
`UPLOAD_TO` may be 'legacy' or 'l' for legacy PyPi, or 'test' or 't' for TestPyPi
"""
from os import system
from argparse import ArgumentParser as p
from unda import __version__ as VERSION
MODULE_NAME = "unda"

DEFAULT_UPLOAD_DESTINATION = 'legacy'
TOKEN = 'Sorry, I can\'t include the token publicly!'

def build() -> None:
    """
    Builds the project.
    :return: None
    """
    system('python -m build')


def upload_testpypi(version: str = VERSION) -> None:
    """
    Uploads the project to PyPi's test server.
    :param version: The specific version to upload.
    :return: None
    """
    system(f'twine upload --username __token__ --password {TOKEN} --repository testpypi dist/{MODULE_NAME}-{version}*')


def upload_legacy(version: str = VERSION) -> None:
    """
    Uploads the project to PyPi's legacy servers.
    :param version: The specific version to upload
    :return: None
    """
    system(f'twine upload --username __token__ --password {TOKEN} --repository-url https://upload.pypi.org/legacy/ dist/{MODULE_NAME}-{version}*')


def _main_cli() -> None:
    """
    Internal use only.

    Handles the CLI for the script.

    Runs when the script is run.
    :return: None
    """
    parser = p()
    parser.add_argument('task',
                        help='Defines what the script will do; \'build\', \'upload\' or \'complete\' (does both).')
    parser.add_argument('--upload_to',
                        help='Where to upload the distro to. '
                             'Should either be \'test\' (to upload to test PyPi) or \'legacy\'. '
                             f'Defaults to {DEFAULT_UPLOAD_DESTINATION}.'
                             'Useful when building.')
    args = parser.parse_args()
    if args.task:
        if args.task == 'build' or args.task == 'complete':
            build()
        if args.task == 'upload' or args.task == 'complete':
            if not args.upload_to:
                args.upload_to = DEFAULT_UPLOAD_DESTINATION
            if args.upload_to in ('test', 't'):
                upload_testpypi()
            elif args.upload_to in ('legacy', 'l'):
                upload_legacy()


if __name__ == '__main__':
    pass
else:
    _main_cli()


