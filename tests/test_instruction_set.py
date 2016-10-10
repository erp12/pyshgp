from __future__ import absolute_import, division, print_function, unicode_literals 

import pysh.pysh_interpreter as interp
from pysh.instructions import boolean, char, code, common, numbers, string, input_output
from pysh.instructions import registered_instructions as ri


print("Setting up Pysh interpreter...")
i = interp.Pysh_Interpreter()

print("Testing boolean_and")
prog = [True, False, ri.get_instruction_by_name('boolean_and')]
result = i.run_push(prog)
assert i.state.total_state_size() == 1,						"State has %r items. Should be 1." % i.state.total_state_size()
assert len(i.state.stacks['_boolean']) == 1, 				i.state.stacks['_boolean']
assert i.state.stacks['_boolean'].top_item() == False, 		i.state.stacks['_boolean'].top_item()

prog = [True, True, ri.get_instruction_by_name('boolean_and')]
result = i.run_push(prog)
assert i.state.total_state_size() == 1,						"State has %r items. Should be 1." % i.state.total_state_size()
assert len(i.state.stacks['_boolean']) == 1					i.state.stacks['_boolean']
assert i.state.stacks['_boolean'].top_item() == True		i.state.stacks['_boolean'].top_item()

print("Testing boolean_or")
prog = [True, False, ri.get_instruction_by_name('boolean_or')]
result = i.run_push(prog)
assert i.state.total_state_size() == 1,						"State has %r items. Should be 1." % i.state.total_state_size()
assert len(i.state.stacks['_boolean']) == 1					i.state.stacks['_boolean']
assert i.state.stacks['_boolean'].top_item() == True		i.state.stacks['_boolean'].top_item()

prog = [False, False, ri.get_instruction_by_name('boolean_or')]
result = i.run_push(prog)
assert i.state.total_state_size() == 1,						"State has %r items. Should be 1." % i.state.total_state_size()
assert len(i.state.stacks['_boolean']) == 1					i.state.stacks['_boolean']
assert i.state.stacks['_boolean'].top_item() == False		i.state.stacks['_boolean'].top_item()

print("Testing boolean_not")
prog = [True, ri.get_instruction_by_name('boolean_not')]
result = i.run_push(prog)
assert i.state.total_state_size() == 1,						"State has %r items. Should be 1." % i.state.total_state_size()
assert len(i.state.stacks['_boolean']) == 1					i.state.stacks['_boolean']
assert i.state.stacks['_boolean'].top_item() == False		i.state.stacks['_boolean'].top_item()

prog = [False, ri.get_instruction_by_name('boolean_not')]
result = i.run_push(prog)
assert i.state.total_state_size() == 1,						"State has %r items. Should be 1." % i.state.total_state_size()
assert len(i.state.stacks['_boolean']) == 1					i.state.stacks['_boolean']
assert i.state.stacks['_boolean'].top_item() == True		i.state.stacks['_boolean'].top_item()