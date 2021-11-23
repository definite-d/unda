"""
![Downloads](https://img.shields.io/pypi/dm/unda.svg?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/definite-d/unda?logo=github&style=flat-square)
![PyPi Version](https://img.shields.io/pypi/v/unda?style=flat-square)
![Python Versions](https://img.shields.io/pypi/pyversions/unda.svg?style=flat-square&logo=python])
![License](https://img.shields.io/pypi/l/unda.svg?style=flat-square&version=latest)

````text
pip install unda
````

# Introduction

Welcome to Unda's Documentation!

Contains technical details for the classes and functions. Not intended to be a [starter tutorial](https://github.com/definite-d/unda/blob/main/USERGUIDE.md).

This documentation is auto-generated from Markdown-syntax docstrings using pdoc3, so please pardon the huge docstring at
the beginning of the module's source code.

"""
__version__ = '1.1.0'

from collections import deque
from copy import copy, deepcopy
from typing import Dict, Optional

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


class UndaClient:
    """
    The `UndaClient` class.

    Arguably the most powerful part of Unda. Performs the duties of undo and redo on behalf of another object.

    ## Parameters

    ### _target:_
    The object itself.

    ### _style:_
    The `style` parameter specifies how this Client handles object state data.

    There are two different styles:

    * `DEEPCOPY` style: With this style, states are regarded as deepcopies of the target object.

    * `LOGGER` style: This style regards states as changes to the `__dict__` attribute of the target object.

    If left unspecified, Unda will resort to the best method for the current scenario.
    To specify a desired style and override Unda's judgement (not recommended), import the name of the style you want,
    e.g.:
    ```python
    from unda import LOGGER
    ```
    and pass it as the value of the `style` parameter.

    ### _auto_first_update:_
    If this is set to True, the Client will automatically update the undo dict once it's created, so there would be no
    need to call `update()` after creating the Client.

    ### _undo_stack:_
    If any deque is passed, it will be used as the undo stack for the Client. If none is passed (by default), a new
    deque will be created for that purpose.

    ### _redo_stack:_
    If any deque is passed, it will be used as the redo stack for the Client. If none is passed (by default), a new
    deque will be created for that purpose.

    ### _stack_height:_
    The maximum number of states to store in either stack. Defaults to 20.

    """

    def __init__(self,
                 target: object,
                 style: Optional[str] = None,
                 auto_first_update: bool = True,
                 undo_stack: Optional[deque] = None,
                 redo_stack: Optional[deque] = None,
                 stack_height: Optional[int] = None):
        self.target: object = target
        self.stack_height: Optional[int] = stack_height
        self.undo_stack: Optional[deque] = undo_stack
        self.redo_stack: Optional[deque] = redo_stack
        if self.stack_height is None:
            self.stack_height = STACK_HEIGHT
        if self.undo_stack is None:
            self.undo_stack = deque(maxlen=self.stack_height)
        if self.redo_stack is None:
            self.redo_stack = deque(maxlen=self.stack_height)
        self.style = style
        if self.style is None:
            if 'dict' in vars(self.target) and self.target.__sizeof__() > self.target.__dict__.__sizeof__():
                self.target_dict: Dict = self.__dict__.copy()
                self.style = LOGGER
            if 'dict' not in vars(self.target):
                self.style = DEEPCOPY
        # print(self.style, self.target.__dict__.__sizeof__(), self.target.__sizeof__())
        if auto_first_update:
            if self.style == DEEPCOPY:
                self.undo_stack.append(deepcopy(self.target))
                self.clear_redo_stack()
            if self.style == LOGGER:
                # If the stack is full, make the oldest change permanent in the target_dict.
                if len(self.undo_stack) == self.undo_stack.maxlen:
                    change = self.undo_stack.popleft()
                    self.target_dict.update(change)
                checklist_anomalies = extract_changes(self.compile_stack(), self.__dict__)
                self.undo_stack.append(checklist_anomalies)
                self.clear_redo_stack()
                del checklist_anomalies

    def entrust(self, key, manager) -> None:
        """
        Adds the client to the care of an `UndoManager` for easier batch use.

        ## Parameters
        ### _key:_
        A string used for referencing this Client directly from the `UndaManager`.

        ### _manager:_
        The `UndaManager` object to add this Client to.
        """
        manager.objects[key] = self
        return None

    def init_unda(self,
                  target: object,
                  style: Optional[str] = None,
                  auto_first_update: bool = False,
                  undo_stack: Optional[deque] = None,
                  redo_stack: Optional[deque] = None,
                  stack_height: Optional[int] = None, ) -> None:
        """
        Custom initialization function.

        ## Parameters
        Same as `UndaClient()`.
        """
        self.target: object = target
        self.stack_height: Optional[int] = stack_height
        self.undo_stack: Optional[deque] = undo_stack
        self.redo_stack: Optional[deque] = redo_stack
        if self.stack_height is None:
            self.stack_height = STACK_HEIGHT
        if self.undo_stack is None:
            self.undo_stack = deque(maxlen=self.stack_height)
        if self.redo_stack is None:
            self.redo_stack = deque(maxlen=self.stack_height)
        self.style = style
        if self.style is None:
            if 'dict' in vars(self.target) and self.target.__sizeof__() > self.target.__dict__.__sizeof__():
                self.target_dict: Dict = self.__dict__.copy()
                self.style = LOGGER
            if 'dict' not in vars(self.target):
                self.style = DEEPCOPY
        # print(self.style, self.target.__dict__.__sizeof__(), self.target.__sizeof__())
        if auto_first_update:
            if self.style == DEEPCOPY:
                self.undo_stack.append(deepcopy(self.target))
                self.clear_redo_stack()
            if self.style == LOGGER:
                # If the stack is full, make the oldest change permanent in the target_dict.
                if len(self.undo_stack) == self.undo_stack.maxlen:
                    change = self.undo_stack.popleft()
                    self.target_dict.update(change)
                checklist_anomalies = extract_changes(self.compile_stack(), self.__dict__)
                self.undo_stack.append(checklist_anomalies)
                self.clear_redo_stack()
                del checklist_anomalies
        return None

    def clear_undo_stack(self) -> None:
        """
        Clears the undo stack for this object.
        """
        self.undo_stack.clear()
        return None

    def clear_redo_stack(self) -> None:
        """
        Clears the redo stack for this object.
        """
        self.redo_stack.clear()
        return None

    def clear_stacks(self) -> None:
        """
        Clears both the undo and redo stacks for this object.
        """
        self.clear_undo_stack()
        self.clear_redo_stack()
        return None

    def compile_stack(self, depth: Optional[int] = None,
                      start_point: Optional[int] = None,
                      stack: Optional[deque] = None) -> Dict:
        """
        Useful only when using `LOGGER` style.

        Creates a version of the target dict that has all state changes in the specified stack applied.
        By default, the specified stack is the undo stack.

        ## Parameters
        ### _depth:_
        The number of changes to apply. Defaults to the total number of changes in the entire stack.

        ### _start_point:_
        The index of the first change to apply. Defaults to 0.

        ### _stack:_
        The stack of relevance.
        """
        if stack is None:
            del stack
            stack: deque = self.undo_stack
        if depth is None:
            del depth
            depth: int = len(stack)
        if start_point is None:
            del start_point
            start_point: int = 0
        changes_required = list(stack.copy())[start_point:depth]
        result = self.target_dict.copy()
        for name in RESERVED_NAMES:
            if name in result.keys():
                del result[name]
        for change in changes_required:
            if change is not None:
                result.update(change)
        return result

    def update(self) -> None:
        """
        Updates the relevant stack with current state data.
        By default, the "relevant stack" is the undo stack.
        """
        if self.style == DEEPCOPY:
            self.undo_stack.append(deepcopy(self.target))
            self.clear_redo_stack()

        if self.style == LOGGER:
            # If the stack is full, make the oldest change permanent in the target_dict.
            if len(self.undo_stack) == self.undo_stack.maxlen:
                change = self.undo_stack.popleft()
                self.target_dict.update(change)
            checklist_anomalies = extract_changes(self.compile_stack(), self.__dict__)
            self.undo_stack.append(checklist_anomalies)
            self.clear_redo_stack()
            del checklist_anomalies

    def undo(self, depth: int = 0, quiet: bool = False, inplace: bool = False) -> Optional[object]:
        """
        Saves current state to the redo stack, then returns a version of the target object with the latest state data
        in the undo stack applied.

        ## Parameters

        ### _depth:_
        The number of states to skip with a single undo call. By default, it's 0, and should work for most uses.

        ### _quiet:_
        Specifies if Unda should be quiet if undo is called but there's nothing to revert to. If False, an error will
        be returned if that happens.

        ### _inplace:_
        Useful only if the target object has a `__dict__` attribute.
        If set to True, the `__dict__` of the target will be replaced by the `__dict__` value of the result of the undo
        operation and returns False, thus there would be no need to re-assign the target object's variable to the
        result (which is what should be done if this parameter is False).
        """
        if not quiet and len(self.undo_stack) == 0:
            raise IndexError('There\'s nothing left to undo.')

        if self.style == DEEPCOPY:
            # Clear all states above the required one.
            self.undo_stack = deque(list(self.undo_stack)[0:len(self.undo_stack) - depth + 1], maxlen=self.stack_height)
            # Get the required state
            result = self.undo_stack.pop()
            # Save the state before the undo call to the redo stack.
            self.redo_stack.append(deepcopy(self.target))
            if inplace:
                self.target.__dict__.update(result.__dict__)
                return None
            return result

        if self.style == LOGGER:
            current_differences = extract_changes(self.compile_stack(), self.__dict__)
            self.redo_stack.append(current_differences)
            result = self.compile_stack()
            self.undo_stack = deque(
                list(self.undo_stack)[0:len(self.undo_stack) - depth - 1],
                maxlen=self.stack_height)
            if inplace:
                self.target.__dict__.update(result)
                return None
            result = copy(self.target)
            result.__dict__.update(result)
            return result

    def redo(self, depth: int = 0, quiet: bool = False, inplace: bool = False) -> Optional[object]:
        """
        Saves current state to the redo stack, then returns a version of the target object with the latest state data
        in the redo stack applied.

        ## Parameters

        ### _depth:_
        The number of states to skip with a single redo call. By default, it's 0, and should work for most uses.

        ### _quiet:_
        Specifies if Unda should be quiet if redo is called but there's nothing to revert to. If False, an error will
        be returned if that happens.

        ### _inplace:_
        Useful only if the target object has a `__dict__` attribute.
        If set to True, the `__dict__` of the target will be replaced by the `__dict__` value of the result of the redo
        operation and returns False, thus there would be no need to re-assign the target object's variable to the
        result (which is what should be done if this parameter is False).
        """
        if not quiet and len(self.redo_stack) == 0:
            raise IndexError('There\'s nothing left to redo.')

        if self.style == DEEPCOPY:
            # Clear all states above the required one.
            self.redo_stack = deque(list(self.redo_stack)[0:len(self.redo_stack) - depth + 1], maxlen=self.stack_height)
            # Get the required state
            result = self.redo_stack.pop()
            # Save the state before the redo call to the undo stack.
            self.undo_stack.append(deepcopy(self.target))
            if inplace:
                self.target.__dict__.update(result.__dict__)
                return None
            return result

        if self.style == LOGGER:
            current_differences = extract_changes(self.compile_stack(), self.__dict__)
            self.undo_stack.append(current_differences)
            result = self.compile_stack()
            self.redo_stack = deque(
                list(self.redo_stack)[0:len(self.redo_stack) - depth - 1],
                maxlen=self.stack_height)
            if inplace:
                self.target.__dict__.update(result)
                return None
            result = copy(self.target)
            result.__dict__.update(result)
            return result


class UndaObject:
    """
    A custom class which gives update, undo and redo abilities to any class that inherits from it by adding an
    UndaClient object to its attributes.

    The easiest way to use Unda in my opinion.

    To use,

    1. Inherit from this class when creating your desired class, (e.g. MyObject(UndaObject))

    2. At the END of the `__init()__` function (if it exists), call `self.init_fondue()`,

    3. At the BEGINNING of any method which may alter the attributes of the objects, call `self.update()`.

    That's it. Any method which step 3 affected can be undone by calling "self.undo()". Do note that if your custom
    class has no `__init__()`, there's no need to bother with step 1.

    ## Parameters
    Same as `UndaClient()` where they apply.
    """

    def __init__(self, style: Optional[str] = None, stack_height: Optional[int] = None):
        self.client = UndaClient(self, style=style, stack_height=stack_height)

    def init_fondue(self, style: Optional[str] = None, stack_height: Optional[int] = None):
        """
        Custom Initialization function. Comes in especially handy if your custom object already overrides
        `__init__()`.

        ## Parameters
        Same as `UndaClient()` where they apply.
        """
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
