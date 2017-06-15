from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

import pyshgp.push.interpreter as interp

#TODO: WRITE _handle_?_instruction TESTS

class TestPushStateMethods(unittest.TestCase):

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
                  '_output': {},
                  '_string': [],
                  '_vector_boolean': [],
                  '_vector_float': [],
                  '_vector_integer': [],
                  '_vector_string': []}

    def test_len(self):
        self.assertEqual(len(self.i.state), 3)

    def test_from_dict(self):
        self.d['_integer'].append(5)
        self.i.state.from_dict(self.d)
        self.assertEqual(len(self.i.state), 4)
        self.assertEqual(self.i.state['_integer'].top_item(), 5)
        self.assertEqual(len(self.i.state['_integer']), 1)

#TODO: WRITE INTERPRETER TESTS
