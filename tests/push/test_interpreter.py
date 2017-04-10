from __future__ import absolute_import, division, print_function, unicode_literals 

import unittest

import pyshgp.utils as u
import pyshgp.push.interpreter as interp

class TestStackMethods(unittest.TestCase):

    def setUp(self):
        self.i = interp.PushInterpreter(inputs=["a", "b", "c"])
        self.d = {'_auxiliary': [],
                  '_boolean': [],
                  '_char': [],
                  '_code': [],
                  '_exec': [],
                  '_float': [],
                  '_input': ['a', 'b', 'c'],
                  '_integer': [],
                  '_output': [''],
                  '_string': [],
                  '_vector_boolean': [],
                  '_vector_float': [],
                  '_vector_integer': [],
                  '_vector_string': []}

    def test_reset_state(self):
        self.i.reset_state()
        self.assertEqual(self.i.state_size(), 0)

    def test_state_size(self):
        self.assertEqual(self.i.state_size(), 3)

    def test_state_as_dict(self):
        self.assertEqual(self.i.state_as_dict(), self.d)

    def test_from_dict(self):
        self.d['_integer'].append(5)
        self.i.state_from_dict(self.d)
        #print(self.i.state_as_dict())
        self.assertEqual(self.i.state_size(), 4)
        self.assertEqual(self.i.state['_integer'].top_item(), 5)
        self.assertEqual(len(self.i.state['_integer']), 1)



