from __future__ import absolute_import, division, print_function, unicode_literals 

import numpy as np

import unittest
import testing_utility as tu

import pyshgp.utils as u
import pyshgp.push.instruction as instr

class TestUtilMethods(unittest.TestCase):

    # Standard use case
    def test_flatten_all_A(self):
        self.assertEqual(u.flatten_all([1, 2, [3, [4]]]), [1, 2, 3, 4])

    # Where input is empty list
    def test_flatten_all_B(self):
        self.assertEqual(u.flatten_all([]), [])

    # is_str_type
    # is_int_type

    # Detect Input Instruction
    def test_recognize_pysh_type_PyshInputInstruction(self):
        i = instr.PyshInputInstruction(0)
        self.assertEqual(u.recognize_pysh_type(i), '_input_instruction')

    # Detect Class Vote Instruction
    def test_recognize_pysh_type_PyshClassVoteInstruction(self):
        i = instr.PyshClassVoteInstruction(1, '_integer')
        self.assertEqual(u.recognize_pysh_type(i), '_class_vote_instruction')

    # Detect int
    def test_recognize_pysh_type_int(self):
        for i in tu.random_test_ints(5):
            self.assertEqual(u.recognize_pysh_type(i), '_integer')

    # Detect float
    def test_recognize_pysh_type_float(self):
        for i in tu.random_test_floats(5):
            self.assertEqual(u.recognize_pysh_type(i), '_float')

    # Detect numpy float
    def test_recognize_pysh_type_float(self):
        for i in np.float32(1.1):
            self.assertEqual(u.recognize_pysh_type(i), '_float')

    # Detect string
    def test_recognize_pysh_type_string(self):
        for i in tu.random_test_strings(10):
            self.assertEqual(u.recognize_pysh_type(i), '_string')

    # Detect Character
    def test_recognize_pysh_type_character(self):
        for i in tu.random_test_characters(10):
            self.assertEqual(u.recognize_pysh_type(i), '_char')

    # Detect Booleans
    def test_recognize_pysh_type_bool(self):
        for i in tu.random_test_bools():
            self.assertEqual(u.recognize_pysh_type(i), '_boolean')

    # keep_number_reasonable
    # count_parens
    # count_points
    # reductions

    # Test 3 dicts
    def test_merge_dicts_stnrd(self):
        d1 = {"a" : 1, "b" : 2}
        d2 = {"c" : 3, "a" : 4}
        d3 = {"b" : 5}
        self.assertEqual(u.merge_dicts(d1, d2, d3),
                         {"a" : 4, "b" : 5, "c" : 3})

    # Test 1 dicts
    def test_merge_dicts_single(self):
        d = {"a" : 1, "b" : 2}
        self.assertEqual(u.merge_dicts(d), {"a" : 1, "b" : 2})

    # Test No arguments
    def test_merge_dicts_empty(self):
        self.assertEqual(u.merge_dicts(), {})

    # Test with non-dict argument

if __name__ == '__main__':
    unittest.main()