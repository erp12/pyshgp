from __future__ import absolute_import, division, print_function, unicode_literals

import sys, unittest
sys.path.insert(0, '..')
import testing_utilities as t_u

from pyshgp.utils import Character

class TestCharInstructions(unittest.TestCase):

    def test_char_all_from_string(self):
        i = '_char_all_from_string'
        # 1
        before = {'_string' : ['abc']}
        after  = {'_char' : [Character('c'), Character('b'), Character('a')]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string' : ['a \n']}
        after  = {'_char' : [Character('\n'), Character(' '), Character('a')]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_string' : ['']}
        after  = {'_char' : []}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_char_from_integer(self):
        i = '_char_from_integer'
        # 1
        before = {'_integer' : [97]}
        after  = {'_char' : [Character('a')]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer' : [33]}
        after  = {'_char' : [Character('!')]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_integer' : [10]}
        after  = {'_char' : [Character('\n')]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_integer' : [32]}
        after  = {'_char' : [Character(' ')]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_char_from_float(self):
        i = '_char_from_float'
        # 1
        before = {'_float' : [97.1]}
        after  = {'_char' : [Character('a')]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_float' : [33.2]}
        after  = {'_char' : [Character('!')]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_float' : [10.3]}
        after  = {'_char' : [Character('\n')]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_float' : [32.9]}
        after  = {'_char' : [Character(' ')]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_char_is_letter(self):
        i = '_char_is_letter'
        # 1
        before = {'_char' : [Character('a')]}
        after  = {'_boolean' : [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_char' : [Character('7')]}
        after  = {'_boolean' : [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_char' : [Character('!')]}
        after  = {'_boolean' : [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_char' : [Character('\n')]}
        after  = {'_boolean' : [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 5
        before = {'_char' : [Character('\n')]}
        after  = {'_boolean' : [False]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_char_is_digit(self):
        i = '_char_is_digit'
        # 1
        before = {'_char' : [Character('a')]}
        after  = {'_boolean' : [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_char' : [Character('7')]}
        after  = {'_boolean' : [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_char' : [Character('!')]}
        after  = {'_boolean' : [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_char' : [Character('\n')]}
        after  = {'_boolean' : [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 5
        before = {'_char' : [Character('\n')]}
        after  = {'_boolean' : [False]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_char_is_white_space(self):
        i = '_char_is_white_space'
        # 1
        before = {'_char' : [Character('a')]}
        after  = {'_boolean' : [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_char' : [Character('7')]}
        after  = {'_boolean' : [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_char' : [Character('!')]}
        after  = {'_boolean' : [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_char' : [Character('\n')]}
        after  = {'_boolean' : [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 5
        before = {'_char' : [Character('\n')]}
        after  = {'_boolean' : [True]}
        self.assertTrue(t_u.run_test(before, after, i))
