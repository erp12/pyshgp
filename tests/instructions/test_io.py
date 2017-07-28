import sys
import unittest
import testing_utilities as t_u
sys.path.insert(0, '..')


class TestIOInstructions(unittest.TestCase):

    def test_print_A(self):
        before = {'_integer': [7]}
        after = {'_stdout': '7'}
        self.assertTrue(t_u.run_test(before, after, '_print_integer'))

    def test_print_B(self):
        before = {'_float': [7.1]}
        after = {'_stdout': '7.1'}
        self.assertTrue(t_u.run_test(before, after, '_print_float'))

    def test_print_newline_A(self):
        before = {'_stdout': 'A'}
        after = {'_stdout': 'A\n'}
        self.assertTrue(t_u.run_test(before, after, '_print_newline'))

    def test_print_newline_B(self):
        before = {}
        after = {'_stdout': '\n'}
        self.assertTrue(t_u.run_test(before, after, '_print_newline'))
