import sys
import math
import unittest
import testing_utilities as t_u

from pyshgp.utils import Character

sys.path.insert(0, '..')


class TestIntegerInstructions(unittest.TestCase):

    def test_integer_add(self):
        i = '_integer_add'
        # 1
        before = {'_integer': [1, 2]}
        after = {'_integer': [3]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer': [0, 0]}
        after = {'_integer': [0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_integer': [999999, -9]}
        after = {'_integer': [999990]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_integer_sub(self):
        i = '_integer_sub'
        # 1
        before = {'_integer': [1, 2]}
        after = {'_integer': [-1]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer': [0, 0]}
        after = {'_integer': [0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_integer': [999999, -9]}
        after = {'_integer': [1000008]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_integer_mult(self):
        i = '_integer_mult'
        # 1
        before = {'_integer': [2, 3]}
        after = {'_integer': [6]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer': [10, 0]}
        after = {'_integer': [0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_integer': [7, -1]}
        after = {'_integer': [-7]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_integer_div(self):
        i = '_integer_div'
        # 1
        before = {'_integer': [10, 3]}
        after = {'_integer': [3]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer': [10, 2]}
        after = {'_integer': [5]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_integer': [4, -2]}
        after = {'_integer': [-2]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_integer': [3, 0]}
        after = {'_integer': [3, 0]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_integer_mod(self):
        i = '_integer_mod'
        # 1
        before = {'_integer': [10, 3]}
        after = {'_integer': [1]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer': [10, 2]}
        after = {'_integer': [0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_integer': [4, -2]}
        after = {'_integer': [0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_integer': [3, 0]}
        after = {'_integer': [3, 0]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_integer_lt(self):
        i = '_integer_lt'
        # 1
        before = {'_integer': [10, 3]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer': [-3, 3]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_integer': [5, 5]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_integer': [4, -2]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_integer_lte(self):
        i = '_integer_lte'
        # 1
        before = {'_integer': [10, 3]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer': [-3, 3]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_integer': [5, 5]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_integer': [4, -2]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_integer_gt(self):
        i = '_integer_gt'
        # 1
        before = {'_integer': [10, 3]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer': [-3, 3]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_integer': [5, 5]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_integer': [4, -2]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_integer_gte(self):
        i = '_integer_gte'
        # 1
        before = {'_integer': [10, 3]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer': [-3, 3]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_integer': [5, 5]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_integer': [4, -2]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_integer_min(self):
        i = '_integer_min'
        # 1
        before = {'_integer': [10, 3]}
        after = {'_integer': [3]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer': [-3, 3]}
        after = {'_integer': [-3]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_integer': [5, 5]}
        after = {'_integer': [5]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_integer': [4, -2]}
        after = {'_integer': [-2]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_integer_max(self):
        i = '_integer_max'
        # 1
        before = {'_integer': [10, 3]}
        after = {'_integer': [10]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer': [-3, 3]}
        after = {'_integer': [3]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_integer': [5, 5]}
        after = {'_integer': [5]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_integer': [4, -2]}
        after = {'_integer': [4]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_integer_inc(self):
        i = '_integer_inc'
        # 1
        before = {'_integer': [10]}
        after = {'_integer': [11]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer': [-3]}
        after = {'_integer': [-2]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_integer': [0]}
        after = {'_integer': [1]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_integer_dec(self):
        i = '_integer_dec'
        # 1
        before = {'_integer': [10]}
        after = {'_integer': [9]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer': [-3]}
        after = {'_integer': [-4]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_integer': [0]}
        after = {'_integer': [-1]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_integer_from_float(self):
        i = '_integer_from_float'
        # 1
        before = {'_float': [3.3]}
        after = {'_integer': [3]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_float': [-7.9]}
        after = {'_integer': [-7]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_float': [0.0]}
        after = {'_integer': [0]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_integer_from_boolean(self):
        i = '_integer_from_boolean'
        # 1
        before = {'_boolean': [False]}
        after = {'_integer': [0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_boolean': [True]}
        after = {'_integer': [1]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_integer_from_string(self):
        i = '_integer_from_string'
        # 1
        before = {'_string': ['123']}
        after = {'_integer': [123]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string': ['-2']}
        after = {'_integer': [-2]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_string': ['0']}
        after = {'_integer': [0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_string': ['']}
        after = {'_string': ['']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 5
        before = {'_string': ['abc']}
        after = {'_string': ['abc']}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_integer_from_char(self):
        i = '_integer_from_char'
        # 1
        before = {'_char': [Character('1')]}
        after = {'_integer': [49]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_char': [Character('0')]}
        after = {'_integer': [48]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_char': [Character(' ')]}
        after = {'_integer': [32]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_char': [Character('\n')]}
        after = {'_integer': [10]}
        self.assertTrue(t_u.run_test(before, after, i))


class TestFloatInstructions(unittest.TestCase):

    def test_float_add(self):
        i = '_float_add'
        # 1
        before = {'_float': [1.7, 2.7]}
        after = {'_float': [4.4]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_float': [0.0, 0.0]}
        after = {'_float': [0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_float': [999.999, -0.9]}
        after = {'_float': [999.099]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_float_sub(self):
        i = '_float_sub'
        # 1
        before = {'_float': [1.7, 7.8]}
        after = {'_float': [-6.1]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_float': [0.0, 0.0]}
        after = {'_float': [0.0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_float': [999.999, -0.9]}
        after = {'_float': [1000.899]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_float_mult(self):
        i = '_float_mult'
        # 1
        before = {'_float': [2.2, 3.7]}
        after = {'_float': [8.14]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_float': [10.0, 0.0]}
        after = {'_float': [0.0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_float': [7.5, -1.1]}
        after = {'_float': [-8.25]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_float_div(self):
        i = '_float_div'
        # 1
        before = {'_float': [10.0, 4.0]}
        after = {'_float': [2.5]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_float': [4.2, -2.0]}
        after = {'_float': [-2.1]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_float': [3.0, 0.0]}
        after = {'_float': [3.0, 0.0]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_float_mod(self):
        i = '_float_mod'
        # 1
        before = {'_float': [10.31, 3.2]}
        after = {'_float': [0.71]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_float': [10.0, 2.0]}
        after = {'_float': [0.0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_float': [4.5, -2.0]}
        after = {'_float': [-1.5]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_float': [3.0, 0.0]}
        after = {'_float': [3.0, 0.0]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_float_lt(self):
        i = '_float_lt'
        # 1
        before = {'_float': [10.1, 3.7]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_float': [-3.0, 3.0]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_float': [5.01, 5.01]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_float': [0.0, 0.0]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_float_lte(self):
        i = '_float_lte'
        # 1
        before = {'_float': [10.1, 3.7]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_float': [-3.0, 3.0]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_float': [5.01, 5.01]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_float': [0.0, 0.0]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_float_gt(self):
        i = '_float_gt'
        # 1
        before = {'_float': [10.1, 3.7]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_float': [-3.0, 3.0]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_float': [5.01, 5.01]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_float': [0.0, 0.0]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_float_gte(self):
        i = '_float_gte'
        # 1
        before = {'_float': [10.1, 3.7]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_float': [-3.0, 3.0]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_float': [5.01, 5.01]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_float': [0.0, 0.0]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_float_min(self):
        i = '_float_min'
        # 1
        before = {'_float': [10.1, 3.7]}
        after = {'_float': [3.7]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_float': [-3.0, 3.0]}
        after = {'_float': [-3.0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_float': [5.1, 5.11]}
        after = {'_float': [5.1]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_float': [0.0, -2.99]}
        after = {'_float': [-2.99]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_float_max(self):
        i = '_float_max'
        # 1
        before = {'_float': [10.1, 3.7]}
        after = {'_float': [10.1]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_float': [-3.0, 3.0]}
        after = {'_float': [3.0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_float': [5.1, 5.11]}
        after = {'_float': [5.11]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_float': [0.0, -2.99]}
        after = {'_float': [0.0]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_float_inc(self):
        i = '_float_inc'
        # 1
        before = {'_float': [10.0]}
        after = {'_float': [11.0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_float': [-3.2]}
        after = {'_float': [-2.2]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_float': [0.0]}
        after = {'_float': [1.0]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_float_dec(self):
        i = '_float_dec'
        # 1
        before = {'_float': [10.0]}
        after = {'_float': [9.0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_float': [-3.2]}
        after = {'_float': [-4.2]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_float': [0.0]}
        after = {'_float': [-1.0]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_float_sin(self):
        i = '_float_sin'
        # 1
        before = {'_float': [0.0]}
        after = {'_float': [0.0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_float': [1.0]}
        after = {'_float': [math.sin(1.0)]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_float': [0.5]}
        after = {'_float': [math.sin(0.5)]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_float': [-0.5]}
        after = {'_float': [math.sin(-0.5)]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_float_cos(self):
        i = '_float_cos'
        # 1
        before = {'_float': [0.0]}
        after = {'_float': [1.0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_float': [1.0]}
        after = {'_float': [math.cos(1.0)]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_float': [0.5]}
        after = {'_float': [math.cos(0.5)]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_float': [-0.5]}
        after = {'_float': [math.cos(-0.5)]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_float_tan(self):
        i = '_float_tan'
        # 1
        before = {'_float': [0.0]}
        after = {'_float': [0.0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_float': [1.0]}
        after = {'_float': [math.tan(1.0)]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_float': [0.5]}
        after = {'_float': [math.tan(0.5)]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_float': [-0.5]}
        after = {'_float': [math.tan(-0.5)]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_float_from_integer(self):
        i = '_float_from_integer'
        # 1
        before = {'_integer': [3]}
        after = {'_float': [3.0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer': [-7]}
        after = {'_float': [-7.0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_integer': [0]}
        after = {'_float': [0.0]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_float_from_boolean(self):
        i = '_float_from_boolean'
        # 1
        before = {'_boolean': [False]}
        after = {'_float': [0.0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_boolean': [True]}
        after = {'_float': [1.0]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_float_from_string(self):
        i = '_float_from_string'
        # 1
        before = {'_string': ['123']}
        after = {'_float': [123.0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string': ['-2.3']}
        after = {'_float': [-2.3]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_string': ['0.1']}
        after = {'_float': [0.1]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_string': ['']}
        after = {'_string': ['']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 5
        before = {'_string': ['abc']}
        after = {'_string': ['abc']}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_float_from_char(self):
        i = '_float_from_char'
        # 1
        before = {'_char': [Character('1')]}
        after = {'_float': [49.0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_char': [Character('0')]}
        after = {'_float': [48.0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_char': [Character(' ')]}
        after = {'_float': [32.0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_char': [Character('\n')]}
        after = {'_float': [10.0]}
        self.assertTrue(t_u.run_test(before, after, i))
