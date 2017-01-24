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
     {'_exec' : [[4, 4, ri.InstructionLookerUpper('_exec_do*range'), ri.get_instruction('_integer_inc')], ri.get_instruction('_integer_inc')], '_integer' : [3]}]

]  

for t in code_tests:
    passed = i_t.run_test(t, True)
    if not passed:
        raise Exception("The following test failed: " + str(t))
print("All code instructions passed.")