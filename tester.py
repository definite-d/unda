import unittest
import importlib
import sys
from os.path import abspath

from unda import UndaClient, UndaObject, UndaManager
from unda.version import Version

class Skateboard():

    def __init__(self, name):
        self.name = name
        self.moving = False
        UndaObject.__init__(self)

    def start_skating(self):
        self.moving = True

    def stop_skating(self):
        self.moving = False


# UndaObject Tests
class UndaObjectSkateboard(Skateboard, UndaObject):
    def __init__(self, name):
        Skateboard.__init__(self, name)
        UndaObject.__init__(self)

    def start_skating(self):
        self.update()
        Skateboard.start_skating(self)
        
    def stop_skating(self):
        self.update()
        Skateboard.stop_skating(self)


class TestUndaObject(unittest.TestCase):
    def setUp(self):
        self.board = UndaObjectSkateboard('Varial')

    def test_start_skating(self):
        self.board.start_skating()
        self.assertTrue(self.board.moving)

    def test_stop_skating(self):
        self.board.stop_skating()
        self.assertFalse(self.board.moving)

    def test_start_skating_then_undo(self):
        self.board.start_skating()
        self.board.undo(inplace=True)
        self.assertFalse(self.board.moving)
    
    def test_check_if_undo_stack_functions_properly(self):
        for n in range(3):
            self.board.start_skating()
            self.board.stop_skating()
        self.board.undo()
        self.assertTrue(self.board.moving)


# UndaClient Tests
class TestUndaClient(unittest.TestCase):
    def setUp(self):
        self.board = Skateboard('Hippie')
        self.client = UndaClient(self.board)

    def test_check_if_client_functions_properly(self):
        for n in range(3):
            self.client.update()
            self.board.start_skating()
            self.client.update()
            self.board.stop_skating()
        self.board = self.client.undo()
        self.assertTrue(self.board.moving)


# UndaManager Tests
class TestUndaManager(unittest.TestCase):
    def setUp(self):
        self.skateboard1 = Skateboard('Kickflip')
        self.skateboard2 = Skateboard('Ollie')
        self.skateboard3 = Skateboard('50:50')
        self.manager = UndaManager({1: self.skateboard1, 2:self.skateboard2})

    def test_managerial_skills(self):
        self.skateboard1.start_skating()
        self.manager.update(1)
        self.assertEqual(self.skateboard1, self.manager[1].target)
        self.manager.objects[3] = self.skateboard3
        self.assertTrue(isinstance(self.manager[3], UndaClient))

    def test_adding_new_client(self):
        skateboard = Skateboard('NoComply')
        client = UndaClient(self.skateboard1)
        self.manager.add_object('SkateboardClient', client)
        self.assertTrue('SkateboardClient' in self.manager.objects)


# Version Object Tests
class TestVersionObject(unittest.TestCase):
    def setUp(self):
        self.version_a = Version(2, 4, 9)
        self.version_b = Version('Version 1.1.239 Wheelie Edition')

    def test_correct_parsing(self):
        self.assertEqual(self.version_b.major, 1)
        self.assertEqual(self.version_b.minor, 1)
        self.assertEqual(self.version_b.patch, 239)
        self.assertEqual(self.version_b.additional_info, 'Wheelie Edition')

    def test_shifts(self):
        self.version_a.shift_major()
        self.version_a.shift_minor()
        self.version_a.shift_patch()
        self.assertEqual(self.version_a.major, 3)
        self.assertEqual(self.version_a.minor, 5)
        self.assertEqual(self.version_a.patch, 10)

    def test_comparisons(self):
        self.assertTrue(self.version_a > self.version_b)
        self.assertTrue(self.version_a >= self.version_b)
        self.assertFalse(self.version_a < self.version_b)
        self.assertFalse(self.version_a <= self.version_b)
        self.assertFalse(self.version_a == self.version_b)
    
    

if __name__ == '__main__':
    unittest.main()
