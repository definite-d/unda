from typing import Dict, Optional, Any

from .constants import STACK_HEIGHT
from .functions import _deprecated
from .unda_client import UndaClient


class _ObjectDict(dict):
    def __setitem__(self, _key: Any, _value: Any):
        if isinstance(_value, UndaClient):
            super().__setitem__(_key, _value)
        else:
            super().__setitem__(_key, UndaClient(_value))

class UndaManager:
    """
    `UndaManager` class. Manages update, undo and redo operations for all objects in its care.
    Best for managing Undo and Redo functionality for multiple Python objects and existing UndaClients.
    
    When an object is added to an UndaManager, if it isn't an `UndaClient`, a new `UndaClient` is made for the
    object automatically and is added to the UndaManager in its stead. If it's already an `UndaClient`, it
    gets added directly.
    
    _Essentially, the `UndaManager` only manages `UndaClient`s, not the objects themselves._
    
    ## Usage

    ### Adding Objects

    To add objects to its care, you can either:

    * pass a dict of `{key: object (or UndaClient)}` pairs as the `starter_objects` parameter,

    * Use `__setitem__` notation, e.g.:
    ```python
    manager = UndaManager()
    manager['item'] = MyItem()
    ```

    * or use the `add_object()` or `add_objects()` methods.

    ### Accessing Clients
    * You are to use `__getitem__` notation, e.g.: `client = manager['key']`

    ### Undoing

    * Similar to other interfaces of Unda, remember to `update_all()` or call the `update()` method of an UndaClient
    before trying to undo.


    ## Parameters
    ### _starter_objects:_
    A dict of objects/`UndaClient`s/both to be entrusted to the UndaManager in the pattern: 
    `{key: object (or UndaClient)}`

    ### _stack_height:_
    An integer representing the maximum number of states to store in any stack created by this `UndaManager`. 

    """
    starter_objects: Optional[Dict] = None

    def __init__(
            self,
            starter_objects: Optional[Dict] = None,
            stack_height: int = STACK_HEIGHT
    ) -> None:

        self.stack_height: int = stack_height
        self.starter_objects: Optional[Dict] = starter_objects
        self.objects: _ObjectDict = _ObjectDict()

        if self.starter_objects:
            self.add_objects(self.starter_objects)

    def __getitem__(self, key):
        return self.objects.get(key)

    def __setitem__(self, key, value):
        self.objects[key] = value

    def __delitem__(self, key):
        del self.objects[key]

    def add_object(self, key: str, target: object) -> None:
        """
        Entrusts an object into the UndaManager's care.

        ## Parameters
        ### _key:_
        A key to reference the object. Could be anything, even the class name.

        ### _target:_
        The object itself.
        """
        self[key] = target

    def add_objects(self, dictionary_of_objects):
        """
        Adds multiple objects at once to the UndaManager.

        ## Parameters
        ### _dictionary_of_objects:_
        A Python dict with access keys as the keys and your objects as values.
        """
        for key, value in dictionary_of_objects.items():
            self[key] = value

    @_deprecated(version='1.1.2', use_instead='add_object')
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
        self[key] = client

    def update(self, key):
        """
        Updates the UndaClient referenced by the specified key.

        ## Parameters

        ### _key_:
        The string used to reference a specific `UndaClient`.
        """
        self[key].update()
        

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
