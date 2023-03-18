# Using unda
## Installation
First, install unda by the pip command (if you haven't already):
````
pip install --upgrade unda
````

## Basic Usage
unda currently provides three ways of handling undo/redo for your objects:

* Use an `UndaClient` object pointing to your custom object.
* Code your object to inherit from the `UndoObject` class.
* Use an `UndaManager` object and add your object to it.

The usage guides for each method below are very basic and aimed at beginners to Python, thus I recommend you always 
check the docstrings and [docs](https://definite-d.github.io/unda) of each method and class to understand the 
full capabilities of unda. 

### Using undaClient
The UndaClient manages the undo/redo functionality on behalf of your object. 

- Let's assume this is your custom class...:
````python
# Nothing fancy here, just an example. 
# Bonus points if you skate though.

class Skateboard:

    def __init__(self, name):
        self.name = name
        self.flipped = False
        
    def do_a_kickflip(self):
        self.flipped = True
        print('Board flipped successfully.')
```` 
- ...and you've got an instance of the class, like so:
````python
board = Skateboard('Varial')  # Just a skateboard named Varial.
````
- Import the undaClient object and create an instance for our board/object:
```python
from unda import undaClient
client = undaClient(board)
```
- Next, we **update** the Client. When using unda in general, "updating" simply 
means saving a state to the undo stack which we can go back to when we call undo().
So remember, always call `update()` when you need to be able to undo whatever happens next.
```python
client.update()
```
- Now that we've got our client all set up, we can go crazy on this object and make 
whatever changes we like to its attributes...:
```python
board.do_a_kickflip()
```
- As you can see, the `do_a_kickflip()` method is supposed to change the `flipped` attribute of our object.
The value of the `flipped` attribute should now be `True`. We can confirm using 
```python
print(board.flipped)  # This should print True currently.
```
- And if we need to undo, it's as easy as:
```python
board = client.undo()
``` 
- We can confirm if the action was actually undone using
```python
print(board.flipped)  # This will print False
```
- If we need to redo the action, we call the `redo()` function.
```python
board = client.redo()
print(board.flipped)  # This will print False
``` 


That's basically all you need to know to start using unda, but that is _far_ from all that it offers. 
Feel free to go through the [docs](https://definite-d.github.io/unda) to see more of what it's capable of.