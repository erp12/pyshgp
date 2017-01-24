from __future__ import absolute_import, division, print_function, unicode_literals 

from pyshgp import utils as u

from .. import instructions_test as i_t

char_tests = [
	# _char_all_from_string
	[{'_string' : ['abc']}, '_char_all_from_string', {'_char' : [u.Character('c'), u.Character('b'), u.Character('a')]}],
	[{'_string' : ['a \n']}, '_char_all_from_string', {'_char' : [u.Character('\n'), u.Character(' '), u.Character('a')]}],
	[{'_string' : ['']}, '_char_all_from_string', {'_char' : []}],
	# _char_from_integer
	[{'_integer' : [97]}, '_char_from_integer', {'_char' : [u.Character('a')]}],
	[{'_integer' : [33]}, '_char_from_integer', {'_char' : [u.Character('!')]}],
	[{'_integer' : [10]}, '_char_from_integer', {'_char' : [u.Character('\n')]}],
	[{'_integer' : [32]}, '_char_from_integer', {'_char' : [u.Character(' ')]}],
	# _char_from_float
	[{'_float' : [97.1]}, '_char_from_float', {'_char' : [u.Character('a')]}],
	[{'_float' : [33.2]}, '_char_from_float', {'_char' : [u.Character('!')]}],
	[{'_float' : [10.3]}, '_char_from_float', {'_char' : [u.Character('\n')]}],
	[{'_float' : [32.9]}, '_char_from_float', {'_char' : [u.Character(' ')]}],
	# _char_is_letter
	[{'_char' : [u.Character('a')]}, '_char_is_letter', {'_boolean' : [True]}],
	[{'_char' : [u.Character('7')]}, '_char_is_letter', {'_boolean' : [False]}],
	[{'_char' : [u.Character('!')]}, '_char_is_letter', {'_boolean' : [False]}],
	[{'_char' : [u.Character('\n')]}, '_char_is_letter', {'_boolean' : [False]}],
	[{'_char' : [u.Character(' ')]}, '_char_is_letter', {'_boolean' : [False]}],
	# _char_is_digit
	[{'_char' : [u.Character('a')]}, '_char_is_digit', {'_boolean' : [False]}],
	[{'_char' : [u.Character('7')]}, '_char_is_digit', {'_boolean' : [True]}],
	[{'_char' : [u.Character('!')]}, '_char_is_digit', {'_boolean' : [False]}],
	[{'_char' : [u.Character('\n')]}, '_char_is_digit', {'_boolean' : [False]}],
	[{'_char' : [u.Character(' ')]}, '_char_is_digit', {'_boolean' : [False]}],
	# _char_is_white_space
	[{'_char' : [u.Character('a')]}, '_char_is_white_space', {'_boolean' : [False]}],
	[{'_char' : [u.Character('7')]}, '_char_is_white_space', {'_boolean' : [False]}],
	[{'_char' : [u.Character('!')]}, '_char_is_white_space', {'_boolean' : [False]}],
	[{'_char' : [u.Character('\n')]}, '_char_is_white_space', {'_boolean' : [True]}],
	[{'_char' : [u.Character(' ')]}, '_char_is_white_space', {'_boolean' : [True]}],
	]

for t in char_tests:
	passed = i_t.run_test(t)
	if not passed:
		raise Exception("The following test failed: " + str(t))
print("All char instructions passed.")