from __future__ import absolute_import, division, print_function, unicode_literals 

import unittest
import testing_utility as tu

import pysh.utils as u

class TestUtilMethods(unittest.TestCase):

	# Standard use case
    def test_flatten_all_A(self):
        self.assertEqual(u.flatten_all([1, 2, [3, [4]]]), [1, 2, 3, 4])

    # Where input is empty list
    def test_flatten_all_B(self):
        self.assertEqual(u.flatten_all([]), [])

    # Detect int
    def test_recognize_pysh_type_int(self):
    	for i in tu.random_test_ints(5):
        	self.assertEqual(u.recognize_pysh_type(i), '_integer')

    # Detect float
    def test_recognize_pysh_type_int(self):
        for i in tu.random_test_ints(5):
            self.assertEqual(u.recognize_pysh_type(i), '_integer')

if __name__ == '__main__':
    unittest.main()