from __future__ import absolute_import, division, print_function, unicode_literals 

import math

from .. import instructions_test as i_t

integer_tests = [
    # _integer_add
    [{'_integer' : [1, 2]}, '_integer_add', {'_integer' : [3]}],
    [{'_integer' : [0, 0]}, '_integer_add', {'_integer' : [0]}],
    [{'_integer' : [999999, -9]}, '_integer_add', {'_integer' : [999990]}],
    # _integer_sub
    [{'_integer' : [1, 2]}, '_integer_sub', {'_integer' : [-1]}],
    [{'_integer' : [0, 0]}, '_integer_sub', {'_integer' : [0]}],
    [{'_integer' : [999999, -9]}, '_integer_sub', {'_integer' : [1000008]}],
    # _integer_mult
    [{'_integer' : [2, 3]}, '_integer_mult', {'_integer' : [6]}],
    [{'_integer' : [10, 0]}, '_integer_mult', {'_integer' : [0]}],
    [{'_integer' : [7, -1]}, '_integer_mult', {'_integer' : [-7]}],
    # _integer_div
    [{'_integer' : [10, 3]}, '_integer_div', {'_integer' : [3]}],
    [{'_integer' : [10, 2]}, '_integer_div', {'_integer' : [5]}],
    [{'_integer' : [4, -2]}, '_integer_div', {'_integer' : [-2]}],
    [{'_integer' : [3, 0]}, '_integer_div', {'_integer' : [3, 0]}],
    # _integer_mod
    [{'_integer' : [10, 3]}, '_integer_mod', {'_integer' : [1]}],
    [{'_integer' : [10, 2]}, '_integer_mod', {'_integer' : [0]}],
    [{'_integer' : [4, -2]}, '_integer_mod', {'_integer' : [0]}],
    [{'_integer' : [3, 0]}, '_integer_mod', {'_integer' : [3, 0]}],
    # _integer_lt
    [{'_integer' : [10, 3]}, '_integer_lt', {'_boolean' : [False]}],
    [{'_integer' : [-3, 3]}, '_integer_lt', {'_boolean' : [True]}],
    [{'_integer' : [5, 5]}, '_integer_lt', {'_boolean' : [False]}],
    [{'_integer' : [4, -2]}, '_integer_lt', {'_boolean' : [False]}],
    [{'_integer' : [0, 0]}, '_integer_lt', {'_boolean' : [False]}],
    # _integer_lte
    [{'_integer' : [10, 3]}, '_integer_lte', {'_boolean' : [False]}],
    [{'_integer' : [-3, 3]}, '_integer_lte', {'_boolean' : [True]}],
    [{'_integer' : [3, -3]}, '_integer_lte', {'_boolean' : [False]}],
    [{'_integer' : [5, 5]}, '_integer_lte', {'_boolean' : [True]}],
    [{'_integer' : [4, -2]}, '_integer_lte', {'_boolean' : [False]}],
    [{'_integer' : [0, 0]}, '_integer_lte', {'_boolean' : [True]}],
    # _integer_gt
    [{'_integer' : [10, 3]}, '_integer_gt', {'_boolean' : [True]}],
    [{'_integer' : [-3, 3]}, '_integer_gt', {'_boolean' : [False]}],
    [{'_integer' : [5, 5]}, '_integer_gt', {'_boolean' : [False]}],
    [{'_integer' : [4, -2]}, '_integer_gt', {'_boolean' : [True]}],
    [{'_integer' : [0, 0]}, '_integer_gt', {'_boolean' : [False]}],
    # _integer_gte
    [{'_integer' : [10, 3]}, '_integer_gte', {'_boolean' : [True]}],
    [{'_integer' : [-3, 3]}, '_integer_gte', {'_boolean' : [False]}],
    [{'_integer' : [3, -3]}, '_integer_gte', {'_boolean' : [True]}],
    [{'_integer' : [5, 5]}, '_integer_gte', {'_boolean' : [True]}],
    [{'_integer' : [4, -2]}, '_integer_gte', {'_boolean' : [True]}],
    [{'_integer' : [0, 0]}, '_integer_gte', {'_boolean' : [True]}],
    # _integer_min
    [{'_integer' : [10, 3]}, '_integer_min', {'_integer' : [3]}],
    [{'_integer' : [-3, 3]}, '_integer_min', {'_integer' : [-3]}],
    [{'_integer' : [5, 5]}, '_integer_min', {'_integer' : [5]}],
    [{'_integer' : [0, -2]}, '_integer_min', {'_integer' : [-2]}],
    # _integer_max
    [{'_integer' : [10, 3]}, '_integer_max', {'_integer' : [10]}],
    [{'_integer' : [-3, 3]}, '_integer_max', {'_integer' : [3]}],
    [{'_integer' : [5, 5]}, '_integer_max', {'_integer' : [5]}],
    [{'_integer' : [0, -2]}, '_integer_max', {'_integer' : [0]}],
    # _integer_inc
    [{'_integer' : [10]}, '_integer_inc', {'_integer' : [11]}],
    [{'_integer' : [-3]}, '_integer_inc', {'_integer' : [-2]}],
    [{'_integer' : [0]}, '_integer_inc', {'_integer' : [1]}],
    # _integer_dec
    [{'_integer' : [10]}, '_integer_dec', {'_integer' : [9]}],
    [{'_integer' : [-3]}, '_integer_dec', {'_integer' : [-4]}],
    [{'_integer' : [0]}, '_integer_dec', {'_integer' : [-1]}],
    # _integer_from_float
    [{'_float' : [3.3]}, '_integer_from_float', {'_integer' : [3]}],
    [{'_float' : [-7.9]}, '_integer_from_float', {'_integer' : [-7]}],
    [{'_float' : [0.0]}, '_integer_from_float', {'_integer' : [0]}],
    # _integer_from_boolean
    [{'_boolean' : [False]}, '_integer_from_boolean', {'_integer' : [0]}],
    [{'_boolean' : [True]}, '_integer_from_boolean', {'_integer' : [1]}],
    # _integer_from_string
    [{'_string' : ['123']}, '_integer_from_string', {'_integer' : [123]}],
    [{'_string' : ['-2']}, '_integer_from_string', {'_integer' : [-2]}],
    [{'_string' : ['0']}, '_integer_from_string', {'_integer' : [0]}],
    [{'_string' : ['']}, '_integer_from_string', {'_string' : ['']}],
    [{'_string' : ['abc']}, '_integer_from_string', {'_string' : ['abc']}],
    ]

float_tests = [
    # _float_add
    [{'_float' : [1.7, 2.7]}, '_float_add', {'_float' : [4.4]}],
    [{'_float' : [0.0, 0.0]}, '_float_add', {'_float' : [0]}],
    [{'_float' : [999.999, -0.9]}, '_float_add', {'_float' : [999.099]}],
    # _float_sub
    [{'_float' : [1.7, 7.8]}, '_float_sub', {'_float' : [-6.1]}],
    [{'_float' : [0.0, 0.0]}, '_float_sub', {'_float' : [0.0]}],
    [{'_float' : [999.999, -0.9]}, '_float_sub', {'_float' : [1000.899]}],
    # _float_mult
    [{'_float' : [2.2, 3.7]}, '_float_mult', {'_float' : [8.14]}],
    [{'_float' : [10.0, 0.0]}, '_float_mult', {'_float' : [0.0]}],
    [{'_float' : [7.5, -1.1]}, '_float_mult', {'_float' : [-8.25]}],
    # _float_div
    [{'_float' : [10.0, 4.0]}, '_float_div', {'_float' : [2.5]}],
    [{'_float' : [4.2, -2.0]}, '_float_div', {'_float' : [-2.1]}],
    [{'_float' : [3.0, 0.0]}, '_float_div', {'_float' : [3.0, 0.0]}],
    # _float_mod
    [{'_float' : [10.31, 3.2]}, '_float_mod', {'_float' : [0.71]}],
    [{'_float' : [10.0, 2.0]}, '_float_mod', {'_float' : [0.0]}],
    [{'_float' : [4.5, -2.0]}, '_float_mod', {'_float' : [-1.5]}],
    [{'_float' : [3.0, 0.0]}, '_float_mod', {'_float' : [3.0, 0.0]}],
    # _float_lt
    [{'_float' : [10.1, 3.7]}, '_float_lt', {'_boolean' : [False]}],
    [{'_float' : [-3.0, 3.0]}, '_float_lt', {'_boolean' : [True]}],
    [{'_float' : [5.01, 5.01]}, '_float_lt', {'_boolean' : [False]}],
    [{'_float' : [4.2, -2.1]}, '_float_lt', {'_boolean' : [False]}],
    [{'_float' : [0.0, 0.0]},  '_float_lt', {'_boolean' : [False]}],
    # _float_lte
    [{'_float' : [10.1, 3.7]}, '_float_lte', {'_boolean' : [False]}],
    [{'_float' : [-3.0, 3.0]}, '_float_lte', {'_boolean' : [True]}],
    [{'_float' : [3.0, -3.0]}, '_float_lte', {'_boolean' : [False]}],
    [{'_float' : [5.01, 5.01]}, '_float_lte', {'_boolean' : [True]}],
    [{'_float' : [4.2, -2.1]}, '_float_lte', {'_boolean' : [False]}],
    [{'_float' : [0.0, 0.0]}, '_float_lte', {'_boolean' : [True]}],
    # _float_gt
    [{'_float' : [10.1, 3.7]}, '_float_gt', {'_boolean' : [True]}],
    [{'_float' : [-3.0, 3.0]}, '_float_gt', {'_boolean' : [False]}],
    [{'_float' : [5.01, 5.01]}, '_float_gt', {'_boolean' : [False]}],
    [{'_float' : [4.2, -2.1]}, '_float_gt', {'_boolean' : [True]}],
    [{'_float' : [0.0, 0.0]}, '_float_gt', {'_boolean' : [False]}],
    # _float_gte
    [{'_float' : [10.1, 3.7]}, '_float_gte', {'_boolean' : [True]}],
    [{'_float' : [-3.0, 3.0]}, '_float_gte', {'_boolean' : [False]}],
    [{'_float' : [3.0, -3.0]}, '_float_gte', {'_boolean' : [True]}],
    [{'_float' : [5.01, 5.01]}, '_float_gte', {'_boolean' : [True]}],
    [{'_float' : [4.2, -2.1]}, '_float_gte', {'_boolean' : [True]}],
    [{'_float' : [0.0, 0.0]}, '_float_gte', {'_boolean' : [True]}],
    # _float_min
    [{'_float' : [10.1, 3.7]}, '_float_min', {'_float' : [3.7]}],
    [{'_float' : [-3.0, 3.0]}, '_float_min', {'_float' : [-3.0]}],
    [{'_float' : [5.1, 5.11]}, '_float_min', {'_float' : [5.1]}],
    [{'_float' : [0.0, -2.99]}, '_float_min', {'_float' : [-2.99]}],
    # _float_max
    [{'_float' : [10.1, 3.7]}, '_float_max', {'_float' : [10.1]}],
    [{'_float' : [-3.0, 3.0]}, '_float_max', {'_float' : [3.0]}],
    [{'_float' : [5.0, 5.0]}, '_float_max', {'_float' : [5.0]}],
    [{'_float' : [5.1, 5.11]}, '_float_max', {'_float' : [5.11]}],
    [{'_float' : [0.0, -2.99]}, '_float_max', {'_float' : [0.0]}],
    # _float_inc
    [{'_float' : [10.0]}, '_float_inc', {'_float' : [11.0]}],
    [{'_float' : [-3.2]}, '_float_inc', {'_float' : [-2.2]}],
    [{'_float' : [0.0]}, '_float_inc', {'_float' : [1.0]}],
    # _float_dec
    [{'_float' : [10.0]}, '_float_dec', {'_float' : [9.0]}],
    [{'_float' : [-3.2]}, '_float_dec', {'_float' : [-4.2]}],
    [{'_float' : [0.0]}, '_float_dec', {'_float' : [-1.0]}],
    # _float_sin
    [{'_float' : [0.0]}, '_float_sin', {'_float' : [0.0]}],
    [{'_float' : [1.0]}, '_float_sin', {'_float' : [math.sin(1.0)]}],
    [{'_float' : [0.5]}, '_float_sin', {'_float' : [math.sin(0.5)]}],
    [{'_float' : [-0.5]}, '_float_sin', {'_float' : [math.sin(-0.5)]}],
    # _float_cos
    [{'_float' : [0.0]}, '_float_cos', {'_float' : [1.0]}],
    [{'_float' : [1.0]}, '_float_cos', {'_float' : [math.cos(1.0)]}],
    [{'_float' : [0.5]}, '_float_cos', {'_float' : [math.cos(0.5)]}],
    [{'_float' : [-0.5]}, '_float_cos', {'_float' : [math.cos(-0.5)]}],
    # _float_tan
    [{'_float' : [0.0]}, '_float_tan', {'_float' : [0.0]}],
    [{'_float' : [1.0]}, '_float_tan', {'_float' : [math.tan(1.0)]}],
    [{'_float' : [0.5]}, '_float_tan', {'_float' : [math.tan(0.5)]}],
    [{'_float' : [-0.5]}, '_float_tan', {'_float' : [math.tan(-0.5)]}],
    # _float_from_integer
    [{'_integer' : [3]}, '_float_from_integer', {'_float' : [3.0]}],
    [{'_integer' : [-7]}, '_float_from_integer', {'_float' : [-7.0]}],
    [{'_integer' : [0]}, '_float_from_integer', {'_float' : [0.0]}],
    # _float_from_boolean
    [{'_boolean' : [False]}, '_float_from_boolean', {'_float' : [0.0]}],
    [{'_boolean' : [True]}, '_float_from_boolean', {'_float' : [1.0]}],
    # _float_from_string
    [{'_string' : ['123']}, '_float_from_string', {'_float' : [123.0]}],
    [{'_string' : ['-2.3']}, '_float_from_string', {'_float' : [-2.3]}],
    [{'_string' : ['0']}, '_float_from_string', {'_float' : [0]}],
    [{'_string' : ['0.1']}, '_float_from_string', {'_float' : [0.1]}],
    [{'_string' : ['']}, '_float_from_string', {'_string' : ['']}],
    [{'_string' : ['abc']}, '_float_from_string', {'_string' : ['abc']}],
    ]

for t in integer_tests:
    passed = i_t.run_test(t)
    if not passed:
        raise Exception("The following test failed: " + str(t))
print("All integer instructions passed.")

for t in float_tests:
    passed = i_t.run_test(t)
    if not passed:
        raise Exception("The following test failed: " + str(t))
print("All float instructions passed.")