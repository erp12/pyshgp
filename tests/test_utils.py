from __future__ import absolute_import, division, print_function, unicode_literals 

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

if __name__ == '__main__':
    unittest.main()