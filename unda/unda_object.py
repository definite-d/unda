from typing import Optional

from .unda_client import UndaClient


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

    * Step 2 must apply; `UndaObject``.__init__(self)` must be the last line of your custom object's `__init__()`
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

