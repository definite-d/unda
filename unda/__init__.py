"""
[![Downloads](https://static.pepy.tech/badge/unda)](https://pepy.tech/project/unda)
![Monthly Downloads](https://img.shields.io/pypi/dm/unda.svg?style=flat)
![GitHub forks](https://img.shields.io/github/forks/definite-d/unda?logo=github&style=flat)
![PyPi Version](https://img.shields.io/pypi/v/unda?style=flat)
![Python Versions](https://img.shields.io/pypi/pyversions/unda.svg?style=flat&logo=python])
![License](https://img.shields.io/pypi/l/unda.svg?style=flat&version=latest)

````text
pip install unda
````

# Introduction

Welcome to Unda's Documentation!

Contains technical details for the classes and functions. Not intended to be a [starter tutorial](https://github.com/definite-d/unda/blob/main/USERGUIDE.md).

_This documentation is auto-generated from Markdown-syntax docstrings using pdoc3, so please pardon the huge docstring at
the beginning of the module's source code._

"""

__name__ = "unda"

from .constants import RESERVED_NAMES, DEEPCOPY, LOGGER, __version__
from .unda_manager import UndaManager
from .unda_object import UndaObject
from .unda_client import UndaClient
