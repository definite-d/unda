# Unda
````python
pip install unda
````

## What's Unda?
Unda is a Python 3 module which provides state-based undo and redo functionality for Python objects using a 
special manager object.

It does this by creating and managing undo and redo stacks (via Python deques) for each object placed in its care.
Each time an object in its care is updated, a deepcopy of that object is saved to its undo stack, 
essentially functioning as a "state" for that object. Calling an undo on that object simply returns its latest 
state in its undo stack.

## Usage
Please refer to the (super simple) User Guide [here](https://github.com/definite-d/unda/blob/main/USERGUIDE.md).

## Why is it called Unda?
Well, because I didn't want to call it Undo. 

## Standards
Unda is:
 * compact (it's import dependencies all come with the Python standard library), 
 * well documented (via docstrings), 
 * built using Python 3.7 (in PyCharm), 
 * fully PEP-8 compliant (checked with PyCharm), 
 * distributed under the MIT License and 
 * uses type hinting (verified by MyPy).
