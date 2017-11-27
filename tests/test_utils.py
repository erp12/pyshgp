import numpy as np
import unittest
import testing_utilities as tu
import pyshgp.utils as u
from pyshgp.push.instruction import InputInstruction


class TestUtilsMethods(unittest.TestCase):

    # Standard use case
    def test_flatten_all_A(self):
        self.assertEqual(u.flatten_all([1, 2, [3, [4]]]), [1, 2, 3, 4])

    # Where input is empty list
    def test_flatten_all_B(self):
        self.assertEqual(u.flatten_all([]), [])

    # is_str_type
    # is_int_type

    # Detect Input Instruction
    def test_recognize_pysh_type_InputInstruction(self):
        i = InputInstruction(0)
        self.assertEqual(u.recognize_pysh_type(i), '_instruction')

    # Detect int
    def test_recognize_pysh_type_int(self):
        for i in tu.random_test_ints(5):
            self.assertEqual(u.recognize_pysh_type(i), '_integer')

    # Detect float
    def test_recognize_pysh_type_float(self):
        for i in tu.random_test_floats(5):
            self.assertEqual(u.recognize_pysh_type(i), '_float')

    # Detect numpy float
    def test_recognize_pysh_type_float_np(self):
        self.assertEqual(u.recognize_pysh_type(np.float64(1.1)), '_float')

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
        d1 = {"a": 1, "b": 2}
        d2 = {"c": 3, "a": 4}
        d3 = {"b": 5}
        self.assertEqual(u.merge_dicts(d1, d2, d3),
                         {"a": 4, "b": 5, "c": 3})

    # Test 1 dicts
    def test_merge_dicts_single(self):
        d = {"a": 1, "b": 2}
        self.assertEqual(u.merge_dicts(d), {"a": 1, "b": 2})

    # Test No arguments
    def test_merge_dicts_empty(self):
        self.assertEqual(u.merge_dicts(), {})

    # Test with non-dict argument

    def test_levenshtein_distance_std(self):
        sed = u.levenshtein_distance('Hello', 'World')
        self.assertEqual(sed, 4)

    def test_levenshtein_distance_empty(self):
        sed = u.levenshtein_distance('Hello', '')
        self.assertEqual(sed, 5)

    def test_int_to_char_A(self):
        self.assertEqual(u.int_to_char(42), 'J')

    def test_int_to_char_B(self):
        self.assertEqual(u.int_to_char(-42), 'v')


if __name__ == '__main__':
    unittest.main()
