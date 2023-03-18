URLS=[
"unda/index.html",
"unda/constants.html",
"unda/functions.html",
"unda/unda_client.html",
"unda/unda_manager.html",
"unda/unda_object.html",
"unda/version.html"
];
INDEX=[
{
"ref":"unda",
"url":0,
"doc":"[![Downloads](https: static.pepy.tech/badge/unda)](https: pepy.tech/project/unda) ![Monthly Downloads](https: img.shields.io/pypi/dm/unda.svg?style=flat) ![GitHub forks](https: img.shields.io/github/forks/definite-d/unda?logo=github&style=flat) ![PyPi Version](https: img.shields.io/pypi/v/unda?style=flat) ![Python Versions](https: img.shields.io/pypi/pyversions/unda.svg?style=flat&logo=python]) ![License](https: img.shields.io/pypi/l/unda.svg?style=flat&version=latest)   pip install unda    Introduction Welcome to Unda's Documentation! Contains technical details for the classes and functions. Not intended to be a [starter tutorial](https: github.com/definite-d/unda/blob/main/USERGUIDE.md). _This documentation is auto-generated from Markdown-syntax docstrings using pdoc3, so please pardon the huge docstring at the beginning of the module's source code._"
},
{
"ref":"unda.constants",
"url":1,
"doc":""
},
{
"ref":"unda.functions",
"url":2,
"doc":""
},
{
"ref":"unda.functions.extract_changes",
"url":2,
"doc":"Obtains and returns a dict of changes by comparing two dicts.  Parameters  _original:_ Dict to compare \"changed\" against.  _changed:_ Dict to be compared for differences.",
"func":1
},
{
"ref":"unda.unda_client",
"url":3,
"doc":""
},
{
"ref":"unda.unda_client.UndaClient",
"url":3,
"doc":"The  UndaClient class. Arguably the most powerful part of Unda. Performs the duties of undo and redo on behalf of another object.  Usage Create an UndaClient instance and pass your desired target object, e.g:   target = MyFantasticObject() my_client = UndaClient(target)    Parameters  _target:_ The object itself.  _style:_ The  style parameter specifies how this Client handles object state data. There are two different styles:   DEEPCOPY style: With this style, states are regarded as deep-copies of the target object.   LOGGER style: This style regards states as changes to the  __dict__ attribute of the target object. If left unspecified, Unda will resort to the best method for the current scenario. To specify a desired style and override Unda's judgement (not recommended), import the name of the style you want, e.g.:   from unda import LOGGER   and pass it as the value of the  style parameter.  _auto_first_update:_ If this is set to True, the Client will automatically update the undo dict once it's created, so there would be no need to call  update() after creating the Client.  _undo_stack:_ If any deque is passed, it will be used as the undo stack for the Client. If none is passed (by default), a new deque will be created for that purpose.  _redo_stack:_ If any deque is passed, it will be used as the redo stack for the Client. If none is passed (by default), a new deque will be created for that purpose.  _stack_height:_ The maximum number of states to store in either stack. Defaults to 30."
},
{
"ref":"unda.unda_client.UndaClient.entrust",
"url":3,
"doc":"Adds the client to the care of an  UndoManager for easier batch use.  Parameters  _key:_ A string used for referencing this Client directly from the  UndaManager .  _manager:_ The  UndaManager object to add this Client to.",
"func":1
},
{
"ref":"unda.unda_client.UndaClient.clear_undo_stack",
"url":3,
"doc":"Clears the undo stack for this object.",
"func":1
},
{
"ref":"unda.unda_client.UndaClient.clear_redo_stack",
"url":3,
"doc":"Clears the redo stack for this object.",
"func":1
},
{
"ref":"unda.unda_client.UndaClient.clear_stacks",
"url":3,
"doc":"Clears both the undo and redo stacks for this object.",
"func":1
},
{
"ref":"unda.unda_client.UndaClient.compile_stack",
"url":3,
"doc":"Useful only when using  LOGGER style. Creates a version of the target dict that has all state changes in the specified stack applied. By default, the specified stack is the undo stack.  Parameters  _depth:_ The number of changes to apply. Defaults to the total number of changes in the entire stack.  _start_point:_ The index of the first change to apply. Defaults to 0.  _stack:_ The stack of relevance.",
"func":1
},
{
"ref":"unda.unda_client.UndaClient.update",
"url":3,
"doc":"Updates the relevant stack with current state data. By default, the \"relevant stack\" is the undo stack.",
"func":1
},
{
"ref":"unda.unda_client.UndaClient.undo",
"url":3,
"doc":"Saves current state to the redo stack, then returns a version of the target object with the latest state data in the undo stack applied.  Parameters  _depth:_ The number of states to skip with a single undo call. By default, it's 0, and should work for most uses.  _quiet:_ Specifies if Unda should be quiet if undo is called but there's nothing to revert to. If False, an error will be returned if that happens.  _inplace:_ Useful only if the target object has a  __dict__ attribute. If set to True, the  __dict__ of the target will be replaced by the  __dict__ value of the result of the undo operation and returns False, thus there would be no need to re-assign the target object's variable to the result (which is what should be done if this parameter is False).",
"func":1
},
{
"ref":"unda.unda_client.UndaClient.redo",
"url":3,
"doc":"Saves current state to the redo stack, then returns a version of the target object with the latest state data in the redo stack applied.  Parameters  _depth:_ The number of states to skip with a single redo call. By default, it's 0, and should work for most uses.  _quiet:_ Specifies if Unda should be quiet if redo is called but there's nothing to revert to. If False, an error will be returned if that happens.  _inplace:_ Useful only if the target object has a  __dict__ attribute. If set to True, the  __dict__ of the target will be replaced by the  __dict__ value of the result of the redo operation and returns False, thus there would be no need to re-assign the target object's variable to the result (which is what should be done if this parameter is False).",
"func":1
},
{
"ref":"unda.unda_manager",
"url":4,
"doc":""
},
{
"ref":"unda.unda_manager.UndaManager",
"url":4,
"doc":" UndaManager class. Manages update, undo and redo operations for all objects in its care. Best for managing Undo and Redo functionality for multiple Python objects and existing UndaClients. When an object is added to an UndaManager, if it isn't an  UndaClient , a new  UndaClient is made for the object automatically and is added to the UndaManager in its stead. If it's already an  UndaClient , it gets added directly. _Essentially, the  UndaManager only manages  UndaClient s, not the objects themselves._  Usage  Adding Objects To add objects to its care, you can either:  pass a dict of  {key: object (or UndaClient)} pairs as the  starter_objects parameter,  Use  __setitem__ notation, e.g.:   manager = UndaManager() manager['item'] = MyItem()    or use the  add_object() or  add_objects() methods.  Accessing Clients  You are to use  __getitem__ notation, e.g.:  client = manager['key']  Undoing  Similar to other interfaces of Unda, remember to  update_all() or call the  update() method of an UndaClient before trying to undo.  Parameters  _starter_objects:_ A dict of objects/ UndaClient s/both to be entrusted to the UndaManager in the pattern:  {key: object (or UndaClient)}  _stack_height:_ An integer representing the maximum number of states to store in any stack created by this  UndaManager ."
},
{
"ref":"unda.unda_manager.UndaManager.starter_objects",
"url":4,
"doc":""
},
{
"ref":"unda.unda_manager.UndaManager.add_object",
"url":4,
"doc":"Entrusts an object into the UndaManager's care.  Parameters  _key:_ A key to reference the object. Could be anything, even the class name.  _target:_ The object itself.",
"func":1
},
{
"ref":"unda.unda_manager.UndaManager.add_objects",
"url":4,
"doc":"Adds multiple objects at once to the UndaManager.  Parameters  _dictionary_of_objects:_ A Python dict with access keys as the keys and your objects as values.",
"func":1
},
{
"ref":"unda.unda_manager.UndaManager.add_client",
"url":4,
"doc":"",
"func":1
},
{
"ref":"unda.unda_manager.UndaManager.update",
"url":4,
"doc":"Updates the UndaClient referenced by the specified key.  Parameters  _key_: The string used to reference a specific  UndaClient .",
"func":1
},
{
"ref":"unda.unda_manager.UndaManager.update_all",
"url":4,
"doc":"Same as \"update\", but applies it to all keys.",
"func":1
},
{
"ref":"unda.unda_manager.UndaManager.clear_all_stacks",
"url":4,
"doc":"Calls the \"clear_stacks\" function for all objects.",
"func":1
},
{
"ref":"unda.unda_manager.UndaManager.clear_undo_stacks",
"url":4,
"doc":"Calls the \"clear_undo_stack\" function for all objects.",
"func":1
},
{
"ref":"unda.unda_manager.UndaManager.clear_redo_stacks",
"url":4,
"doc":"Calls the \"clear_redo_stack\" function for all objects.",
"func":1
},
{
"ref":"unda.unda_manager.UndaManager.undo",
"url":4,
"doc":"Calls the  undo() function of the UndaClient referenced by the specified key.  Parameters  _key_: The string used to reference a specific  UndaClient . All other parameters are the same as  UndaClient.undo() where they apply.",
"func":1
},
{
"ref":"unda.unda_manager.UndaManager.undo_all",
"url":4,
"doc":"Same as undo, but applies to all objects in the UndaManager's care, and returns a dict in the format: {key: result}  Parameters Same as  UndaClient.undo() ",
"func":1
},
{
"ref":"unda.unda_manager.UndaManager.redo",
"url":4,
"doc":"Calls the  redo() function of the UndaClient referenced by the specified key.  Parameters  _key_: The string used to reference a specific  UndaClient . All other parameters are the same as  UndaClient.redo() where they apply.",
"func":1
},
{
"ref":"unda.unda_manager.UndaManager.redo_all",
"url":4,
"doc":"Same as redo, but applies to all objects in the UndaManager's care, and returns a dict in the format: {key: result}  Parameters Same as  UndaClient.redo() ",
"func":1
},
{
"ref":"unda.unda_object",
"url":5,
"doc":""
},
{
"ref":"unda.unda_object.UndaObject",
"url":5,
"doc":"A custom class which gives update, undo and redo abilities to any class that inherits from it by adding an UndaClient object to its attributes. The easiest way to use Unda in my opinion.  Usage 1. Inherit from this class when creating your desired class, (e.g. MyObject(UndaObject 2. At the END of the  __init()__ function, call  UndaObject.__init__(self) , 3. At the BEGINNING of any method which may alter the attributes of the objects, call  self.update() . That's it. Any method which step 3 affected can be undone by calling  self.undo() .  Dealing with Multiple Inheritance and  __init__() functions. If your custom object inherits from more than just  UndaObject :  it must have an  __init__() function with all the other parent classes'  __init__() functions (if they have such) being called (e.g.  OtherParent.__init__(self) ), and  Step 2 must apply;  UndaObject .__init__(self) must be the last line of your custom object's  __init__() function.  Parameters Same as  UndaClient() where they apply."
},
{
"ref":"unda.unda_object.UndaObject.update",
"url":5,
"doc":"Same as  UndaClient.update() .",
"func":1
},
{
"ref":"unda.unda_object.UndaObject.undo",
"url":5,
"doc":"Same as  UndaClient.undo() .",
"func":1
},
{
"ref":"unda.unda_object.UndaObject.redo",
"url":5,
"doc":"Same as  UndaClient.redo() .",
"func":1
},
{
"ref":"unda.version",
"url":6,
"doc":""
},
{
"ref":"unda.version.Version",
"url":6,
"doc":"Basic class built for versioning and version comparisons."
},
{
"ref":"unda.version.Version.parse",
"url":6,
"doc":"Constructs a Version object out of an appropriate version string (e.g. 'Version 1.3.2a').",
"func":1
},
{
"ref":"unda.version.Version.set_values",
"url":6,
"doc":"",
"func":1
},
{
"ref":"unda.version.Version.shift_major",
"url":6,
"doc":"Increases or decreases the value of the major part of the version by the specified value.",
"func":1
},
{
"ref":"unda.version.Version.shift_minor",
"url":6,
"doc":"Increases or decreases the value of the minor part of the version by the specified value.",
"func":1
},
{
"ref":"unda.version.Version.shift_patch",
"url":6,
"doc":"Increases or decreases the value of the patch part of the version by the specified value.",
"func":1
}
]