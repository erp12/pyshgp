import sys
import unittest
import testing_utilities as t_u

from pyshgp.utils import Character

sys.path.insert(0, '..')


class TestStringInstructions(unittest.TestCase):

    def test_string_from_integer(self):
        i = '_string_from_integer'
        # 1
        before = {'_integer': [7]}
        after = {'_string': ['7']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer': [-7]}
        after = {'_string': ['-7']}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_from_float(self):
        i = '_string_from_float'
        # 1
        before = {'_float': [7.0]}
        after = {'_string': ['7.0']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_float': [-7.123]}
        after = {'_string': ['-7.123']}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_from_boolean(self):
        i = '_string_from_boolean'
        # 1
        before = {'_boolean': [True]}
        after = {'_string': ['True']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_boolean': [False]}
        after = {'_string': ['False']}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_concat(self):
        i = '_string_concat'
        # 1
        before = {'_string': ['', '']}
        after = {'_string': ['']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string': ['A', '']}
        after = {'_string': ['A']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_string': ['', 'A']}
        after = {'_string': ['A']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_string': ['A', 'B']}
        after = {'_string': ['AB']}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_head(self):
        i = '_string_head'
        # 1
        before = {'_string': ['HelloWorld'], '_integer': [5]}
        after = {'_string': ['Hello']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string': [''], '_integer': [5]}
        after = {'_string': ['']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_string': ['HelloWorld'], '_integer': [-3]}
        after = {'_string': ['HelloWo']}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_tail(self):
        i = '_string_tail'
        # 1
        before = {'_string': ['HelloWorld'], '_integer': [5]}
        after = {'_string': ['World']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string': [''], '_integer': [5]}
        after = {'_string': ['']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_string': ['HelloWorld'], '_integer': [-3]}
        after = {'_string': ['loWorld']}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_split_at_index(self):
        i = '_string_split_at_index'
        # 1
        before = {'_string': ['HelloWorld'], '_integer': [5]}
        after = {'_string': ['Hello', 'World']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string': [''], '_integer': [5]}
        after = {'_string': ['', '']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_string': ['HelloWorld'], '_integer': [-3]}
        after = {'_string': ['HelloWo', 'rld']}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_split_at_str(self):
        i = '_string_split_at_str'
        # 1
        before = {'_string': ['', '']}
        after = {'_string': ['']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string': ['HelloWorld', '']}
        after = {'_string': ['HelloWorld']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_string': ['HelloWorld', 'o']}
        after = {'_string': ['Hell', 'W', 'rld']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_string': ['HelloWorld', 'a']}
        after = {'_string': ['HelloWorld']}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_split_at_char(self):
        i = '_string_split_at_char'
        # 1
        before = {'_string': [''], '_char': [Character('o')]}
        after = {'_string': ['']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string': ['HelloWorld'], '_char': [Character('o')]}
        after = {'_string': ['Hell', 'W', 'rld']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_string': ['HelloWorld'], '_char': [Character('a')]}
        after = {'_string': ['HelloWorld']}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_split_at_space(self):
        i = '_string_split_at_space'
        # 1
        before = {'_string': ['']}
        after = {'_string': ['']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string': ['HelloWorld']}
        after = {'_string': ['HelloWorld']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_string': ['Hello World']}
        after = {'_string': ['Hello', 'World']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_string': ['Just 3 Words']}
        after = {'_string': ['Just', '3', 'Words']}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_length(self):
        i = '_string_length'
        # 1
        before = {'_string': ['']}
        after = {'_integer': [0]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string': ['Hello']}
        after = {'_integer': [5]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_reverse(self):
        i = '_string_reverse'
        # 1
        before = {'_string': ['']}
        after = {'_string': ['']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string': ['Hello']}
        after = {'_string': ['olleH']}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_char_at(self):
        i = '_string_char_at'
        # 1
        before = {'_string': [''], '_integer': [2]}
        after = {'_string': [''], '_integer': [2]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string': ['Hello'], '_integer': [1]}
        after = {'_char': [Character('e')]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_empty_string(self):
        i = '_string_empty_string'
        # 1
        before = {'_string': ['']}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string': ['Hello']}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_contains(self):
        i = '_string_contains'
        # 1
        before = {'_string': ['', '']}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string': ['', 'A']}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_string': ['A', '']}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_string': ['A', 'A']}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 5
        before = {'_string': ['A', 'AB']}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 6
        before = {'_string': ['AB', 'A']}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_replace(self):
        i = '_string_replace'
        # 1
        before = {'_string': ['', '', '']}
        after = {'_string': ['']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string': ['', '', 'A']}
        after = {'_string': ['A']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_string': ['', 'A', '']}
        after = {'_string': ['']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_string': ['', 'A', 'A']}
        after = {'_string': ['']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 5
        before = {'_string': ['A', '', '']}
        after = {'_string': ['A']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 6
        before = {'_string': ['A', '', 'A']}
        after = {'_string': ['AAA']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 7
        before = {'_string': ['A', 'A', '']}
        after = {'_string': ['']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 8
        before = {'_string': ['A', 'A', 'A']}
        after = {'_string': ['A']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 9
        before = {'_string': ['', 'A', 'A']}
        after = {'_string': ['']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 10
        before = {'_string': ['AB', 'A', 'Z']}
        after = {'_string': ['ZB']}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_from_char(self):
        i = '_string_from_char'
        # 1
        before = {'_char': [Character('e')]}
        after = {'_string': ['e']}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_append_char(self):
        i = '_string_append_char'
        # 1
        before = {'_char': [Character('C')], '_string': ['']}
        after = {'_string': ['C']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_char': [Character('C')], '_string': ['AB']}
        after = {'_string': ['ABC']}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_first(self):
        i = '_string_first'
        # 1
        before = {'_string': ['']}
        after = {'_string': ['']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string': ['A']}
        after = {'_char': [Character('A')]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_string': ['AB']}
        after = {'_char': [Character('A')]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_last(self):
        i = '_string_last'
        # 1
        before = {'_string': ['']}
        after = {'_string': ['']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string': ['A']}
        after = {'_char': [Character('A')]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_string': ['AB']}
        after = {'_char': [Character('B')]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_nth(self):
        i = '_string_nth'
        # 1
        before = {'_string': [''], '_integer': [1]}
        after = {'_string': [''], '_integer': [1]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string': ['A'], '_integer': [1]}
        after = {'_char': [Character('A')]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_string': ['AB'], '_integer': [3]}
        after = {'_char': [Character('B')]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_replace_char(self):
        i = '_string_replace_char'
        # 1
        before = {'_string': [''], '_char': [Character('A'), Character('B')]}
        after = {'_string': ['']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string': ['A'], '_char': [Character('A'), Character('B')]}
        after = {'_string': ['B']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_string': ['B'], '_char': [Character('A'), Character('B')]}
        after = {'_string': ['B']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_string': ['AA'],
                  '_char': [Character('A'), Character('B')]}
        after = {'_string': ['BB']}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_replace_first_char(self):
        i = '_string_replace_first_char'
        # 1
        before = {'_string': [''], '_char': [Character('A'), Character('B')]}
        after = {'_string': ['']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string': ['A'], '_char': [Character('A'), Character('B')]}
        after = {'_string': ['B']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_string': ['B'], '_char': [Character('A'), Character('B')]}
        after = {'_string': ['B']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_string': ['AA'],
                  '_char': [Character('A'), Character('B')]}
        after = {'_string': ['BA']}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_string_remove_char(self):
        i = '_string_remove_char'
        # 1
        before = {'_string': [''], '_char': [Character('A')]}
        after = {'_string': ['']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_string': ['A'], '_char': [Character('A')]}
        after = {'_string': ['']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_string': ['B'], '_char': [Character('A')]}
        after = {'_string': ['B']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_string': ['AA'], '_char': [Character('A')]}
        after = {'_string': ['']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 5
        before = {'_string': ['AB'], '_char': [Character('A')]}
        after = {'_string': ['B']}
        self.assertTrue(t_u.run_test(before, after, i))
