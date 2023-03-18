from collections import deque
from copy import copy, deepcopy
from typing import Dict, Optional

from .constants import DEEPCOPY, LOGGER, RESERVED_NAMES, STACK_HEIGHT
from .functions import extract_changes


class UndaClient:
    """
    The `UndaClient` class.
    Arguably the most powerful part of Unda. Performs the duties of undo and redo on behalf of another object.
    ## Usage
    Create an UndaClient instance and pass your desired target object, e.g:
    ```python
    target = MyFantasticObject()
    my_client = UndaClient(target)
    ```
    ## Parameters
    ### _target:_
    The object itself.
    ### _style:_
    The `style` parameter specifies how this Client handles object state data.
    There are two different styles:
    * `DEEPCOPY` style: With this style, states are regarded as deep-copies of the target object.
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
    The maximum number of states to store in either stack. Defaults to 30.
    """

    def __init__(
            self,
            target: object,
            style: Optional[str] = None,
            auto_first_update: bool = True,
            undo_stack: Optional[deque] = None,
            redo_stack: Optional[deque] = None,
            stack_height: Optional[int] = None
    ):

        self.target = target
        self.style = style
        self.stack_height = stack_height
        self.undo_stack = undo_stack
        self.redo_stack = redo_stack
        self._target_dict: Optional[Dict] = None

        self._init_stack_height()
        self._init_undo_stack()
        self._init_redo_stack()
        self._init_style()

        if auto_first_update:
            self._auto_first_update()

    def _init_stack_height(self):
        if self.stack_height is None:
            self.stack_height = STACK_HEIGHT

    def _init_undo_stack(self):
        if self.undo_stack is None:
            self.undo_stack = deque(maxlen=self.stack_height)

    def _init_redo_stack(self):
        if self.redo_stack is None:
            self.redo_stack = deque(maxlen=self.stack_height)

    def _init_style(self):
        if self.style is None:
            if 'dict' in vars(self.target) and self.target.__sizeof__() > self.target.__dict__.__sizeof__():
                self._target_dict = self.__dict__.copy()
                self.style = LOGGER
            elif 'dict' not in vars(self.target):
                self.style = DEEPCOPY

    def _auto_first_update(self):
        if self.style == DEEPCOPY:
            self.undo_stack.append(deepcopy(self.target))
            self.clear_redo_stack()
        elif self.style == LOGGER:
            if len(self.undo_stack) == self.undo_stack.maxlen:
                change = self.undo_stack.popleft()
                self._target_dict.update(change)
            checklist_anomalies = extract_changes(
                self.compile_stack(), self.__dict__)
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
        manager[key] = self

    def clear_undo_stack(self) -> None:
        """
        Clears the undo stack for this object.
        """
        self.undo_stack.clear()

    def clear_redo_stack(self) -> None:
        """
        Clears the redo stack for this object.
        """
        self.redo_stack.clear()

    def clear_stacks(self) -> None:
        """
        Clears both the undo and redo stacks for this object.
        """
        self.clear_undo_stack()
        self.clear_redo_stack()

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
        result = self._target_dict.copy()
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
                self._target_dict.update(change)
            checklist_anomalies = extract_changes(
                self.compile_stack(), self.__dict__)
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
            self.undo_stack = deque(list(self.undo_stack)[0:len(
                self.undo_stack) - depth + 1], maxlen=self.stack_height)
            # Get the required state
            result = self.undo_stack.pop()
            # Save the state before the undo call to the redo stack.
            self.redo_stack.append(deepcopy(self.target))
            if inplace:
                self.target.__dict__.update(result.__dict__)
                return None
            return result

        if self.style == LOGGER:
            print('Using LOGGER')
            current_differences = extract_changes(
                self.compile_stack(), self.__dict__)
            self.redo_stack.append(current_differences)
            result = self.compile_stack()
            self.undo_stack = deque(
                list(self.undo_stack)[0:len(self.undo_stack) - depth - 1],
                maxlen=self.stack_height)
            if inplace:
                self.target.__dict__.update(result)
                return None
            _result = result
            result = copy(self.target)
            result.__dict__.update(_result)
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
            self.redo_stack = deque(list(self.redo_stack)[0:len(
                self.redo_stack) - depth + 1], maxlen=self.stack_height)
            # Get the required state
            result = self.redo_stack.pop()
            # Save the state before the redo call to the undo stack.
            self.undo_stack.append(deepcopy(self.target))
            if inplace:
                self.target.__dict__.update(result.__dict__)
                return None
            return result

        if self.style == LOGGER:
            current_differences = extract_changes(
                self.compile_stack(), self.__dict__)
            self.undo_stack.append(current_differences)
            result = self.compile_stack()
            self.redo_stack = deque(
                list(self.redo_stack)[0:len(self.redo_stack) - depth - 1],
                maxlen=self.stack_height)
            if inplace:
                self.target.__dict__.update(result)
                return None
            _result = result
            result = copy(self.target)
            result.__dict__.update(_result)
            return result
