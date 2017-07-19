from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
import unittest
import testing_utilities as t_u
sys.path.insert(0, '..')


class TestBooleanInstructions(unittest.TestCase):

    def test_boolean_and(self):
        i = '_boolean_and'
        # 1
        before = {'_boolean': [False, False]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_boolean': [False, True]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_boolean': [True, False]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_boolean': [True, True]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_boolean_or(self):
        i = '_boolean_or'
        # 1
        before = {'_boolean': [False, False]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_boolean': [False, True]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_boolean': [True, False]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_boolean': [True, True]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_boolean_not(self):
        i = '_boolean_not'
        # 1
        before = {'_boolean': [False]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_boolean': [True]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_boolean_xor(self):
        i = '_boolean_xor'
        # 1
        before = {'_boolean': [False, False]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_boolean': [False, True]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_boolean': [True, False]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_boolean': [True, True]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_boolean_invert_first_then_and(self):
        i = '_boolean_invert_first_then_and'
        # 1
        before = {'_boolean': [False, False]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_boolean': [False, True]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_boolean': [True, False]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_boolean': [True, True]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_boolean_invert_second_then_and(self):
        i = '_boolean_invert_second_then_and'
        # 1
        before = {'_boolean': [False, False]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_boolean': [False, True]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_boolean': [True, False]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_boolean': [True, True]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_boolean_from_integer(self):
        i = '_boolean_from_integer'
        # 1
        before = {'_integer': [0]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer': [1]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_integer': [-1]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_boolean_from_float(self):
        i = '_boolean_from_float'
        # 1
        before = {'_float': [0.0]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_float': [1.1]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_float': [-1.9]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
