from __future__ import absolute_import, division, print_function, unicode_literals 

from pyshgp import utils as u

from .. import instructions_test as i_t

common_tests = [
	# _pop
	[{'_integer' : [1, 2, 3]}, '_integer_pop', {'_integer' : [1, 2]}],
	[{'_boolean' : [True]}, '_boolean_pop', {'_boolean' : []}],
	# _dup
	[{'_string' : ['A']}, '_string_dup', {'_string' : ['A', 'A']}],
	# _swap
	[{'_float' : [1.5, 2.3]}, '_float_swap', {'_float' : [2.3, 1.5]}],
	# _rot
	[{'_integer' : [1, 2, 3]}, '_integer_rot', {'_integer' : [2, 3, 1]}],
	# _flush
	[{'_boolean' : [True, False]}, '_boolean_flush', {'_boolean' : []}],
	# _eq
	[{'_string' : ['A', 'B']}, '_string_eq', {'_boolean' : [False]}],
	[{'_float' : [1.23, 1.23]}, '_float_eq', {'_boolean' : [True]}],
	# _stack_depth
	[{'_integer' : [3, 2, 1]}, '_integer_stack_depth', {'_integer' : [3, 2, 1, 3]}],
	# _yank
	[{'_boolean' : [True, True, False], '_integer' : [1]}, '_boolean_yank', {'_boolean' : [True, False, True]}],
	# _yankduper
	[{'_string' : ['A', 'B', 'C'], '_integer' : [1]}, '_string_yankdup', {'_string' : ['A', 'B', 'C', 'B']}],
	# _shove
	[{'_float' : [1.1, 2.2, 3.3, 4.4], '_integer' : [2]}, '_float_shove', {'_float' : [1.1, 4.4, 2.2, 3.3]}],
	# _empty
	[{'_integer' : []}, '_integer_empty', {'_boolean' : [True]}],
	[{'_boolean' : [True]}, '_boolean_empty', {'_boolean' : [True, False]}],
	]

for t in common_tests:
	passed = i_t.run_test(t)
	if not passed:
		raise Exception("The following test failed: " + str(t))
print("All common instructions passed.")