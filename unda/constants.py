from .version import Version

VERSION = Version(1, 1, 2)
__version__ = str(VERSION)

STACK_HEIGHT = 30
RESERVED_NAMES = ['target_dict', 'undo_stack', 'redo_stack', 'stack_height']
DEEPCOPY = 'DEEPCOPY'
LOGGER = 'LOGGER'
