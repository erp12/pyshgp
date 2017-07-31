import sys
import unittest
import testing_utilities as t_u
from pyshgp.push.instructions.jit import JustInTimeInstruction
from pyshgp.push.registered_instructions import get_instruction
sys.path.insert(0, '..')


class TestCodeInstructions(unittest.TestCase):

    def test_code_noop(self):
        i = '_code_noop'
        # 1
        before = {'_integer': [1]}
        self.assertTrue(t_u.run_test(before, before, i))
        # 2
        before = {'_string': ["HelloWorld"]}
        self.assertTrue(t_u.run_test(before, before, i))
        # 3
        before = {'_exec': [7]}
        self.assertTrue(t_u.run_test(before, before, i))

    def test_code_from(self):
        # 1
        before = {'_integer': [1]}
        after = {'_code': [1]}
        self.assertTrue(t_u.run_test(before, after, '_code_from_integer'))
        # 2
        before = {'_float': [-2.3]}
        after = {'_code': [-2.3]}
        self.assertTrue(t_u.run_test(before, after, '_code_from_float'))
        # 3
        before = {'_boolean': [True]}
        after = {'_code': [True]}
        self.assertTrue(t_u.run_test(before, after, '_code_from_boolean'))
        # 4
        before = {'_exec': [7]}
        after = {'_code': [7]}
        self.assertTrue(t_u.run_test(before, after, '_code_from_exec'))

    def test_code_append(self):
        i = '_code_append'
        # 1
        before = {'_code': [1, 2]}
        after = {'_code': [[2, 1]]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_code': ["a", "b"]}
        after = {'_code': [["b", "a"]]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_code_atom(self):
        i = '_code_atom'
        # 1
        before = {'_code': ["a"]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_code': [["a", "b"]]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_code': [[]]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_code_car(self):
        i = '_code_car'
        # 1
        before = {'_code': [[]]}
        after = {'_code': [[]]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_code': ["a"]}
        after = {'_code': ["a"]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_code': [["a"]]}
        after = {'_code': ["a"]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_code': [["a", "b"]]}
        after = {'_code': ["a"]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_code_cdr(self):
        i = '_code_cdr'
        # 1
        before = {'_code': [[]]}
        after = {'_code': [[]]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_code': ["a"]}
        after = {'_code': [[]]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_code': [["a"]]}
        after = {'_code': [[]]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_code': [["a", "b"]]}
        after = {'_code': [["b"]]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_code_cons(self):
        i = '_code_cons'
        # 1
        before = {'_code': [[], []]}
        after = {'_code': [[[]]]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_code': [[], "c"]}
        after = {'_code': [[[], 'c']]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_code': [[], ["c"]]}
        after = {'_code': [[[], 'c']]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_code': [[], ["c", "d"]]}
        after = {'_code': [[[], 'c', 'd']]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 5
        before = {'_code': ["a", []]}
        after = {'_code': [['a']]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 6
        before = {'_code': ["a", "c"]}
        after = {'_code': [['a', 'c']]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 7
        before = {'_code': ["a", ["c"]]}
        after = {'_code': [['a', 'c']]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 8
        before = {'_code': ["a", ["c", "d"]]}
        after = {'_code': [['a', 'c', 'd']]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 9
        before = {'_code': [["a"], []]}
        after = {'_code': [[["a"]]]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 10
        before = {'_code': [["a"], "c"]}
        after = {'_code': [[["a"], "c"]]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 11
        before = {'_code': [["a"], ["c"]]}
        after = {'_code': [[["a"], "c"]]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 12
        before = {'_code': [["a"], ["c", "d"]]}
        after = {'_code': [[["a"], "c", "d"]]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 13
        before = {'_code': [["a", "b"], []]}
        after = {'_code': [[["a", "b"]]]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 14
        before = {'_code': [["a", "b"], "c"]}
        after = {'_code': [[["a", "b"], "c"]]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 15
        before = {'_code': [["a", "b"], ["c"]]}
        after = {'_code': [[["a", "b"], "c"]]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 16
        before = {'_code': [["a", "b"], ["c", "d"]]}
        after = {'_code': [[["a", "b"], "c", "d"]]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_code_do(self):
        before = {'_code': [7], '_exec': []}
        after = {'_exec': [JustInTimeInstruction('_code_pop'), 7],
                 '_code': [7]}
        self.assertTrue(t_u.run_test(before, after, '_code_do'))

    def test_code_do_star(self):
        before = {'_code': [7], '_exec': []}
        after = {'_exec': [7]}
        self.assertTrue(t_u.run_test(before, after, '_code_do*'))

    def test_code_do_range(self):
        before = {'_code': [get_instruction('_integer_inc')],
                  '_integer': [1, 2, 3]}
        after = {'_exec': [[3, 3, JustInTimeInstruction('_code_from_exec'),
                            get_instruction('_integer_inc'),
                            JustInTimeInstruction('_code_do*range')],
                           get_instruction('_integer_inc')],
                 '_integer': [1, 2]}
        self.assertTrue(t_u.run_test(before, after, '_code_do*range'))

    def test_exec_do_range(self):
        before = {'_exec': [get_instruction('_integer_inc')],
                  '_integer': [3, 4]}
        after = {'_exec': [[4, 4, JustInTimeInstruction('_exec_do*range'),
                            get_instruction('_integer_inc')],
                           get_instruction('_integer_inc')],
                 '_integer': [3]}
        self.assertTrue(t_u.run_test(before, after, '_exec_do*range'))

    def test_code_do_count(self):
        i = '_code_do*count'
        # 1
        before = {'_integer': [2],
                  '_code': [get_instruction('_string_stack_depth')]}
        after = {'_exec': [[0, 1, JustInTimeInstruction('_code_from_exec'),
                            get_instruction('_string_stack_depth'),
                            JustInTimeInstruction('_code_do*range')]]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer': [2], '_code': [get_instruction('_integer_inc')]}
        after = {'_exec': [[0, 1, JustInTimeInstruction('_code_from_exec'),
                            get_instruction('_integer_inc'),
                            JustInTimeInstruction('_code_do*range')]]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_exec_do_count(self):
        i = '_exec_do*count'
        # 1
        before = {'_integer': [2],
                  '_exec': [get_instruction('_string_stack_depth')]}
        after = {'_exec': [[0, 1, JustInTimeInstruction('_exec_do*range'),
                            get_instruction('_string_stack_depth')]]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer': [2], '_exec': [get_instruction('_integer_inc')]}
        after = {'_exec': [[0, 1, JustInTimeInstruction('_exec_do*range'),
                            get_instruction('_integer_inc')]]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_code_do_times(self):
        i = '_code_do*times'
        # 1
        before = {'_integer': [2],
                  '_code': [get_instruction('_string_stack_depth')]}
        after = {'_exec': [[0, 1, JustInTimeInstruction('_code_from_exec'),
                            [JustInTimeInstruction('_integer_pop'),
                             get_instruction('_string_stack_depth')],
                            JustInTimeInstruction('_code_do*range')]]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer': [2], '_code': [get_instruction('_integer_inc')]}
        after = {'_exec': [[0, 1, JustInTimeInstruction('_code_from_exec'),
                            [JustInTimeInstruction('_integer_pop'),
                             get_instruction('_integer_inc')],
                            JustInTimeInstruction('_code_do*range')]]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_exec_do_times(self):
        i = '_exec_do*times'
        # 1
        before = {'_integer': [2],
                  '_exec': [get_instruction('_string_stack_depth')]}
        after = {'_exec': [[0, 1, JustInTimeInstruction('_exec_do*range'),
                            [JustInTimeInstruction('_integer_pop'),
                             get_instruction('_string_stack_depth')]]]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer': [2], '_exec': [get_instruction('_integer_inc')]}
        after = {'_exec': [[0, 1, JustInTimeInstruction('_exec_do*range'),
                            [JustInTimeInstruction('_integer_pop'),
                             get_instruction('_integer_inc')]]]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_exec_while(self):
        i = '_exec_while'
        # 1
        before = {'_integer': [5], '_boolean': [True],
                  '_exec': [get_instruction('_integer_inc')]}
        after = {'_integer': [5],
                 '_exec': [get_instruction('_integer_inc'),
                           JustInTimeInstruction('_exec_while'),
                           get_instruction('_integer_inc')]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_integer': [5], '_boolean': [False],
                  '_exec': [get_instruction('_integer_inc')]}
        after = {'_integer': [5]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_boolean': [True],
                  '_exec': [get_instruction('_string_stack_depth')]}
        after = {'_exec': [get_instruction('_string_stack_depth'),
                           JustInTimeInstruction('_exec_while'),
                           get_instruction('_string_stack_depth')]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_boolean': [False],
                  '_exec': [get_instruction('_string_stack_depth')]}
        after = {}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_code_if(self):
        i = '_code_if'
        # 1
        before = {'_boolean': [True],
                  '_code': [get_instruction('_string_stack_depth'),
                            get_instruction('_string_empty')]}
        after = {'_exec': [get_instruction('_string_stack_depth')]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_boolean': [False],
                  '_code': [get_instruction('_string_stack_depth'),
                            get_instruction('_string_empty')]}
        after = {'_exec': [get_instruction('_string_empty')]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_exec_if(self):
        i = '_exec_if'
        # 1
        before = {'_boolean': [True],
                  '_exec': [get_instruction('_string_stack_depth'),
                            get_instruction('_string_empty')]}
        after = {'_exec': [get_instruction('_string_empty')]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_boolean': [False],
                  '_exec': [get_instruction('_string_stack_depth'),
                            get_instruction('_string_empty')]}
        after = {'_exec': [get_instruction('_string_stack_depth')]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_exec_when(self):
        i = '_exec_when'
        # 1
        before = {'_boolean': [True],
                  '_exec': [get_instruction('_string_stack_depth')]}
        after = {'_exec': [get_instruction('_string_stack_depth')]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_boolean': [False],
                  '_exec': [get_instruction('_string_stack_depth')]}
        after = {}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_boolean': [True],
                  '_exec': [get_instruction('_string_empty')]}
        after = {'_exec': [get_instruction('_string_empty')]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_boolean': [False],
                  '_exec': [get_instruction('_string_empty')]}
        after = {}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_code_length(self):
        i = '_code_length'
        # 1
        before = {'_code': [7]}
        after = {'_integer': [1]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_code': [[7]]}
        after = {'_integer': [1]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_code': [[1, 2, 3]]}
        after = {'_integer': [3]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_code_list(self):
        i = '_code_list'
        # 1
        before = {'_code': [1, 2]}
        after = {'_code': [[1, 2]]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_code': [1, [2]]}
        after = {'_code': [[1, [2]]]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_code': [[1], [2]]}
        after = {'_code': [[[1], [2]]]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_code_wrap(self):
        i = '_code_wrap'
        # 1
        before = {'_code': [1]}
        after = {'_code': [[1]]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_code': [[1]]}
        after = {'_code': [[[1]]]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_code_member(self):
        i = '_code_member'
        # 1
        before = {'_code': [1, []]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_code': [1, [1]]}
        after = {'_boolean': [True]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_code': [1, [2]]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 4
        before = {'_code': [7, [1, 2]]}
        after = {'_boolean': [False]}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_code_nth(self):
        i = '_code_nth'
        # 1
        before = {'_code': [['a', 'b', 'c']], '_integer': [1]}
        after = {'_code': ['b']}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_code': [['a', 'b', 'c']], '_integer': [4]}
        after = {'_code': ['b']}
        self.assertTrue(t_u.run_test(before, after, i))

    def test_code_nthcdr(self):
        i = '_code_nthcdr'
        # 1
        before = {'_code': [['a', 'b', 'c']], '_integer': [1]}
        after = {'_code': [['a', 'c']]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 2
        before = {'_code': [['a', 'b', 'c']], '_integer': [4]}
        after = {'_code': [['a', 'c']]}
        self.assertTrue(t_u.run_test(before, after, i))
        # 3
        before = {'_code': [['a']], '_integer': [3]}
        after = {'_code': [[]]}
        self.assertTrue(t_u.run_test(before, after, i))
