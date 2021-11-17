"""
Unda Undo/Redo Algorithm Script
Provides state-based functionality behind undo and redo of Python objects.
"""
from collections import deque
from copy import copy, deepcopy
from typing import Dict, Optional

STACK_HEIGHT = 20


class UndaObject:
    """
    Contains a shallow copy of the object and the deque used as an undo stack.
    """
    def __init__(self,
                 target: object,
                 undo_stack: deque = deque(maxlen = STACK_HEIGHT),
                 redo_stack: deque = deque(maxlen = STACK_HEIGHT)):
        self.target: object = copy(target)
        self.undo_stack: deque = undo_stack
        self.redo_stack: deque = redo_stack

    def clear_undo_stack(self) -> None:
        """
        Clears the undo stack for this object.
        :return: None
        """
        self.undo_stack.clear()
        return None

    def clear_redo_stack(self) -> None:
        """
        Clears the redo stack for this object.
        :return: None
        """
        self.redo_stack.clear()
        return None

    def clear_stacks(self) -> None:
        """
        Clears both the undo and redo stacks for this object.
        :return: None
        """
        self.clear_undo_stack()
        self.clear_redo_stack()
        return None


class UndaManager:
    """
    UndaManager class. Manages undo and redo operations for all objects in its care.
    To use, pass a dict of {key: object} pairs in the "starter_objects" parameter or using add_object().

    Please do not attempt to add an object by using "UndaManager.objects[key] = target",
    as this will not work as intended. Always use the "add_object()" function instead.
    """
    starter_objects: Optional[Dict] = None

    def __init__(self, starter_objects: Optional[Dict] = None, stack_height: int = STACK_HEIGHT) -> None:
        self.stack_height: int = stack_height
        self.starter_objects: Optional[Dict] = starter_objects
        self.objects: Dict = {}
        if self.starter_objects is not None:
            self.objects.update({x: UndaObject(self.starter_objects[x]) for x in self.starter_objects})

    def add_object(self, key: str, target: object) -> None:
        """
        Entrusts an object into the UndaManager's care.
        Please do not attempt to add an object by using "UndaManager.objects[key] = target" (direct dictionary edits),
        as this will not work as intended. Always use this function instead.
        :param key: A key to reference the object. Could be anything, even the class name.
        :param target: The object itself.
        :return: None
        """
        self.objects[key] = UndaObject(target)
        
    def update(self, key) -> None:
        """
        Tells the Manager to add a deepcopied instance of an object to its deque using its key as reference.
        This is what you should call before a change happens with the object and you want it to be undo-able,
        i.e.: Call this when you need to save a state of the object to go back to when undo is called.
        :param key: The key tied to the object in the UndaManager's care.
        :return: None
        """
        self.objects[key].undo_stack.append(deepcopy(self.objects[key].target))
        self.objects[key].clear_redo_stack()

    def update_all(self) -> None:
        """
        Same as "update", but applies it to all keys.
        :return: None
        """
        for key in self.objects.keys():
            self.update(key)

    def clear_all_stacks(self) -> None:
        """
        Calls the "clear_stacks" function for all objects.
        :return: None
        """
        for key in self.objects.keys():
            self.objects[key].clear_stacks()

    def clear_undo_stacks(self) -> None:
        """
        Calls the "clear_undo_stack" function for all objects.
        :return: None
        """
        for key in self.objects.keys():
            self.objects[key].clear_undo_stack()

    def clear_redo_stacks(self) -> None:
        """
        Calls the "clear_redo_stack" function for all objects.
        :return: None
        """
        for key in self.objects.keys():
            self.objects[key].clear_redo_stack()

    def undo(self, key: str, depth: int = 1) -> object:
        """
        The star of the show.
        Returns (by default) the first object found in the undo deque.
        (i.e.: a deepcopy version of the object which was added prior to the current one).
        :param key: The key to the object.
        :param depth: The number of states to skip with a single undo call.
                        By default, it's 1, and should work for most uses.
        :return: The deepcopied object. You can use this to replace the original object that needs to be undone.
        """
        # Clear all states above the required one.
        self.objects[key].undo_stack = deque(
            list(self.objects[key].undo_stack)[0:len(self.objects[key].undo_stack) - depth],
            maxlen=self.stack_height)
        # Get the required state
        response = list(self.objects[key].undo_stack).pop()
        # Save the state before the undo call to the redo stack.
        self.objects[key].undo_stack.append(deepcopy(self.objects[key].target))
        return response

    def undo_all(self, depth: int = 1) -> Dict:
        """
        Same as undo, but applies to all objects in the UndaManager's care, and returns a dict in the format:
        {key: object}
        :param depth: The number of states to skip with a single undo call.
                        By default, it's 1, and should work for most uses.
        :return: A dict in the format: {key: deepcopied object)
        """
        return {key: self.undo(key, depth) for key in self.objects.keys()}

    def redo(self, key: str, depth: int = 1) -> object:
        """
        The complement of the undo function.
        Returns (by default) the first object found in the redo deque.
        (i.e.: a deepcopy version of the object which was added prior to the current one).
        :param key: The key to the object.
        :param depth: The number of states to skip with a single redo call.
                        By default, it's 1, and should work for most uses.
        :return: The deepcopied object. You can use this to replace the original object that needs to be redone.
        """
        # Clear all states above the required one.
        self.objects[key].undo_stack = deque(
            list(self.objects[key].undo_stack)[0:len(self.objects[key].undo_stack) - depth],
            maxlen=self.stack_height)
        # Get the required state
        response = self.objects[key].undo_stack.pop()
        # Save the state before the undo call to the redo stack.
        self.objects[key].undo_stack.append(deepcopy(self.objects[key].target))
        return response

    def redo_all(self, depth: int = 1) -> Dict:
        """
        Same as redo, but applies to all objects in the UndaManager's care, and returns a dict in the format:
        {key: object}
        :param depth: The number of states to skip with a single redo call.
                        By default, it's 1, and should work for most uses.
        :return: A dict in the format: {key: deepcopied object)
        """
        return {key: self.redo(key, depth) for key in self.objects.keys()}
