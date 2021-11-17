# Using Unda
## Installation
First, install Unda by the pip command (if you haven't already):
````
pip install unda
````

## Actual Usage (Super Easy Guide)
### Prepare an object
First, you've got to have an object which you want the undo/redo 
functionality for. 
For demonstration purposes, let's use this simple one:
````python
# Just an example object class here, you can use any object at all.
class SomeClass:
    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar

x = SomeClass('a string', 'another_string')
y = SomeClass('some string', 'some_other_string')
````
### Import Unda
Next, import the module like so:
````python
from unda import UndaManager
````
The UndaManager is bascally the only interface you need for normal use.
Next, you'll need to add objects to it.

### Place your object in Unda's care
There's two ways for adding an object to an UndaManager:
#### Way 1 (Single):
You can first create an UndaManager, and then add the object.
````python
manager = UndaManager()
manager.add_object(key='object X', target=x)
````
The `key` can be literally any string. It's purpose is for referencing.
The `target` should be the object you want to add. In our example here, that's `x`.

#### Way 2 (Bulk):
If you've got more than one object, you can add them all at once.
First put them all in a `dict`, then pass it as a parameter when creating 
the UndaManager:
````python
some_objects = {'object X': x, 'object Y': y}
manager = UndaManager(some_objects)
````

### Using the Undo and Redo functionality
Using `x` as a test subject here:
````python
UndaManager.update('object X')
x.foo = 'The foo has changed!'
print(x.foo)
x = UndaManager.undo('object X')
print(x.foo)
x = UndaManager.redo('object X')
print(x.foo)
````
Running that gives this result...:
````text
The foo has changed!
a string
The foo has changed!
````
...as expected.

That's basically it.

### Full example code (using Way 2 to add objects):
````python
# Just an example object class here, you can use any object at all.
class SomeClass:
    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar

x = SomeClass('a string', 'another_string')
y = SomeClass('some string', 'some_other_string')

from unda import UndaManager

some_objects = {'object X': x, 'object Y': y}
manager = UndaManager(some_objects)

UndaManager.update('object X')
x.foo = 'The foo has changed!'
print(x.foo)
x = UndaManager.undo('object X')
print(x.foo)
x = UndaManager.redo('object X')
print(x.foo)
````
