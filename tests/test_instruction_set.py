from __future__ import absolute_import, division, print_function, unicode_literals 

import pysh.pysh_interpreter as interp
from pysh.instructions import boolean, char, code, common, numbers, string, input_output
from pysh.instructions import registered_instructions as ri

print("Setting up Pysh interpreter...")
interpreter = interp.Pysh_Interpreter()

print("Testing boolean_and")
prog = [True, False, ri.get_instruction_by_name('boolean_and')]
result = interpreter.run_push(prog)
assert interpreter.state.total_state_size() == 1
assert len(interpreter.state.stacks['_boolean']) == 1
assert interpreter.state.stacks['_boolean'].top_item() == False

prog = [True, True, ri.get_instruction_by_name('boolean_and')]
result = interpreter.run_push(prog)
assert interpreter.state.total_state_size() == 1
assert len(interpreter.state.stacks['_boolean']) == 1
assert interpreter.state.stacks['_boolean'].top_item() == True

print("Testing boolean_or")
prog = [True, False, ri.get_instruction_by_name('boolean_or')]
result = interpreter.run_push(prog)
assert interpreter.state.total_state_size() == 1
assert len(interpreter.state.stacks['_boolean']) == 1
assert interpreter.state.stacks['_boolean'].top_item() == True

prog = [False, False, ri.get_instruction_by_name('boolean_or')]
result = interpreter.run_push(prog)
assert interpreter.state.total_state_size() == 1
assert len(interpreter.state.stacks['_boolean']) == 1
assert interpreter.state.stacks['_boolean'].top_item() == False

print("Testing boolean_not")
prog = [True, ri.get_instruction_by_name('boolean_not')]
result = interpreter.run_push(prog)
assert interpreter.state.total_state_size() == 1
assert len(interpreter.state.stacks['_boolean']) == 1
assert interpreter.state.stacks['_boolean'].top_item() == False

prog = [False, ri.get_instruction_by_name('boolean_not')]
result = interpreter.run_push(prog)
assert interpreter.state.total_state_size() == 1
assert len(interpreter.state.stacks['_boolean']) == 1
assert interpreter.state.stacks['_boolean'].top_item() == True