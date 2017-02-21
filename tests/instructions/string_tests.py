from __future__ import absolute_import, division, print_function, unicode_literals 

import pyshgp.utils as u

from .. import instructions_test as i_t

string_tests = [
	# _string_from_integer
	[{'_integer' : [7]}, '_string_from_integer', {'_string' : ['7']}],
	[{'_integer' : [-7]}, '_string_from_integer', {'_string' : ['-7']}],
	# _string_from_float
	[{'_float' : [7.0]}, '_string_from_float', {'_string' : ['7.0']}],
	[{'_float' : [-7.123]}, '_string_from_float', {'_string' : ['-7.123']}],
	# _string_from_boolean
	[{'_boolean' : [True]}, '_string_from_boolean', {'_string' : ['True']}],
	[{'_boolean' : [False]}, '_string_from_boolean', {'_string' : ['False']}],
	# _string_concat
	[{'_string' : ['', '']}, '_string_concat', {'_string' : ['']}],
	[{'_string' : ['A', '']}, '_string_concat', {'_string' : ['A']}],
	[{'_string' : ['', 'A']}, '_string_concat', {'_string' : ['A']}],
	[{'_string' : ['A', 'B']}, '_string_concat', {'_string' : ['AB']}],
	# _string_head
	[{'_string' : ['HelloWorld'], '_integer' : [5]}, '_string_head', {'_string' : ['Hello']}],
	[{'_string' : [''], '_integer' : [5]}, '_string_head', {'_string' : ['']}],
	[{'_string' : ['HelloWorld'], '_integer' : [-3]}, '_string_head', {'_string' : ['HelloWo']}],
	# _string_tail
	[{'_string' : ['HelloWorld'], '_integer' : [5]}, '_string_tail', {'_string' : ['World']}],
	[{'_string' : [''], '_integer' : [5]}, '_string_tail', {'_string' : ['']}],
	[{'_string' : ['HelloWorld'], '_integer' : [-3]}, '_string_tail', {'_string' : ['loWorld']}],
	# _string_split_at_index
	[{'_string' : ['HelloWorld'], '_integer' : [5]}, '_string_split_at_index', {'_string' : ['Hello', 'World']}],
	[{'_string' : [''], '_integer' : [5]}, '_string_split_at_index', {'_string' : ['', '']}],
	[{'_string' : ['HelloWorld'], '_integer' : [-3]}, '_string_split_at_index', {'_string' : ['HelloWo', 'rld']}],
	# _string_split_at_str
	[{'_string' : ['', '']}, '_string_split_at_str', {'_string' : ['']}],
	[{'_string' : ['HelloWorld', '']}, '_string_split_at_str', {'_string' : ['HelloWorld']}],
	[{'_string' : ['HelloWorld', 'o']}, '_string_split_at_str', {'_string' : ['Hell', 'W', 'rld']}],
	[{'_string' : ['HelloWorld', 'a']}, '_string_split_at_str', {'_string' : ['HelloWorld']}],
	# _string_split_at_char
	[{'_string' : [''], '_char' : [u.Character('o')]}, '_string_split_at_char', {'_string' : ['']}],
	[{'_string' : ['HelloWorld'], '_char' : [u.Character('o')]}, '_string_split_at_char', {'_string' : ['Hell', 'W', 'rld']}],
	[{'_string' : ['HelloWorld'], '_char' : [u.Character('a')]}, '_string_split_at_char', {'_string' : ['HelloWorld']}],
	# _string_split_at_space
	[{'_string' : ['']}, '_string_split_at_space', {'_string' : ['']}],
	[{'_string' : ['HelloWorld']}, '_string_split_at_space', {'_string' : ['HelloWorld']}],
	[{'_string' : ['Hello World']}, '_string_split_at_space', {'_string' : ['Hello', 'World']}],
	[{'_string' : ['Just 3 Words']}, '_string_split_at_space', {'_string' : ['Just', '3', 'Words']}],
	# _string_length
	[{'_string' : ['']}, '_string_length', {'_integer' : [0]}],
	[{'_string' : ['Hello']}, '_string_length', {'_integer' : [5]}],
	# _string_reverse
	[{'_string' : ['']}, '_string_reverse', {'_string' : ['']}],
	[{'_string' : ['Hello']}, '_string_reverse', {'_string' : ['olleH']}],
	# _string_char_at
	[{'_string' : [''], '_integer' : [2]}, '_string_char_at', {'_string' : [''], '_integer' : [2]}],
	[{'_string' : ['Hello'], '_integer' : [1]}, '_string_char_at', {'_char' : [u.Character('e')]}],
	# _string_empty_string
	[{'_string' : ['']}, '_string_empty_string', {'_boolean' : [True]}],
	[{'_string' : ['Hello']}, '_string_empty_string', {'_boolean' : [False]}],
	# _string_contains
	[{'_string' : ['', '']}, '_string_contains', {'_boolean' : [True]}],
	[{'_string' : ['', 'A']}, '_string_contains', {'_boolean' : [False]}],
	[{'_string' : ['A', '']}, '_string_contains', {'_boolean' : [True]}],
	[{'_string' : ['A', 'A']}, '_string_contains', {'_boolean' : [True]}],
	[{'_string' : ['A', 'AB']}, '_string_contains', {'_boolean' : [False]}],
	[{'_string' : ['AB', 'A']}, '_string_contains', {'_boolean' : [True]}],
	# _string_empty_string
	[{'_string' : ['', '', '']}, '_string_replace', {'_string' : ['']}],
	[{'_string' : ['', '', 'A']}, '_string_replace', {'_string' : ['A']}],
	[{'_string' : ['', 'A', '']}, '_string_replace', {'_string' : ['']}],
	[{'_string' : ['', 'A', 'A']}, '_string_replace', {'_string' : ['']}],
	[{'_string' : ['A', '', '']}, '_string_replace', {'_string' : ['A']}],
	[{'_string' : ['A', '', 'A']}, '_string_replace', {'_string' : ['AAA']}],
	[{'_string' : ['A', 'A', '']}, '_string_replace', {'_string' : ['']}],
	[{'_string' : ['A', 'A', 'A']}, '_string_replace', {'_string' : ['A']}],
	[{'_string' : ['', 'A', 'A']}, '_string_replace', {'_string' : ['']}],
	[{'_string' : ['AB', 'A', 'Z']}, '_string_replace', {'_string' : ['ZB']}],
	# _string_from_char
	[{'_char' : [u.Character('e')]}, '_string_from_char', {'_string' : ['e']}],
	# _string_append_char
	[{'_char' : [u.Character('C')], '_string' : ['']}, '_string_append_char', {'_string' : ['C']}],
	[{'_char' : [u.Character('C')], '_string' : ['AB']}, '_string_append_char', {'_string' : ['ABC']}],
	# _string_first
	[{'_string' : ['']}, '_string_first', {'_string' : ['']}],
	[{'_string' : ['A']}, '_string_first', {'_char' : [u.Character('A')]}],
	[{'_string' : ['AB']}, '_string_first', {'_char' : [u.Character('A')]}],
	# _string_last
	[{'_string' : ['']}, '_string_last', {'_string' : ['']}],
	[{'_string' : ['A']}, '_string_last', {'_char' : [u.Character('A')]}],
	[{'_string' : ['AB']}, '_string_last', {'_char' : [u.Character('B')]}],
	# _string_nth
	[{'_string' : [''], '_integer' : [1]}, '_string_nth', {'_string' : [''], '_integer' : [1]}],
	[{'_string' : ['A'], '_integer' : [1]}, '_string_nth', {'_char' : [u.Character('A')]}],
	[{'_string' : ['AB'], '_integer' : [3]}, '_string_nth', {'_char' : [u.Character('B')]}],
	# _string_replace_char
	[{'_string' : [''], '_char' : [u.Character('A'), u.Character('B')]}, '_string_replace_char', {'_string' : ['']}],
	[{'_string' : ['A'], '_char' : [u.Character('A'), u.Character('B')]}, '_string_replace_char', {'_string' : ['B']}],
	[{'_string' : ['B'], '_char' : [u.Character('A'), u.Character('B')]}, '_string_replace_char', {'_string' : ['B']}],
	[{'_string' : ['AA'], '_char' : [u.Character('A'), u.Character('B')]}, '_string_replace_char', {'_string' : ['BB']}],
	# _string_replace_first_char
	[{'_string' : [''], '_char' : [u.Character('A'), u.Character('B')]}, '_string_replace_first_char', {'_string' : ['']}],
	[{'_string' : ['A'], '_char' : [u.Character('A'), u.Character('B')]}, '_string_replace_first_char', {'_string' : ['B']}],
	[{'_string' : ['B'], '_char' : [u.Character('A'), u.Character('B')]}, '_string_replace_first_char', {'_string' : ['B']}],
	[{'_string' : ['AA'], '_char' : [u.Character('A'), u.Character('B')]}, '_string_replace_first_char', {'_string' : ['BA']}],
	# _string_remove_char
	[{'_string' : [''], '_char' : [u.Character('A')]}, '_string_remove_char', {'_string' : ['']}],
	[{'_string' : ['A'], '_char' : [u.Character('A')]}, '_string_remove_char', {'_string' : ['']}],
	[{'_string' : ['B'], '_char' : [u.Character('A')]}, '_string_remove_char', {'_string' : ['B']}],
	[{'_string' : ['AA'], '_char' : [u.Character('A')]}, '_string_remove_char', {'_string' : ['']}],
	[{'_string' : ['AB'], '_char' : [u.Character('A')]}, '_string_remove_char', {'_string' : ['B']}],
	]

for t in string_tests:
	passed = i_t.run_test(t, False)
	if not passed:
		raise Exception("The following test failed: " + str(t))
print("All string instructions passed.")