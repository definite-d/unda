# Unda
![Downloads](https://img.shields.io/pypi/dm/unda.svg?style=flat)
![GitHub forks](https://img.shields.io/github/forks/definite-d/unda?logo=github&style=flat)
![PyPi Version](https://img.shields.io/pypi/v/unda?style=flat)
![Python Versions](https://img.shields.io/pypi/pyversions/unda.svg?style=flat&logo=python])
![License](https://img.shields.io/pypi/l/unda.svg?style=flat&version=latest)

````text
pip install unda
````

[Official Documentation](https://definite-d.github.io/unda/)

[Quick Start User Guide](https://github.com/definite-d/unda/blob/main/USERGUIDE.md)

## What's Unda?
Unda is a Python 3 module which provides state-based undo and redo functionality for Python objects.

## How does it work?

Unda's core interface is the UndaClient object.

The Client regards the objects it provides functionality for as __targets__. A collection of relevant data about a
target (e.g. the attributes of that object) is regarded as a __state__. Unda works mainly by saving such state data; a
process called __updating__. The state data is saved to a data structure known as a __stack__. Unda implements stacks
using the Python [__deque__](https://docs.python.org/3/library/collections.html#collections.deque) object.

Every UndaClient has two stacks. One is used for undo purposes (hence it is known as the __undo stack__), while the
other is used for redo purposes (the __redo stack__). State data obtained by updating specifically gets saved to the
Client's undo stack.

So, when the user (you) needs to undo the target object, the Client first saves the current state of the object to
the redo stack. It then uses the latest state data in the undo stack to basically give back a version of the target that
corresponds to how the target was when the latest update happened. This effectively un-does any changes made to the
target object since the last update occurred. Redo-ing works similarly, but can only be carried out after an undo: a
redo operation takes the latest state in the redo stack and uses it to return the version of the target that existed
prior to the undo operation.

## What's the story behind Unda?
I created Unda to be a part/feature of a desktop application which I'm developing, however, I decided to open-source it,
as I imagined other developers would find such functionality useful in their projects as well.

Developing Unda has been quite the experience, as it's my first time creating such a Python module.

Development began on Wednesday 17th November 2021.

## Why is it called Unda?
Well, because I didn't want to call it Undo.

## Standards
Unda is:

 * versatile; whether you're working with large or small objects, Unda does its best to optimize how it handles states.

 * compact (it's import dependencies all come with the Python standard library),

 * well documented (via docstrings and pdoc3),

 * built using Python 3.7 (in PyCharm),

 * fully PEP-8 compliant (checked with PyCharm),

 * distributed under the OSI-Approved MIT License.
