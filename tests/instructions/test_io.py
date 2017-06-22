from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import unittest
sys.path.insert(0, '..')
import testing_utilities as t_u

from pyshgp.exceptions import InvalidInputStackIndex
from pyshgp.push.instruction import (PyshInputInstruction,
                                     PyshClassVoteInstruction,
                                     PyshOutputInstruction)

inpt_valid = PyshInputInstruction(1)
inpt_too_big = PyshInputInstruction(7)
inpt_negative = PyshInputInstruction(-1)

vote_float = PyshClassVoteInstruction(1, '_float')
vote_int = PyshClassVoteInstruction(1, '_integer')
vote_too_big = PyshClassVoteInstruction(1, '_float')
vote_negative = PyshClassVoteInstruction(-1, '_float')
vote_bad_type_1 = PyshClassVoteInstruction(1, '_string')
vote_bad_type_2 = PyshClassVoteInstruction(1, 'abc')


class TestIOInstructions(unittest.TestCase):

    def test_inpt_valid(self):
        before = {'_input': ['A', 'B', 'C']}
        after = {'_input': ['A', 'B', 'C'], '_exec': ['B']}
        self.assertTrue(t_u.run_test(before, after, inpt_valid, True))

    def test_inpt_too_big(self):
        before = {'_input': ['A', 'B', 'C']}
        after = InvalidInputStackIndex
        self.assertTrue(t_u.run_test(before, after, inpt_too_big))

    def test_inpt_negative(self):
        before = {'_input': ['A', 'B', 'C']}
        after = InvalidInputStackIndex
        self.assertTrue(t_u.run_test(before, after, inpt_negative))

    def test_print_A(self):
        before = {'_integer': [7], '_output': {'stdout': ''}}
        after = {'_output': {'stdout': '7'}}
        self.assertTrue(t_u.run_test(before, after, '_print_integer'))

    def test_print_B(self):
        before = {'_float': [7.1]}
        after = {'_output': {'stdout': '7.1'}}
        self.assertTrue(t_u.run_test(before, after, '_print_float'))

    def test_print_newline_A(self):
        before = {'_output': {'stdout': 'A'}}
        after = {'_output': {'stdout': 'A\n'}}
        self.assertTrue(t_u.run_test(before, after, '_print_newline'))

    def test_print_newline_B(self):
        before = {'_output' : {}}
        after = {'_output': {'stdout': '\n'}}
        self.assertTrue(t_u.run_test(before, after, '_print_newline'))
