"""
![Downloads](https://img.shields.io/pypi/dm/unda.svg?style=flat)
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

This documentation is auto-generated from Markdown-syntax docstrings using pdoc3, so please pardon the huge docstring at
the beginning of the module's source code.

"""
__version__ = '1.1.0.2'


from typing import Dict, Optional
from unda_client import UndaClient

STACK_HEIGHT = 20
RESERVED_NAMES = ['target_dict', 'undo_stack', 'redo_stack', 'stack_height']
DEEPCOPY = 'DEEPCOPY'
LOGGER = 'LOGGER'


def extract_changes(original, changed) -> Optional[Dict]:
    """
    Obtains and returns a dict of changes by comparing two dicts.

    ## Parameters
    ### _original:_
    Dict to compare "changed" against.

    ### _changed:_
    Dict to be compared for differences.
    """
    target_checklist = [(k, changed[k])
                        for k in changed.keys()
                        if k not in RESERVED_NAMES]
    checklist_anomalies = {}
    for key_value, value in target_checklist:
        if original[key_value] != value or key_value not in original.keys():
            checklist_anomalies[key_value] = value
    return checklist_anomalies if len(checklist_anomalies) > 0 else None


class UndaObject:
    """
    A custom class which gives update, undo and redo abilities to any class that inherits from it by adding an
    UndaClient object to its attributes.

    The easiest way to use Unda in my opinion.

    ## Usage

    1. Inherit from this class when creating your desired class, (e.g. MyObject(UndaObject))

    2. At the END of the `__init()__` function, call `UndaObject.__init__(self)`,

    3. At the BEGINNING of any method which may alter the attributes of the objects, call `self.update()`.

    That's it. Any method which step 3 affected can be undone by calling `self.undo()`.


    ## Dealing with Multiple Inheritance and `__init__()` functions.

    If your custom object inherits from more than just `UndaObject`:

    * it must have an `__init__()` function with all the other parent classes' `__init__()` functions (if
    they have such) being called (e.g. `OtherParent.__init__(self)`), and

    * Step 2 must apply; `UndaObject.__init__(self)` must be the last line of your custom object's `__init__()`
    function.

    ## Parameters
    Same as `UndaClient()` where they apply.
    """

    def __init__(self, style: Optional[str] = None, stack_height: Optional[int] = None):
        self.client = UndaClient(self, style=style, stack_height=stack_height)

    def update(self):
        """
        Same as `UndaClient.update()`.
        """
        self.client.update()

    def undo(self, depth: int = 0, quiet: bool = False, inplace: bool = True):
        """
        Same as `UndaClient.undo()`.
        """
        return self.client.undo(depth, quiet, inplace)

    def redo(self, depth: int = 0, quiet: bool = False, inplace: bool = True):
        """
        Same as `UndaClient.redo()`.
        """
        return self.client.redo(depth, quiet, inplace)


class UndaManager:
    """
    `UndaManager` class. Manages undo and redo operations for all objects in its care. Best for managing Undo and Redo
    functionality for multiple objects and existing UndaClients.

    ## Usage

    To use, you can either:

    * pass a dict of `{key: object (or UndaClient)}` pairs as the `starter_objects` parameter,

    * leave the parameters blank and use the `add_client()` or "add_clients()` methods to entrust existing
      `UndaClient`s,

    * or use the `add_object()` or `add_objects()` methods to add objects directly.

    Please do not attempt to add an object by using `UndaManager.objects[key] = target` unless the "target" is an
    `UndaClient`. This will not work as intended, because `UndaManager`s deal with `UndaClient`s, and not the objects
    themselves. Always use the `add_object()` function instead for ordinary objects.

    ## Parameters
    ### _starter_objects:_
    A dict of objects/`UndaClient`s/both to be entrusted to the UndaManager in the pattern: 
    `{key: object (or UndaClient)}`

    ### _stack_height:_
    An integer representing the maximum number of states to store in any stack created by this `UndaManager`. 

    """
    starter_objects: Optional[Dict] = None

    def __init__(self, starter_objects: Optional[Dict] = None, stack_height: int = STACK_HEIGHT) -> None:
        self.stack_height: int = stack_height
        self.starter_objects: Optional[Dict] = starter_objects
        self.objects: Dict = {}
        if self.starter_objects is not None:
            self.objects.update({x: UndaClient(self.starter_objects[x])
                                 for x in self.starter_objects if not issubclass(x, UndaClient)})
            self.objects.update({x: self.starter_objects[x]
                                 for x in self.starter_objects if issubclass(x, UndaClient)})

    def add_object(self, key: str, target: object) -> None:
        """
        Entrusts an object into the UndaManager's care.
        Please do not attempt to add an object by using "UndaManager.objects[key] = target" (direct dictionary edits),
        as this will not work as intended. Always use this function instead.

        ## Parameters
        ### _key:_
        A key to reference the object. Could be anything, even the class name.

        ### _target:_
        The object itself.
        """
        self.objects[key] = UndaClient(target)

    def add_client(self, key: str, client: UndaClient) -> None:
        """
        Entrusts an already existing UndaClient object into the UndaManager's care.
        Unlike "add_object()", direct object dictionary edits to add a Client will work normally. It's ill-advised
        though; it's best to use this function.

        ## Parameters
        ### _key:_
        A key to reference the object. Could be anything, even the class name.

        ### _client:_
        The UndaClient object to entrust.
        """
        client.entrust(key, self)

    def update_all(self) -> None:
        """
        Same as "update", but applies it to all keys.
        """
        for key in self.objects.keys():
            self.objects[key].update()

    def clear_all_stacks(self) -> None:
        """
        Calls the "clear_stacks" function for all objects.
        """
        for key in self.objects.keys():
            self.objects[key].clear_stacks()

    def clear_undo_stacks(self) -> None:
        """
        Calls the "clear_undo_stack" function for all objects.
        """
        for key in self.objects.keys():
            self.objects[key].clear_undo_stack()

    def clear_redo_stacks(self) -> None:
        """
        Calls the "clear_redo_stack" function for all objects.
        """
        for key in self.objects.keys():
            self.objects[key].clear_redo_stack()

    def undo(self, key, depth: int = 0, quiet: bool = False, inplace: bool = False):
        """
        Calls the `undo()` function of the UndaClient referenced by the specified key.

        ## Parameters

        ### _key_:
        The string used to reference a specific `UndaClient`.

        All other parameters are the same as `UndaClient.undo()` where they apply.
        """
        self.objects[key].undo(depth, quiet, inplace)

    def undo_all(self, depth: int = 0, quiet: bool = False, inplace: bool = False) -> Dict:
        """
        Same as undo, but applies to all objects in the UndaManager's care, and returns a dict in the format:
        {key: result}

        ## Parameters
        Same as `UndaClient.undo()`
        """
        return {key: self.objects[key].undo(depth, quiet, inplace) for key in self.objects.keys()}

    def redo(self, key, depth: int = 0, quiet: bool = False, inplace: bool = False):
        """
        Calls the `redo()` function of the UndaClient referenced by the specified key.

        ## Parameters

        ### _key_:
        The string used to reference a specific `UndaClient`.

        All other parameters are the same as `UndaClient.redo()` where they apply.
        """
        self.objects[key].redo(depth, quiet, inplace)

    def redo_all(self, depth: int = 0, quiet: bool = False, inplace: bool = False) -> Dict:
        """
        Same as redo, but applies to all objects in the UndaManager's care, and returns a dict in the format:
        {key: result}

        ## Parameters
        Same as `UndaClient.redo()`
        """
        return {key: self.objects[key].redo(depth, quiet, inplace) for key in self.objects.keys()}
