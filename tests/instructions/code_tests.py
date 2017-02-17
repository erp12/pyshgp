from __future__ import absolute_import, division, print_function, unicode_literals 

import math

from pyshgp import utils as u
from pyshgp.push.instructions import registered_instructions as ri


from .. import instructions_test as i_t

code_tests = [
    # _code_noop
    [{'_integer' : [1]}, '_code_noop', {'_integer' : [1]}],
    [{'_string' : ["HelloWorld"]}, '_code_noop', {'_string' : ["HelloWorld"]}],
    [{'_exec' : [7]}, '_code_noop', {'_exec' : [7]}],
    #_code_from_[type]
    [{'_integer' : [1]}, '_code_from_integer', {'_code' : [1]}],
    [{'_float' : [-2.3]}, '_code_from_float', {'_code' : [-2.3]}],
    [{'_boolean' : [True]}, '_code_from_boolean', {'_code' : [True]}],
    [{'_exec' : [7]}, '_code_from_exec', {'_code' : [7]}],
    # _code_append
    [{'_code' : [1, 2]}, '_code_append', {'_code' : [[2, 1]]}],
    [{'_code' : ["a", "b"]}, '_code_append', {'_code' : [["b", "a"]]}],
    # _code_atom
    [{'_code' : ["a"]}, '_code_atom', {'_boolean' : [True]}],
    [{'_code' : [["a", "b"]]}, '_code_atom', {'_boolean' : [False]}],
    [{'_code' : [[]]}, '_code_atom', {'_boolean' : [False]}],
    # _code_car
    [{'_code' : [[]]}, '_code_car', {'_code' : [[]]}],
    [{'_code' : ["a"]}, '_code_car', {'_code' : ["a"]}],
    [{'_code' : [["a"]]}, '_code_car', {'_code' : ["a"]}],
    [{'_code' : [["a", "b"]]}, '_code_car', {'_code' : ["a"]}],
    # _code_cdr
    [{'_code' : [[]]}, '_code_cdr', {'_code' : [[]]}],
    [{'_code' : ["a"]}, '_code_cdr', {'_code' : [[]]}],
    [{'_code' : [["a"]]}, '_code_cdr', {'_code' : [[]]}],
    [{'_code' : [["a", "b"]]}, '_code_cdr', {'_code' : [["b"]]}],
    # _code_cons
    [{'_code' : [[], []]}, '_code_cons', {'_code' : [[[]]]}],
    [{'_code' : [[], "c"]}, '_code_cons', {'_code' : [[[], 'c']]}],
    [{'_code' : [[], ["c"]]}, '_code_cons', {'_code' : [[[], 'c']]}],
    [{'_code' : [[], ["c", "d"]]}, '_code_cons', {'_code' : [[[], 'c', 'd']]}],
    [{'_code' : ["a", []]}, '_code_cons', {'_code' : [['a']]}],
    [{'_code' : ["a", "c"]}, '_code_cons', {'_code' : [['a', 'c']]}],
    [{'_code' : ["a", ["c"]]}, '_code_cons', {'_code' : [['a', 'c']]}],
    [{'_code' : ["a", ["c", "d"]]}, '_code_cons', {'_code' : [['a', 'c', 'd']]}],
    [{'_code' : [["a"], []]}, '_code_cons', {'_code' : [[["a"]]]}],
    [{'_code' : [["a"], "c"]}, '_code_cons', {'_code' : [[["a"], "c"]]}],
    [{'_code' : [["a"], ["c"]]}, '_code_cons', {'_code' : [[["a"], "c"]]}],
    [{'_code' : [["a"], ["c", "d"]]}, '_code_cons', {'_code' : [[["a"], "c", "d"]]}],
    [{'_code' : [["a", "b"], []]}, '_code_cons', {'_code' : [[["a", "b"]]]}],
    [{'_code' : [["a", "b"], "c"]}, '_code_cons', {'_code' : [[["a", "b"], "c"]]}],
    [{'_code' : [["a", "b"], ["c"]]}, '_code_cons', {'_code' : [[["a", "b"], "c"]]}],
    [{'_code' : [["a", "b"], ["c", "d"]]}, '_code_cons', {'_code' : [[["a", "b"], "c", "d"]]}],
    # _code_do
    [{'_code' : [7], '_exec' : []}, '_code_do', {'_exec' : [ri.InstructionLookerUpper('_code_pop'), 7], '_code' : [7]}],
    # _code_do_star
    [{'_code' : [7], '_exec' : []}, '_code_do*', {'_exec' : [7]}],
    # _code_do*range
    [{'_code' : [ri.get_instruction('_integer_inc')], '_integer' : [1, 2, 3]}, 
     '_code_do*range', 
     {'_exec' : [[3, 3, ri.InstructionLookerUpper('_code_from_exec'), ri.get_instruction('_integer_inc'), ri.InstructionLookerUpper('_code_do*range')], ri.get_instruction('_integer_inc')], '_integer' : [1, 2]}],
    # _exec_do*range
    [{'_exec' : [ri.get_instruction('_integer_inc')], '_integer' : [3, 4]}, 
     '_exec_do*range', 
     {'_exec' : [[4, 4, ri.InstructionLookerUpper('_exec_do*range'), ri.get_instruction('_integer_inc')], ri.get_instruction('_integer_inc')], '_integer' : [3]}],
    # _code_do*count
    [{'_integer' : [2], '_code' : [ri.get_instruction('_string_stack_depth')]}, 
     '_code_do*count', 
     {'_exec' : [[0, 1, ri.InstructionLookerUpper('_code_from_exec'), ri.get_instruction('_string_stack_depth'), ri.InstructionLookerUpper('_code_do*range')]]}],
    [{'_integer' : [2], '_code' : [ri.get_instruction('_integer_inc')]}, 
     '_code_do*count', 
     {'_exec' : [[0, 1, ri.InstructionLookerUpper('_code_from_exec'), ri.get_instruction('_integer_inc'), ri.InstructionLookerUpper('_code_do*range')]]}],
    # _exec_do*count
    [{'_integer' : [2], '_exec' : [ri.get_instruction('_string_stack_depth')]},
     '_exec_do*count',
     {'_exec' : [[0, 1, ri.InstructionLookerUpper('_exec_do*range'), ri.get_instruction('_string_stack_depth')]]}],
    [{'_integer' : [2], '_exec' : [ri.get_instruction('_integer_inc')]},
     '_exec_do*count',
     {'_exec' : [[0, 1, ri.InstructionLookerUpper('_exec_do*range'), ri.get_instruction('_integer_inc')]]}],
    # _code_do*times
    [{'_integer' : [2], '_code' : [ri.get_instruction('_string_stack_depth')]},
     '_code_do*times',
     {'_exec' : [[0, 1, ri.InstructionLookerUpper('_code_from_exec'), [ri.InstructionLookerUpper('_integer_pop'), ri.get_instruction('_string_stack_depth')], ri.InstructionLookerUpper('_code_do*range')]]}],
    [{'_integer' : [2], '_code' : [ri.get_instruction('_integer_inc')]},
     '_code_do*times',
     {'_exec' : [[0, 1, ri.InstructionLookerUpper('_code_from_exec'), [ri.InstructionLookerUpper('_integer_pop'), ri.get_instruction('_integer_inc')], ri.InstructionLookerUpper('_code_do*range')]]}],
    # _exec_do*times
    [{'_integer' : [2], '_exec' : [ri.get_instruction('_string_stack_depth')]},
     '_exec_do*times',
     {'_exec' : [[0, 1, ri.InstructionLookerUpper('_exec_do*range'), [ri.InstructionLookerUpper('_integer_pop'), ri.get_instruction('_string_stack_depth')]]]}],
    [{'_integer' : [2], '_exec' : [ri.get_instruction('_integer_inc')]},
     '_exec_do*times',
     {'_exec' : [[0, 1, ri.InstructionLookerUpper('_exec_do*range'), [ri.InstructionLookerUpper('_integer_pop'), ri.get_instruction('_integer_inc')]]]}],
    # _exec_while
    [{'_integer' : [5], '_boolean' : [True], '_exec' : [ri.get_instruction('_integer_inc')]},
     '_exec_while',
     {'_integer' : [5], '_exec' : [ri.get_instruction('_integer_inc'), ri.InstructionLookerUpper('_exec_while'), ri.get_instruction('_integer_inc')]}],
    [{'_integer' : [5], '_boolean' : [False], '_exec' : [ri.get_instruction('_integer_inc')]},
     '_exec_while',
     {'_integer' : [5]}],
    [{'_boolean' : [True], '_exec' : [ri.get_instruction('_string_stack_depth')]},
     '_exec_while',
     {'_exec' : [ri.get_instruction('_string_stack_depth'), ri.InstructionLookerUpper('_exec_while'), ri.get_instruction('_string_stack_depth')]}],
    [{'_boolean' : [False], '_exec' : [ri.get_instruction('_string_stack_depth')]},
     '_exec_while',
     {}],
    # _exec_do*while
    [{'_integer' : [5], '_boolean' : [True], '_exec' : [ri.get_instruction('_integer_inc')]},
     '_exec_do*while',
     {'_integer' : [5], '_boolean' : [True],  '_exec' : [ri.get_instruction('_integer_inc'), ri.InstructionLookerUpper('_exec_while'), ri.get_instruction('_integer_inc')]}],
    [{'_boolean' : [True], '_exec' : [ri.get_instruction('_string_stack_depth')]},
     '_exec_do*while',
     {'_boolean' : [True],'_exec' : [ri.get_instruction('_string_stack_depth'), ri.InstructionLookerUpper('_exec_while'), ri.get_instruction('_string_stack_depth')]}],
    [{'_integer' : [5], '_boolean' : [False], '_exec' : [ri.get_instruction('_integer_inc')]},
     '_exec_do*while',
     {'_integer' : [5], '_boolean' : [False],  '_exec' : [ri.get_instruction('_integer_inc'), ri.InstructionLookerUpper('_exec_while'), ri.get_instruction('_integer_inc')]}],
    [{'_boolean' : [False], '_exec' : [ri.get_instruction('_string_stack_depth')]},
     '_exec_do*while',
     {'_boolean' : [False],'_exec' : [ri.get_instruction('_string_stack_depth'), ri.InstructionLookerUpper('_exec_while'), ri.get_instruction('_string_stack_depth')]}],
    # _code_if
    [{'_boolean' : [True], '_code' : [ri.get_instruction('_string_stack_depth'), ri.get_instruction('_string_empty')]},
     '_code_if',
     {'_exec' : [ri.get_instruction('_string_stack_depth')]}],
    [{'_boolean' : [False], '_code' : [ri.get_instruction('_string_stack_depth'), ri.get_instruction('_string_empty')]},
     '_code_if',
     {'_exec' : [ri.get_instruction('_string_empty')]}],
    # _exec_if
    [{'_boolean' : [True], '_exec' : [ri.get_instruction('_string_stack_depth'), ri.get_instruction('_string_empty')]},
     '_exec_if',
     {'_exec' : [ri.get_instruction('_string_empty')]}],
    [{'_boolean' : [False], '_exec' : [ri.get_instruction('_string_stack_depth'), ri.get_instruction('_string_empty')]},
     '_exec_if',
     {'_exec' : [ri.get_instruction('_string_stack_depth')]}],
    # _exec_when
    [{'_boolean' : [True], '_exec' : [ri.get_instruction('_string_stack_depth')]},
     '_exec_when',
     {'_exec' : [ri.get_instruction('_string_stack_depth')]}],
    [{'_boolean' : [False], '_exec' : [ri.get_instruction('_string_stack_depth')]},
     '_exec_when',
     {}],
    [{'_boolean' : [True], '_exec' : [ri.get_instruction('_string_empty')]},
     '_exec_when',
     {'_exec' : [ri.get_instruction('_string_empty')]}],
    [{'_boolean' : [False], '_exec' : [ri.get_instruction('_string_empty')]},
     '_exec_when',
     {}],
    # _code_length
    [{'_code' : [7]}, '_code_length', {'_integer' : [1]}],
    [{'_code' : [[7]]}, '_code_length', {'_integer' : [1]}],
    [{'_code' : [[1, 2, 3]]}, '_code_length', {'_integer' : [3]}],
    # _code_list
    [{'_code' : [1, 2]}, '_code_list', {'_code' : [[1, 2]]}],
    [{'_code' : [1, [2]]}, '_code_list', {'_code' : [[1, [2]]]}],
    [{'_code' : [[1], [2]]}, '_code_list', {'_code' : [[[1], [2]]]}],
    # _code_wrap
    [{'_code' : [1]}, '_code_wrap', {'_code' : [[1]]}],
    [{'_code' : [[1]]}, '_code_wrap', {'_code' : [[[1]]]}],
    # _code_member
    [{'_code' : [1, []]}, '_code_member', {'_boolean' : [False]}],
    [{'_code' : [1, [1]]}, '_code_member', {'_boolean' : [True]}],
    [{'_code' : [1, [2]]}, '_code_member', {'_boolean' : [False]}],
    [{'_code' : [7, [1, 2]]}, '_code_member', {'_boolean' : [False]}],
    # _code_nth
    [{'_code' : [['a', 'b', 'c']], '_integer' : [1]}, '_code_nth', {'_code' : ['b']}],
    [{'_code' : [['a', 'b', 'c']], '_integer' : [4]}, '_code_nth', {'_code' : ['b']}],
    # _code_nthcdr
    [{'_code' : [['a', 'b', 'c']], '_integer' : [1]}, '_code_nthcdr', {'_code' : [['a', 'c']]}],
    [{'_code' : [['a', 'b', 'c']], '_integer' : [4]}, '_code_nthcdr', {'_code' : [['a', 'c']]}],
    [{'_code' : [['a']], '_integer' : [3]}, '_code_nthcdr', {'_code' : [[]]}],
]

for t in code_tests:
    passed = i_t.run_test(t)
    if not passed:
        raise Exception("The following test failed: " + str(t))
print("All code instructions passed.")






