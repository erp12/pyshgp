from __future__ import absolute_import, division, print_function, unicode_literals

import sys, unittest
sys.path.insert(0, '..')
import testing_utilities as t_u

class TestCommonInstructions(unittest.TestCase):

    def test_pop(self):
        #1
        before = {'_integer' : [1, 2, 3]}
        after = {'_integer' : [1, 2]}
        self.assertTrue(t_u.run_test(before, after, '_integer_pop'))
        #2
        before = {'_boolean' : [True]}
        after = {'_boolean' : []}
        self.assertTrue(t_u.run_test(before, after, '_boolean_pop'))

    def test_dup(self):
        #1
        before = {'_string' : ['A']}
        after = {'_string' : ['A', 'A']}
        self.assertTrue(t_u.run_test(before, after, '_string_dup'))

    def test_swap(self):
        #1
        before = {'_float' : [1.5, 2.3]}
        after = {'_float' : [2.3, 1.5]}
        self.assertTrue(t_u.run_test(before, after, '_float_swap'))

    def test_rot(self):
        #1
        before = {'_integer' : [1, 2, 3]}
        after = {'_integer' : [2, 3, 1]}
        self.assertTrue(t_u.run_test(before, after, '_integer_rot'))

    def test_flush(self):
        #1
        before = {'_boolean' : [True, False]}
        after = {'_boolean' : []}
        self.assertTrue(t_u.run_test(before, after, '_boolean_flush'))

    def test_eq(self):
        #1
        before = {'_string' : ['A', 'B']}
        after = {'_boolean' : [False]}
        self.assertTrue(t_u.run_test(before, after, '_string_eq'))
        #2
        before = {'_float' : [1.23, 1.23]}
        after = {'_boolean' : [True]}
        self.assertTrue(t_u.run_test(before, after, '_float_eq'))

    def test_stack_depth(self):
        #1
        before = {'_integer' : [3, 2, 1]}
        after = {'_integer' : [3, 2, 1, 3]}
        self.assertTrue(t_u.run_test(before, after, '_integer_stack_depth'))

    def test_yank(self):
        #1
        before = {'_boolean' : [True, True, False], '_integer' : [1]}
        after = {'_boolean' : [True, False, True]}
        self.assertTrue(t_u.run_test(before, after, '_boolean_yank'))

    def test_yankduper(self):
        #1
        before = {'_string' : ['A', 'B', 'C'], '_integer' : [1]}
        after = {'_string' : ['A', 'B', 'C', 'B']}
        self.assertTrue(t_u.run_test(before, after, '_string_yankdup'))

    def test_shove(self):
        #1
        before = {'_float' : [1.1, 2.2, 3.3, 4.4], '_integer' : [2]}
        after = {'_float' : [1.1, 4.4, 2.2, 3.3]}
        self.assertTrue(t_u.run_test(before, after, '_float_shove'))

    def test_empty(self):
        #1
        before = {'_integer' : []}
        after = {'_boolean' : [True]}
        self.assertTrue(t_u.run_test(before, after, '_integer_empty'))
        #2
        before = {'_boolean' : [True]}
        after = {'_boolean' : [True, False]}
        self.assertTrue(t_u.run_test(before, after, '_boolean_empty'))
