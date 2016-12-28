from __future__ import absolute_import, division, print_function, unicode_literals 

from .. import instructions_test as i_t

boolean_tests = [
	# _boolean_and
	[{'_boolean' : [False, False]}, '_boolean_and', {'_boolean' : [False]}],
	[{'_boolean' : [False, True]}, '_boolean_and', {'_boolean' : [False]}],
	[{'_boolean' : [True, False]}, '_boolean_and', {'_boolean' : [False]}],
	[{'_boolean' : [True, True]}, '_boolean_and', {'_boolean' : [True]}],
	# _boolean_or
	[{'_boolean' : [False, False]}, '_boolean_or', {'_boolean' : [False]}],
	[{'_boolean' : [False, True]}, '_boolean_or', {'_boolean' : [True]}],
	[{'_boolean' : [True, False]}, '_boolean_or', {'_boolean' : [True]}],
	[{'_boolean' : [True, True]}, '_boolean_or', {'_boolean' : [True]}],
	# _boolan_not
	[{'_boolean' : [False]}, '_boolean_not', {'_boolean' : [True]}],
	[{'_boolean' : [True]}, '_boolean_not', {'_boolean' : [False]}],
	# _boolean_xor
	[{'_boolean' : [False, False]}, '_boolean_xor', {'_boolean' : [False]}],
	[{'_boolean' : [False, True]}, '_boolean_xor', {'_boolean' : [True]}],
	[{'_boolean' : [True, False]}, '_boolean_xor', {'_boolean' : [True]}],
	[{'_boolean' : [True, True]}, '_boolean_xor', {'_boolean' : [False]}],
	# _boolean_invert_first_then_and
	[{'_boolean' : [False, False]}, '_boolean_invert_first_then_and', {'_boolean' : [False]}],
	[{'_boolean' : [False, True]}, '_boolean_invert_first_then_and', {'_boolean' : [False]}],
	[{'_boolean' : [True, False]}, '_boolean_invert_first_then_and', {'_boolean' : [True]}],
	[{'_boolean' : [True, True]}, '_boolean_invert_first_then_and', {'_boolean' : [False]}],
	# _boolean_invert_second_then_and
	[{'_boolean' : [False, False]}, '_boolean_invert_second_then_and', {'_boolean' : [False]}],
	[{'_boolean' : [False, True]}, '_boolean_invert_second_then_and', {'_boolean' : [True]}],
	[{'_boolean' : [True, False]}, '_boolean_invert_second_then_and', {'_boolean' : [False]}],
	[{'_boolean' : [True, True]}, '_boolean_invert_second_then_and', {'_boolean' : [False]}],
	# _boolean_from_integer
	[{'_integer' : [0]}, '_boolean_from_integer', {'_boolean' : [False]}],
	[{'_integer' : [1]}, '_boolean_from_integer', {'_boolean' : [True]}],
	[{'_integer' : [-1]}, '_boolean_from_integer', {'_boolean' : [True]}],
	# _boolean_from_float
	[{'_float' : [0.0]}, '_boolean_from_float', {'_boolean' : [False]}],
	[{'_float' : [1.1]}, '_boolean_from_float', {'_boolean' : [True]}],
	[{'_float' : [-1.9]}, '_boolean_from_float', {'_boolean' : [True]}],
	]

for t in boolean_tests:
	passed = i_t.run_test(t)
	if not passed:
		raise Exception("The following test failed: " + str(t))
print("All boolean instructions passed.")