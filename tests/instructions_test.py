from __future__ import absolute_import, division, print_function, unicode_literals 

import pyshgp.utils as u
import pyshgp.push.interpreter as interp
import pyshgp.push.instructions.registered_instructions as ri
from pyshgp.push.instructions import *

def dict_matches_state(push_state, state_dict):
	i = 0
	for k in state_dict.keys():
		if not state_dict[k][:] == push_state.stacks[k][:]:
			return False
		i += len(state_dict[k])
	if i == push_state.size():
		return True
	else:
		return False

def run_test(test_info, print_actual=False):
	interpreter = interp.PushInterpreter()
	interpreter.load_state(test_info[0])
	intstruction = ri.get_instruction(test_info[1])
	interpreter.execute_instruction(intstruction)
	if print_actual:
		interpreter.state.pretty_print()
		print()
	return dict_matches_state(interpreter.state, test_info[2])