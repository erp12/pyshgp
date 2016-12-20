from __future__ import absolute_import, division, print_function, unicode_literals 

import pysh.utils as u
import pysh.push.interpreter as interp
import pysh.push.instructions.registered_instructions as ri
from pysh.push.instructions import *
import pysh.push.instruction as instr

print(ri.registered_instructions)

print("Setting up Pysh interpreter...")
i = interp.PyshInterpreter()


print("Testing boolean_and")
i.reset_pysh_state()
prog = [True, False, ri.get_instruction('_boolean_and')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False

i.reset_pysh_state()
prog = [True, True, ri.get_instruction('_boolean_and')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True


print("Testing boolean_or")
i.reset_pysh_state()
prog = [True, False, ri.get_instruction('_boolean_or')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [False, False, ri.get_instruction('_boolean_or')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


print("Testing boolean_not")
i.reset_pysh_state()
prog = [True, ri.get_instruction('_boolean_not')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False

i.reset_pysh_state()
prog = [False, ri.get_instruction('_boolean_not')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True


print("Testing boolean_xor")
i.reset_pysh_state()
prog = [True, False, ri.get_instruction('_boolean_xor')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [True, True, ri.get_instruction('_boolean_xor')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


print("Testing boolean_invert_first_then_and")
i.reset_pysh_state()
prog = [True, False, ri.get_instruction('_boolean_invert_first_then_and')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [True, True, ri.get_instruction('_boolean_invert_first_then_and')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


print("Testing boolean_invert_second_then_and")
i.reset_pysh_state()
prog = [False, True, ri.get_instruction('_boolean_invert_second_then_and')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [True, True, ri.get_instruction('_boolean_invert_second_then_and')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


print("Testing boolean_from_integer")
i.reset_pysh_state()
prog = [1, ri.get_instruction('_boolean_from_integer')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [0, ri.get_instruction('_boolean_from_integer')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False

i.reset_pysh_state()
prog = [-5, ri.get_instruction('_boolean_from_integer')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True


print("Testing boolean_from_float")
i.reset_pysh_state()
prog = [1.0, ri.get_instruction('_boolean_from_float')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [0.0, ri.get_instruction('_boolean_from_float')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False

i.reset_pysh_state()
prog = [-2.5, ri.get_instruction('_boolean_from_float')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True


print("Testing char_all_from_string")
i.reset_pysh_state()
prog = ['', ri.get_instruction('_char_all_from_string')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())
assert len(i.state.stacks['_char']) == 0
assert len(i.state.stacks['_string']) == 0

i.reset_pysh_state()
prog = ["pysh", ri.get_instruction('_char_all_from_string')]
i.run_push(prog)
if not i.state.size() == 4:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 4." % i.state.size())
assert len(i.state.stacks['_char']) == 4
assert len(i.state.stacks['_string']) == 0
assert i.state.stacks['_char'].top_item().char == 'p'

i.reset_pysh_state()
prog = ['\n', ri.get_instruction('_char_all_from_string')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 1
assert len(i.state.stacks['_string']) == 0
assert i.state.stacks['_char'].top_item().char == '\n'


print("Testing char_from_integer")
i.reset_pysh_state()
prog = [97, ri.get_instruction('_char_from_integer')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 1
assert len(i.state.stacks['_integer']) == 0
assert i.state.stacks['_char'].top_item().char == 'a'


print("Testing char_from_float")
i.reset_pysh_state()
prog = [97.8, ri.get_instruction('_char_from_float')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 1
assert len(i.state.stacks['_float']) == 0
assert i.state.stacks['_char'].top_item().char == 'a'


print("Testing char_is_letter")
i.reset_pysh_state()
prog = [u.Character('G'), ri.get_instruction('_char_is_letter')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [u.Character('7'), ri.get_instruction('_char_is_letter')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False

i.reset_pysh_state()
prog = [u.Character('\n'), ri.get_instruction('_char_is_letter')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


print("Testing char_is_digit")
i.reset_pysh_state()
prog = [u.Character('G'), ri.get_instruction('_char_is_digit')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False

i.reset_pysh_state()
prog = [u.Character('7'), ri.get_instruction('_char_is_digit')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [u.Character('\n'), ri.get_instruction('_char_is_digit')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


print("Testing char_is_white_space")
i.reset_pysh_state()
prog = [u.Character('G'), ri.get_instruction('_char_is_white_space')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False

i.reset_pysh_state()
prog = [u.Character('7'), ri.get_instruction('_char_is_white_space')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False

i.reset_pysh_state()
prog = [u.Character('\n'), ri.get_instruction('_char_is_white_space')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing exec_noop")
prog = [ri.get_instruction('_exec_noop')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())
assert len(i.state.stacks['_exec']) == 0


i.reset_pysh_state()
print("Testing code_noop")
prog = [ri.get_instruction('_code_noop')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())
assert len(i.state.stacks['_code']) == 0


i.reset_pysh_state()
print("Testing code_from_boolean")
prog = [True, ri.get_instruction('_code_from_boolean')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert len(i.state.stacks['_boolean']) == 0
assert i.state.stacks['_code'].top_item() == True


i.reset_pysh_state()
print("Testing code_from_float")
prog = [1.5, ri.get_instruction('_code_from_float')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert len(i.state.stacks['_float']) == 0
assert i.state.stacks['_code'].top_item() == 1.5


i.reset_pysh_state()
print("Testing code_from_integer")
prog = [5, ri.get_instruction('_code_from_integer')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert len(i.state.stacks['_integer']) == 0
assert i.state.stacks['_code'].top_item() == 5


i.reset_pysh_state()
print("Testing code_from_exec")
prog = [ri.get_instruction('_code_from_exec'), ri.get_instruction('_exec_noop'),]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert len(i.state.stacks['_exec']) == 0
assert i.state.stacks['_code'].top_item().name == '_exec_noop'


i.reset_pysh_state()
print("Testing code_append")
prog = [5, True, ri.get_instruction('_code_from_integer'), ri.get_instruction('_code_from_boolean'), ri.get_instruction('_code_append'),]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert len(i.state.stacks['_integer']) == 0
assert len(i.state.stacks['_boolean']) == 0
assert i.state.stacks['_code'].top_item() == [True, 5]


i.reset_pysh_state()
print("Testing code_atom")
prog = [5, ri.get_instruction('_code_from_integer'), ri.get_instruction('_code_atom')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [ri.get_instruction('_code_from_exec'), [5, True], ri.get_instruction('_code_atom')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


i.reset_pysh_state()
print("Testing code_car")
prog = [ri.get_instruction('_code_from_exec'), [5, True], ri.get_instruction('_code_car')]
i.run_push(prog)
if not i.state.size() == 1:
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert i.state.stacks['_code'].top_item() == 5

i.reset_pysh_state()
prog = [ri.get_instruction('_code_from_exec'), 5, ri.get_instruction('_code_car')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert i.state.stacks['_code'].top_item() == 5


i.reset_pysh_state()
print("Testing code_cdr")
prog = [ri.get_instruction('_code_from_exec'), [5, True], ri.get_instruction('_code_cdr')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert i.state.stacks['_code'].top_item() == [True]

i.reset_pysh_state()
prog = [ri.get_instruction('_code_from_exec'), 5, ri.get_instruction('_code_cdr')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert i.state.stacks['_code'].top_item() == []


i.reset_pysh_state()
print("Testing code_do")
prog = [ri.get_instruction('_code_from_exec'), [5, True], ri.get_instruction('_code_do')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert len(i.state.stacks['_integer']) == 1
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_integer'].top_item() == 5
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing code_do*")
prog = [ri.get_instruction('_code_from_exec'), [5, True], ri.get_instruction('_code_do*')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert len(i.state.stacks['_integer']) == 1
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_integer'].top_item() == 5
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing code_do*range")
prog = [1, 5, ri.get_instruction('_code_from_exec'), True, ri.get_instruction('_code_do*range')]
i.run_push(prog)
if not i.state.size() == 10:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 10." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert len(i.state.stacks['_boolean']) == 5
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing exec_do*range")
prog = [1, 5, ri.get_instruction('_exec_do*range'), True]
i.run_push(prog)
if not i.state.size() == 10:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 10." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert len(i.state.stacks['_boolean']) == 5
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing code_do*count")
prog = [ri.get_instruction('_code_from_exec'), True, 5, ri.get_instruction('_code_do*count')]
i.run_push(prog)
if not i.state.size() == 10:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 10." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert len(i.state.stacks['_boolean']) == 5
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing exec_do*count")
prog = [5, ri.get_instruction('_exec_do*count'), True]
i.run_push(prog)
if not i.state.size() == 10:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 10." % i.state.size())
assert len(i.state.stacks['_boolean']) == 5
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing code_do*times")
prog = [ri.get_instruction('_code_from_exec'), True, 5, ri.get_instruction('_code_do*times')]
i.run_push(prog)
if not i.state.size() == 5:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 5." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert len(i.state.stacks['_boolean']) == 5
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing exec_do*times")
prog = [5, ri.get_instruction('_exec_do*times'), True]
i.run_push(prog)
if not i.state.size() == 5:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 5." % i.state.size())
assert len(i.state.stacks['_boolean']) == 5
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing exec_while")
prog = [False, True, True, True, ri.get_instruction('_exec_while'), 5]
i.run_push(prog)
if not i.state.size() == 3:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 3." % i.state.size())
assert len(i.state.stacks['_integer']) == 3
assert i.state.stacks['_integer'].top_item() == 5


i.reset_pysh_state()
print("Testing exec_do*while")
prog = [False, True, True, True, ri.get_instruction('_exec_do*while'), 5]
i.run_push(prog)
if not i.state.size() == 4:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 4." % i.state.size())
assert len(i.state.stacks['_integer']) == 4
assert i.state.stacks['_integer'].top_item() == 5


i.reset_pysh_state()
print("Testing code_if")
prog = [True, ri.get_instruction('_code_from_exec'), "Hello", ri.get_instruction('_code_from_exec'), "World", ri.get_instruction('_code_if')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_string']) == 1
assert len(i.state.stacks['_boolean']) == 0
assert len(i.state.stacks['_code']) == 0
assert i.state.stacks['_string'].top_item() == "Hello"

i.reset_pysh_state()
prog = [False, ri.get_instruction('_code_from_exec'), "Hello", ri.get_instruction('_code_from_exec'), "World", ri.get_instruction('_code_if')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_string']) == 1
assert len(i.state.stacks['_boolean']) == 0
assert len(i.state.stacks['_code']) == 0
assert i.state.stacks['_string'].top_item() == "World"


i.reset_pysh_state()
print("Testing exec_if")
prog = [True, ri.get_instruction('_exec_if'), "Hello", "World"]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1" % i.state.size())
assert len(i.state.stacks['_string']) == 1
assert len(i.state.stacks['_boolean']) == 0
assert len(i.state.stacks['_code']) == 0
assert i.state.stacks['_string'].top_item() == "Hello"

i.reset_pysh_state()
prog = [False, ri.get_instruction('_exec_if'), "Hello", "World"]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_string']) == 1
assert len(i.state.stacks['_boolean']) == 0
assert len(i.state.stacks['_code']) == 0
assert i.state.stacks['_string'].top_item() == "World"


i.reset_pysh_state()
print("Testing exec_when")
prog = [True, ri.get_instruction('_exec_when'), "Hello", "World"]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_string']) == 2
assert len(i.state.stacks['_boolean']) == 0
assert len(i.state.stacks['_code']) == 0
assert i.state.stacks['_string'].top_item() == "World"

i.reset_pysh_state()
prog = [False, ri.get_instruction('_exec_when'), "Hello", "World"]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_string']) == 1
assert len(i.state.stacks['_boolean']) == 0
assert len(i.state.stacks['_code']) == 0
assert i.state.stacks['_string'].top_item() == "World"


i.reset_pysh_state()
print("Testing code_length")
prog = [ri.get_instruction('_code_from_exec'), [1, 2, ri.get_instruction('_integer_add')], ri.get_instruction('_code_length')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert i.state.stacks['_integer'].top_item() == 3

i.reset_pysh_state()
prog = [ri.get_instruction('_code_from_exec'), 5, ri.get_instruction('_code_length')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert i.state.stacks['_integer'].top_item() == 1


i.reset_pysh_state()
print("Testing code_list")
prog = [ri.get_instruction('_code_from_exec'), 5, ri.get_instruction('_code_from_exec'), 4, ri.get_instruction('_code_list')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert i.state.stacks['_code'].top_item() == [5, 4]


i.reset_pysh_state()
print("Testing code_member")
prog = [ri.get_instruction('_code_from_exec'), 5, ri.get_instruction('_code_from_exec'), [5, 4], ri.get_instruction('_code_member')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [ri.get_instruction('_code_from_exec'), 5, ri.get_instruction('_code_from_exec'), [1, 3], ri.get_instruction('_code_member')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


i.reset_pysh_state()
print("Testing code_nth")
prog = [ri.get_instruction('_code_from_exec'), [1, 2, 3, 4], 1, ri.get_instruction('_code_nth')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert len(i.state.stacks['_integer']) == 0
assert i.state.stacks['_code'].top_item() == 2

i.reset_pysh_state()
prog = [ri.get_instruction('_code_from_exec'), [1, 2, 3, 4], 5, ri.get_instruction('_code_nth')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert len(i.state.stacks['_integer']) == 0
assert i.state.stacks['_code'].top_item() == 2


i.reset_pysh_state()
print("Testing code_nthcdr")
prog = [ri.get_instruction('_code_from_exec'), [1, 2, 3, 4], 1, ri.get_instruction('_code_nthcdr')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert len(i.state.stacks['_integer']) == 0
assert i.state.stacks['_code'].top_item() == [1, 3, 4]

i.reset_pysh_state()
prog = [ri.get_instruction('_code_from_exec'), [1, 2, 3, 4], 5, ri.get_instruction('_code_nthcdr')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert len(i.state.stacks['_integer']) == 0
assert i.state.stacks['_code'].top_item() == [1, 3, 4]


i.reset_pysh_state()
print("Testing exec_pop")
prog = [ri.get_instruction('_exec_pop'), ri.get_instruction('_integer_stack_depth')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())
assert len(i.state.stacks['_integer']) == 0


i.reset_pysh_state()
print("Testing integer_pop")
prog = [5, ri.get_instruction('_integer_pop')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())
assert len(i.state.stacks['_integer']) == 0


i.reset_pysh_state()
print("Testing float_pop")
prog = [5.1, ri.get_instruction('_float_pop')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())
assert len(i.state.stacks['_float']) == 0


i.reset_pysh_state()
print("Testing code_pop")
prog = [ri.get_instruction('_code_from_exec'), [True, 5], ri.get_instruction('_code_pop')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())
assert len(i.state.stacks['_code']) == 0


i.reset_pysh_state()
print("Testing boolean_pop")
prog = [True, ri.get_instruction('_boolean_pop')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())
assert len(i.state.stacks['_boolean']) == 0


i.reset_pysh_state()
print("Testing string_pop")
prog = ["HelloWorld", ri.get_instruction('_string_pop')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())
assert len(i.state.stacks['_string']) == 0


i.reset_pysh_state()
print("Testing char_pop")
prog = [u.Character('G'), ri.get_instruction('_char_pop')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())
assert len(i.state.stacks['_char']) == 0

i.reset_pysh_state()
print("Testing exec_dup")
prog = [ri.get_instruction('_exec_dup'), 5]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_integer']) == 2
assert i.state.stacks['_integer'].top_item() == 5


i.reset_pysh_state()
print("Testing integer_dup")
prog = [5, ri.get_instruction('_integer_dup')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_integer']) == 2
assert i.state.stacks['_integer'].top_item() == 5


i.reset_pysh_state()
print("Testing float_dup")
prog = [5.1, ri.get_instruction('_float_dup')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_float']) == 2
assert i.state.stacks['_float'].top_item() == 5.1


i.reset_pysh_state()
print("Testing code_dup")
prog = [ri.get_instruction('_code_from_exec'), True, ri.get_instruction('_code_dup')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_code']) == 2
assert i.state.stacks['_code'].top_item() == True


i.reset_pysh_state()
print("Testing boolean_dup")
prog = [True, ri.get_instruction('_boolean_dup')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_boolean']) == 2
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing string_dup")
prog = ["HelloWorld", ri.get_instruction('_string_dup')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_string']) == 2
assert i.state.stacks['_string'].top_item() == "HelloWorld"


i.reset_pysh_state()
print("Testing char_dup")
prog = [u.Character('G'), ri.get_instruction('_char_dup')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_char']) == 2
assert i.state.stacks['_char'].top_item().char == "G"


i.reset_pysh_state()
print("Testing exec_swap")
prog = [ri.get_instruction('_exec_swap'), True, False]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_boolean']) == 2
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing integer_swap")
prog = [1, 2, ri.get_instruction('_integer_swap')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_integer']) == 2
assert i.state.stacks['_integer'].top_item() == 1


i.reset_pysh_state()
print("Testing float_swap")
prog = [1.1, 2.1, ri.get_instruction('_float_swap')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_float']) == 2
assert i.state.stacks['_float'].top_item() == 1.1


i.reset_pysh_state()
print("Testing code_swap")
prog = [ri.get_instruction('_code_from_exec'), True, ri.get_instruction('_code_from_exec'), False, ri.get_instruction('_code_swap')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_code']) == 2
assert i.state.stacks['_code'].top_item() == True


i.reset_pysh_state()
print("Testing boolean_swap")
prog = [True, False, ri.get_instruction('_boolean_swap')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_boolean']) == 2
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing string_swap")
prog = ["HelloWorld", "HelloWorld", ri.get_instruction('_string_swap')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_string']) == 2
assert i.state.stacks['_string'].top_item() == "HelloWorld"


i.reset_pysh_state()
print("Testing char_swap")
prog = [u.Character('A'), u.Character('B'), ri.get_instruction('_char_swap')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_char']) == 2
assert i.state.stacks['_char'].top_item().char == "A"


i.reset_pysh_state()
print("Testing exec_rot")
prog = [ri.get_instruction('_exec_rot'), "A", "B", "C"]
i.run_push(prog)
if not i.state.size() == 3:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 3." % i.state.size())
assert len(i.state.stacks['_string']) == 3
assert i.state.stacks['_string'].top_item() == "B"


i.reset_pysh_state()
print("Testing integer_rot")
prog = [1, 2, 3, ri.get_instruction('_integer_rot')]
i.run_push(prog)
if not i.state.size() == 3:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 3." % i.state.size())
assert len(i.state.stacks['_integer']) == 3
assert i.state.stacks['_integer'].top_item() == 1


i.reset_pysh_state()
print("Testing float_rot")
prog = [1.1, 2.2, 3.3, ri.get_instruction('_float_rot')]
i.run_push(prog)
if not i.state.size() == 3:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 3." % i.state.size())
assert len(i.state.stacks['_float']) == 3
assert i.state.stacks['_float'].top_item() == 1.1


i.reset_pysh_state()
print("Testing code_rot")
prog = [ri.get_instruction('_code_from_exec'), 1, ri.get_instruction('_code_from_exec'), 2, ri.get_instruction('_code_from_exec'), 3, ri.get_instruction('_code_rot')]
i.run_push(prog)
if not i.state.size() == 3:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 3." % i.state.size())
assert len(i.state.stacks['_code']) == 3
assert i.state.stacks['_code'].top_item() == 1


i.reset_pysh_state()
print("Testing boolean_rot")
prog = [True, False, True, ri.get_instruction('_boolean_rot')]
i.run_push(prog)
if not i.state.size() == 3:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 3." % i.state.size())
assert len(i.state.stacks['_boolean']) == 3
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing string_rot")
prog = ["A", "B", "C", ri.get_instruction('_string_rot')]
i.run_push(prog)
if not i.state.size() == 3:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 3." % i.state.size())
assert len(i.state.stacks['_string']) == 3
assert i.state.stacks['_string'].top_item() == "A"


i.reset_pysh_state()
print("Testing char_rot")
prog = [u.Character('A'), u.Character('B'), u.Character('C'), ri.get_instruction('_char_rot')]
i.run_push(prog)
if not i.state.size() == 3:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 3." % i.state.size())
assert len(i.state.stacks['_char']) == 3
assert i.state.stacks['_char'].top_item().char == "A"


i.reset_pysh_state()
print("Testing exec_flush")
prog = [ri.get_instruction('_exec_flush'), 1, 2, 3]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())


i.reset_pysh_state()
print("Testing integer_flush")
prog = [1, 2, 3, ri.get_instruction('_integer_flush')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())


i.reset_pysh_state()
print("Testing float_flush")
prog = [1.1, 2.2, 3.3, ri.get_instruction('_float_flush')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())


i.reset_pysh_state()
print("Testing code_flush")
prog = [ri.get_instruction('_code_from_exec'), 1, ri.get_instruction('_code_from_exec'), 2, ri.get_instruction('_code_from_exec'), 3, ri.get_instruction('_code_flush')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())


i.reset_pysh_state()
print("Testing boolean_flush")
prog = [True, False, True, ri.get_instruction('_boolean_flush')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())


i.reset_pysh_state()
print("Testing string_flush")
prog = ["Hello", "World", ri.get_instruction('_string_flush')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())


i.reset_pysh_state()
print("Testing char_flush")
prog = [u.Character('A'), u.Character('B'), u.Character('C'), ri.get_instruction('_char_flush')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())


i.reset_pysh_state()
print("Testing exec_eq")
prog = [ri.get_instruction('_exec_eq'), 1, 1]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [ri.get_instruction('_exec_eq'), 1, 2]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


i.reset_pysh_state()
print("Testing integer_eq")
prog = [1, 1, ri.get_instruction('_integer_eq')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [1, 2, ri.get_instruction('_integer_eq')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


i.reset_pysh_state()
print("Testing float_eq")
prog = [1.1, 1.1, ri.get_instruction('_float_eq')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [1.1, 2.2, ri.get_instruction('_float_eq')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


i.reset_pysh_state()
print("Testing code_eq")
prog = [ri.get_instruction('_code_from_exec'), 1, ri.get_instruction('_code_from_exec'), 1, ri.get_instruction('_code_eq')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [ri.get_instruction('_code_from_exec'), 1, ri.get_instruction('_code_from_exec'), 2, ri.get_instruction('_code_eq')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


i.reset_pysh_state()
print("Testing boolean_eq")
prog = [True, True, ri.get_instruction('_boolean_eq')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [True, False, ri.get_instruction('_boolean_eq')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


i.reset_pysh_state()
print("Testing string_eq")
prog = ["Hello", "Hello", ri.get_instruction('_string_eq')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = ["Hello", "World", ri.get_instruction('_string_eq')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


i.reset_pysh_state()
print("Testing char_eq")
prog = [u.Character('A'), u.Character('A'), ri.get_instruction('_char_eq')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [u.Character('A'), u.Character('B'), ri.get_instruction('_char_eq')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


i.reset_pysh_state()
print("Testing [type]_stack_depth instructions")
prog = [True, False, 1.5, ri.get_instruction('_exec_stack_depth'), ri.get_instruction('_integer_stack_depth'), ri.get_instruction('_float_stack_depth'), ri.get_instruction('_boolean_stack_depth')]
i.run_push(prog)
if not i.state.size() == 7:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 7." % i.state.size())
assert i.state.stacks['_integer'].stack_ref(0) == 2
assert i.state.stacks['_integer'].stack_ref(1) == 1
assert i.state.stacks['_integer'].stack_ref(2) == 1
assert i.state.stacks['_integer'].stack_ref(3) == 3


i.reset_pysh_state()
print("Testing exec_yank")
prog = [3, ri.get_instruction('_exec_yank'), 1, 2, 3, ri.get_instruction('_integer_stack_depth')]
i.run_push(prog)
if not i.state.size() == 4:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 4." % i.state.size())
assert i.state.stacks['_integer'].stack_ref(0) == 3
assert i.state.stacks['_integer'].stack_ref(1) == 2
assert i.state.stacks['_integer'].stack_ref(2) == 1
assert i.state.stacks['_integer'].stack_ref(3) == 0


i.reset_pysh_state()
print("Testing integer_yank")
prog = [0, 1, 2, 3, 2, ri.get_instruction('_integer_yank')]
i.run_push(prog)
if not i.state.size() == 4:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 4." % i.state.size())
assert i.state.stacks['_integer'].stack_ref(0) == 1
assert i.state.stacks['_integer'].stack_ref(1) == 3
assert i.state.stacks['_integer'].stack_ref(2) == 2
assert i.state.stacks['_integer'].stack_ref(3) == 0


i.reset_pysh_state()
print("Testing boolean_yank")
prog = [True, False, True, True, 2, ri.get_instruction('_boolean_yank')]
i.run_push(prog)
if not i.state.size() == 4:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 4." % i.state.size())
assert i.state.stacks['_boolean'].stack_ref(0) == False


i.reset_pysh_state()
print("Testing exec_yankdup")
prog = [3, ri.get_instruction('_exec_yankdup'), 1, 2, 3, ri.get_instruction('_integer_stack_depth')]
i.run_push(prog)
if not i.state.size() == 5:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 5." % i.state.size())
assert i.state.stacks['_integer'].stack_ref(0) == 4
assert i.state.stacks['_integer'].stack_ref(1) == 3
assert i.state.stacks['_integer'].stack_ref(2) == 2
assert i.state.stacks['_integer'].stack_ref(3) == 1
assert i.state.stacks['_integer'].stack_ref(4) == 0


i.reset_pysh_state()
print("Testing integer_yankdup")
prog = [0, 1, 2, 3, 2, ri.get_instruction('_integer_yankdup')]
i.run_push(prog)
if not i.state.size() == 5:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 5." % i.state.size())
assert i.state.stacks['_integer'].stack_ref(0) == 1
assert i.state.stacks['_integer'].stack_ref(1) == 3
assert i.state.stacks['_integer'].stack_ref(2) == 2
assert i.state.stacks['_integer'].stack_ref(3) == 1
assert i.state.stacks['_integer'].stack_ref(4) == 0


i.reset_pysh_state()
print("Testing boolean_yankdup")
prog = [True, False, True, True, 2, ri.get_instruction('_boolean_yankdup')]
i.run_push(prog)
if not i.state.size() == 5:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 5." % i.state.size())
assert i.state.stacks['_boolean'].stack_ref(0) == False
assert i.state.stacks['_boolean'].stack_ref(1) == True
assert i.state.stacks['_boolean'].stack_ref(2) == True
assert i.state.stacks['_boolean'].stack_ref(3) == False


i.reset_pysh_state()
print("Testing exec_shove")
prog = [3, ri.get_instruction('_exec_shove'), 1, 2, 3, 4, 5]
i.run_push(prog)
if not i.state.size() == 5:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 5." % i.state.size())
assert i.state.stacks['_integer'].stack_ref(0) == 5
assert i.state.stacks['_integer'].stack_ref(1) == 1
assert i.state.stacks['_integer'].stack_ref(2) == 4
assert i.state.stacks['_integer'].stack_ref(3) == 3


i.reset_pysh_state()
print("Testing integer_shove")
prog = [1, 2, 3, 4, 5, 3, ri.get_instruction('_integer_shove')]
i.run_push(prog)
if not i.state.size() == 5:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 5." % i.state.size())
assert i.state.stacks['_integer'].stack_ref(0) == 4
assert i.state.stacks['_integer'].stack_ref(1) == 3
assert i.state.stacks['_integer'].stack_ref(2) == 2
assert i.state.stacks['_integer'].stack_ref(3) == 5
assert i.state.stacks['_integer'].stack_ref(4) == 1


i.reset_pysh_state()
print("Testing string_shove")
prog = ["A", "B", "C", "D", "E", 0, ri.get_instruction('_string_shove')]
i.run_push(prog)
if not i.state.size() == 5:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 5." % i.state.size())
assert i.state.stacks['_string'].stack_ref(0) == "E" 
assert i.state.stacks['_string'].stack_ref(1) == "D" 
assert i.state.stacks['_string'].stack_ref(2) == "C" 
assert i.state.stacks['_string'].stack_ref(3) == "B" 
assert i.state.stacks['_string'].stack_ref(4) == "A"


i.reset_pysh_state()
print("Testing string_shove (beyond length of stack)")
prog = ["A", "B", "C", "D", "E", 7, ri.get_instruction('_string_shove')]
i.run_push(prog)
if not i.state.size() == 5:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 5." % i.state.size())
assert i.state.stacks['_string'].stack_ref(0) == "D"
assert i.state.stacks['_string'].stack_ref(1) == "C" 
assert i.state.stacks['_string'].stack_ref(2) == "B" 
assert i.state.stacks['_string'].stack_ref(3) == "A" 
assert i.state.stacks['_string'].stack_ref(4) == "E"


i.reset_pysh_state()
print("Testing exec_empty")
prog = [ri.get_instruction('_exec_empty')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [ri.get_instruction('_exec_empty'), ri.get_instruction('_integer_add')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_boolean'].top_item() == False


i.reset_pysh_state()
print("Testing boolean_empty")
prog = [ri.get_instruction('_boolean_empty'), ri.get_instruction('_boolean_empty')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert i.state.stacks['_boolean'].stack_ref(0) == False
assert i.state.stacks['_boolean'].stack_ref(1) == True


i.reset_pysh_state()
print("Testing integer_add")
prog = [1, 2, ri.get_instruction('_integer_add')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_integer'].top_item() == 3


i.reset_pysh_state()
print("Testing float_add")
prog = [1.1, 2.2, ri.get_instruction('_float_add')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert round(i.state.stacks['_float'].top_item(), 3) == 3.3


i.reset_pysh_state()
print("Testing integer_sub")
prog = [1, 2, ri.get_instruction('_integer_sub')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_integer'].top_item() == -1


i.reset_pysh_state()
print("Testing float_sub")
prog = [1.1, 2.2, ri.get_instruction('_float_sub')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_float'].top_item() == -1.1


i.reset_pysh_state()
print("Testing integer_mult")
prog = [2, 3, ri.get_instruction('_integer_mult')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_integer'].top_item() == 6


i.reset_pysh_state()
print("Testing float_mult")
prog = [1.125, 8.0, ri.get_instruction('_float_mult')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_float'].top_item() == 9.0


i.reset_pysh_state()
print("Testing integer_div")
prog = [10, 3, ri.get_instruction('_integer_div')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_integer'].top_item() == 3

i.reset_pysh_state()
prog = [10, 0, ri.get_instruction('_integer_div')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert i.state.stacks['_integer'].top_item() == 0


i.reset_pysh_state()
print("Testing float_div")
prog = [9.0, 1.125, ri.get_instruction('_float_div')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_float'].top_item() == 8.0

i.reset_pysh_state()
prog = [9.0, 0.0, ri.get_instruction('_float_div')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert i.state.stacks['_float'].top_item() == 0.0


i.reset_pysh_state()
print("Testing integer_mod")
prog = [10, 3, ri.get_instruction('_integer_mod')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_integer'].top_item() == 1


i.reset_pysh_state()
print("Testing float_mod")
prog = [10.1, 3.7, ri.get_instruction('_float_mod')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert round(i.state.stacks['_float'].top_item(), 3) == 2.7


i.reset_pysh_state()
print("Testing integer_lt")
prog = [0, 3, ri.get_instruction('_integer_lt')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [0, -3, ri.get_instruction('_integer_lt')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_boolean'].top_item() == False

i.reset_pysh_state()
prog = [3, 3, ri.get_instruction('_integer_lt')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_boolean'].top_item() == False


i.reset_pysh_state()
print("Testing float_lt")
prog = [0.1, 3.1, ri.get_instruction('_float_lt')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [0.1, -3.1, ri.get_instruction('_float_lt')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_boolean'].top_item() == False


i.reset_pysh_state()
print("Testing integer_lte")
prog = [0, 3, ri.get_instruction('_integer_lte')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [3, 3, ri.get_instruction('_integer_lte')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing float_lte")
prog = [0.1, 3.1, ri.get_instruction('_float_lte')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [3.1, 3.1, ri.get_instruction('_float_lte')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing integer_gt")
prog = [0, 3, ri.get_instruction('_integer_gt')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_boolean'].top_item() == False

i.reset_pysh_state()
prog = [0, -3, ri.get_instruction('_integer_gt')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [3, 3, ri.get_instruction('_integer_gt')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_boolean'].top_item() == False


i.reset_pysh_state()
print("Testing float_gt")
prog = [0.1, 3.1, ri.get_instruction('_float_gt')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_boolean'].top_item() == False

i.reset_pysh_state()
prog = [0.1, -3.1, ri.get_instruction('_float_gt')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing integer_gte")
prog = [0, 3, ri.get_instruction('_integer_gte')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_boolean'].top_item() == False

i.reset_pysh_state()
prog = [3, 3, ri.get_instruction('_integer_gte')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing float_gte")
prog = [0.1, 3.1, ri.get_instruction('_float_gte')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_boolean'].top_item() == False

i.reset_pysh_state()
prog = [3.1, 3.1, ri.get_instruction('_float_gte')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing integer_min")
prog = [0, 3, ri.get_instruction('_integer_min')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_integer'].top_item() == 0

i.reset_pysh_state()
prog = [3, 3, ri.get_instruction('_integer_min')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_integer'].top_item() == 3


i.reset_pysh_state()
print("Testing float_min")
prog = [0.5, 3.5, ri.get_instruction('_float_min')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_float'].top_item() == 0.5

i.reset_pysh_state()
prog = [3.5, 3.5, ri.get_instruction('_float_min')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_float'].top_item() == 3.5


i.reset_pysh_state()
print("Testing integer_max")
prog = [0, 3, ri.get_instruction('_integer_max')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_integer'].top_item() == 3

i.reset_pysh_state()
prog = [3, 3, ri.get_instruction('_integer_max')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_integer'].top_item() == 3


i.reset_pysh_state()
print("Testing float_max")
prog = [0.5, 3.5, ri.get_instruction('_float_max')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_float'].top_item() == 3.5

i.reset_pysh_state()
prog = [3.5, 3.5, ri.get_instruction('_float_max')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_float'].top_item() == 3.5


i.reset_pysh_state()
print("Testing integer_inc")
prog = [2, ri.get_instruction('_integer_inc')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_integer'].top_item() == 3


i.reset_pysh_state()
print("Testing float_inc")
prog = [3.5, ri.get_instruction('_float_inc')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_float'].top_item() == 4.5


i.reset_pysh_state()
print("Testing integer_dec")
prog = [2, ri.get_instruction('_integer_dec')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_integer'].top_item() == 1


i.reset_pysh_state()
print("Testing float_dec")
prog = [3.5, ri.get_instruction('_float_dec')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_float'].top_item() == 2.5


i.reset_pysh_state()
print("Testing float_sin")
prog = [3.5, ri.get_instruction('_float_sin')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert round(i.state.stacks['_float'].top_item(), 3) == -0.351


i.reset_pysh_state()
print("Testing float_cos")
prog = [3.5, ri.get_instruction('_float_cos')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert round(i.state.stacks['_float'].top_item(), 3) == -0.936


i.reset_pysh_state()
print("Testing float_tan")
prog = [3.5, ri.get_instruction('_float_tan')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert round(i.state.stacks['_float'].top_item(), 3) == 0.375


i.reset_pysh_state()
print("Testing integer_from_float")
prog = [3.5, ri.get_instruction('_integer_from_float')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_integer'].top_item() == 3


i.reset_pysh_state()
print("Testing integer_from_boolean")
prog = [True, ri.get_instruction('_integer_from_boolean')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_integer'].top_item() == 1


i.reset_pysh_state()
print("Testing integer_from_string")
prog = ["123", ri.get_instruction('_integer_from_string')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_integer'].top_item() == 123


i.reset_pysh_state()
print("Testing integer_from_char")
prog = [u.Character('7'), ri.get_instruction('_integer_from_char')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_integer'].top_item() == 55


i.reset_pysh_state()
print("Testing float_from_integer")
prog = [7, ri.get_instruction('_float_from_integer')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_float'].top_item() == 7.0


i.reset_pysh_state()
print("Testing foat_from_boolean")
prog = [False, ri.get_instruction('_foat_from_boolean')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_float'].top_item() == 0.0


i.reset_pysh_state()
print("Testing float_from_string")
prog = ['1.23', ri.get_instruction('_float_from_string')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_float'].top_item() == 1.23


i.reset_pysh_state()
print("Testing float_from_char")
prog = [u.Character('7'), ri.get_instruction('_float_from_char')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_float'].top_item() == 55.0


i.reset_pysh_state()
print("Testing string_from_integer")
prog = [5, ri.get_instruction('_string_from_integer')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_string'].top_item() == '5'


i.reset_pysh_state()
print("Testing string_from_float")
prog = [5.5, ri.get_instruction('_string_from_float')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_string'].top_item() == '5.5'


i.reset_pysh_state()
print("Testing string_from_float")
prog = [True, ri.get_instruction('_string_from_boolean')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_string'].top_item() == 'True'

i.reset_pysh_state()
print("Testing string_concat")
prog = ["Hello", "World", ri.get_instruction('_string_concat')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_string'].top_item() == 'HelloWorld'


i.reset_pysh_state()
print("Testing string_head")
prog = ["HelloWorld", 5, ri.get_instruction('_string_head')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_string'].top_item() == 'Hello'


i.reset_pysh_state()
print("Testing string_tail")
prog = ["HelloWorld", 5, ri.get_instruction('_string_tail')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert i.state.stacks['_string'].top_item() == 'World'


i.reset_pysh_state()
print("Testing string_split_at_index")
prog = ["HelloWorld", 5, ri.get_instruction('_string_split_at_index')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert i.state.stacks['_string'].stack_ref(0) == 'World'
assert i.state.stacks['_string'].stack_ref(1) == 'Hello'


i.reset_pysh_state()
print("Testing string_split_at_str")
prog = ["HelloWorld", "o", ri.get_instruction('_string_split_at_str')]
i.run_push(prog)
if not i.state.size() == 3:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 3." % i.state.size())
assert len(i.state.stacks['_string']) == 3
assert i.state.stacks['_string'].top_item() == 'rld'


i.reset_pysh_state()
print("Testing string_split_at_space")
prog = ["Hello World", ri.get_instruction('_string_split_at_space')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_string']) == 2
assert i.state.stacks['_string'].top_item() == 'World'


i.reset_pysh_state()
print("Testing string_length")
prog = ["Hello World", ri.get_instruction('_string_length')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_integer']) == 1
assert i.state.stacks['_integer'].top_item() == 11


i.reset_pysh_state()
print("Testing string_reverse")
prog = ["Hello", ri.get_instruction('_string_reverse')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_string']) == 1
assert i.state.stacks['_string'].top_item() == 'olleH'


i.reset_pysh_state()
print("Testing string_char_at")
prog = ["Hello", 1, ri.get_instruction('_string_char_at')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 1
assert i.state.stacks['_char'].top_item().char == 'e'


i.reset_pysh_state()
print("Testing string_empty_string")
prog = ['', ri.get_instruction('_string_empty_string')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = ['HelloWorld', ri.get_instruction('_string_empty_string')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


i.reset_pysh_state()
print("Testing string_contains")
prog = ['HelloWorld', 'loW', ri.get_instruction('_string_contains')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = ['zzz', 'HelloWorld', ri.get_instruction('_string_contains')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


i.reset_pysh_state()
print("Testing string_replace")
prog = ['Hello World', 'o', '0', ri.get_instruction('_string_replace')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_string']) == 1
assert i.state.stacks['_string'].top_item() == 'Hell0 W0rld'


i.reset_pysh_state()
print("Testing string_from_char")
prog = [u.Character('E'), ri.get_instruction('_string_from_char')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_string']) == 1
assert i.state.stacks['_string'].top_item() == 'E'


i.reset_pysh_state()
print("Testing string_append_char")
prog = ['HelloWorl', u.Character('d'), ri.get_instruction('_string_append_char')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_string']) == 1
assert i.state.stacks['_string'].top_item() == 'HelloWorld'


i.reset_pysh_state()
print("Testing string_first")
prog = ['HelloWorld', ri.get_instruction('_string_first')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 1
assert i.state.stacks['_char'].top_item().char == 'H'


i.reset_pysh_state()
print("Testing string_last")
prog = ['HelloWorld', ri.get_instruction('_string_last')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 1
assert i.state.stacks['_char'].top_item().char == 'd'


i.reset_pysh_state()
print("Testing string_nth")
prog = ['HelloWorld', 5, ri.get_instruction('_string_nth')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 1
assert i.state.stacks['_char'].top_item().char == 'W'


i.reset_pysh_state()
print("Testing string_replace_char")
prog = ['HelloWorld', u.Character('o'), u.Character('Z'), ri.get_instruction('_string_replace_char')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_string']) == 1
assert i.state.stacks['_string'].top_item() == 'HellZWZrld'


i.reset_pysh_state()
print("Testing string_replace_first_char")
prog = ['HelloWorld', u.Character('o'), u.Character('Z'), ri.get_instruction('_string_replace_first_char')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_string']) == 1
assert i.state.stacks['_string'].top_item() == 'HellZWorld'


i.reset_pysh_state()
print("Testing string_remove_char")
prog = ['HelloWorld', u.Character('o'), ri.get_instruction('_string_remove_char')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_string']) == 1
assert i.state.stacks['_string'].top_item() == 'HellWrld'


i.reset_pysh_state()
print("Testing vector instruction (A)")
prog = [u.PushVector([1, 2, 3, 4, 5], int), ri.get_instruction('_vector_integer_rest'), ri.get_instruction('_vector_integer_butlast'), 7, ri.get_instruction('_vector_integer_append'), ri.get_instruction('_exec_do*vector_integer'), [ri.get_instruction('_integer_inc')]]
i.run_push(prog)
if not i.state.size() == 4:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 4." % i.state.size())
assert len(i.state.stacks['_integer']) == 4
assert i.state.stacks['_integer'].top_item() == 8
assert i.state.stacks['_integer'].stack_ref(3) == 3

i.reset_pysh_state()
print("Testing vector instruction (B)")
prog = [u.PushVector([1, 2], int), u.PushVector([3, 4], int), ri.get_instruction('_vector_integer_concat'), 3, ri.get_instruction('_vector_integer_take'), ri.get_instruction('_vector_integer_last')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_integer']) == 1
assert i.state.stacks['_integer'].top_item() == 3

i.reset_pysh_state()
print("Testing vector instruction (C)")
prog = [u.PushVector([1, 2, 3, 4, 5, 6], int), 2, 4, ri.get_instruction('_vector_integer_subvec'), ri.get_instruction('_vector_integer_first')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_integer']) == 1
assert i.state.stacks['_integer'].top_item() == 3

i.reset_pysh_state()
print("Testing vector instruction (D)")
prog = [u.PushVector([1, 2, 3, 4, 5], int), 1, ri.get_instruction('_vector_integer_reverse'), ri.get_instruction('_vector_integer_nth')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_integer']) == 1
assert i.state.stacks['_integer'].top_item() == 4

i.reset_pysh_state()
print("Testing vector instruction (E)")
prog = [u.PushVector([1, 1, 1, 2, 2, 2, 3, 3, 3], int), 3, ri.get_instruction('_vector_integer_remove'), 1, 7, ri.get_instruction('_vector_integer_replace'), 2, 0, ri.get_instruction('_vector_integer_replace'), 2, 0, ri.get_instruction('_vector_integer_replacefirst'), 0, ri.get_instruction('_vector_integer_indexof')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_integer']) == 1
assert i.state.stacks['_integer'].top_item() == 3

i.reset_pysh_state()
print("Testing vector instruction (F)")
prog = [u.PushVector([1, 1, 2, 1, 1], int), 1, 2, ri.get_instruction('_vector_integer_set'), 1, ri.get_instruction('_vector_integer_occurrencesof')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_integer']) == 1
assert i.state.stacks['_integer'].top_item() == 5

i.reset_pysh_state()
print("Testing vector instruction (G)")
prog = [u.PushVector([1, 2, 3, 4], int), ri.get_instruction('_vector_integer_length'), u.PushVector([3, 4, 5], int), ri.get_instruction('_vector_integer_contains'), u.PushVector([1, 2, 3], int), ri.get_instruction('_vector_integer_pushall')]
i.run_push(prog)
if not i.state.size() == 4:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 4." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert len(i.state.stacks['_integer']) == 3
assert i.state.stacks['_integer'].top_item() == 1
assert i.state.stacks['_integer'].stack_ref(2) == 3
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
print("Testing vector instruction (H)")
prog = [u.PushVector([], int), ri.get_instruction('_vector_integer_emptyvector')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True









