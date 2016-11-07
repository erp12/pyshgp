from __future__ import absolute_import, division, print_function, unicode_literals 

import pysh.pysh_interpreter as interp
import pysh.pysh_globals as g
from pysh.instructions import boolean, char, code, common, numbers, string, input_output
from pysh.instructions import registered_instructions as ri


print("Setting up Pysh interpreter...")
i = interp.Pysh_Interpreter()


print("Testing boolean_and")
i.reset_pysh_state()
prog = [True, False, ri.get_instruction_by_name('boolean_and')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False

i.reset_pysh_state()
prog = [True, True, ri.get_instruction_by_name('boolean_and')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True


print("Testing boolean_or")
i.reset_pysh_state()
prog = [True, False, ri.get_instruction_by_name('boolean_or')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [False, False, ri.get_instruction_by_name('boolean_or')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


print("Testing boolean_not")
i.reset_pysh_state()
prog = [True, ri.get_instruction_by_name('boolean_not')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False

i.reset_pysh_state()
prog = [False, ri.get_instruction_by_name('boolean_not')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True


print("Testing boolean_xor")
i.reset_pysh_state()
prog = [True, False, ri.get_instruction_by_name('boolean_xor')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [True, True, ri.get_instruction_by_name('boolean_xor')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


print("Testing boolean_invert_first_then_and")
i.reset_pysh_state()
prog = [True, False, ri.get_instruction_by_name('boolean_invert_first_then_and')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [True, True, ri.get_instruction_by_name('boolean_invert_first_then_and')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


print("Testing boolean_invert_second_then_and")
i.reset_pysh_state()
prog = [False, True, ri.get_instruction_by_name('boolean_invert_second_then_and')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [True, True, ri.get_instruction_by_name('boolean_invert_second_then_and')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


print("Testing boolean_from_integer")
i.reset_pysh_state()
prog = [1, ri.get_instruction_by_name('boolean_from_integer')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [0, ri.get_instruction_by_name('boolean_from_integer')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False

i.reset_pysh_state()
prog = [-5, ri.get_instruction_by_name('boolean_from_integer')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True


print("Testing boolean_from_float")
i.reset_pysh_state()
prog = [1.0, ri.get_instruction_by_name('boolean_from_float')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [0.0, ri.get_instruction_by_name('boolean_from_float')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False

i.reset_pysh_state()
prog = [-2.5, ri.get_instruction_by_name('boolean_from_float')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True


print("Testing char_all_from_string")
i.reset_pysh_state()
prog = ['', ri.get_instruction_by_name('char_all_from_string')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())
assert len(i.state.stacks['_char']) == 0
assert len(i.state.stacks['_string']) == 0

i.reset_pysh_state()
prog = ["pysh", ri.get_instruction_by_name('char_all_from_string')]
i.run_push(prog)
if not i.state.size() == 4:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 4." % i.state.size())
assert len(i.state.stacks['_char']) == 4
assert len(i.state.stacks['_string']) == 0
assert i.state.stacks['_char'].top_item().char == 'p'

i.reset_pysh_state()
prog = ['\n', ri.get_instruction_by_name('char_all_from_string')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 1
assert len(i.state.stacks['_string']) == 0
assert i.state.stacks['_char'].top_item().char == '\n'


print("Testing char_from_integer")
i.reset_pysh_state()
prog = [97, ri.get_instruction_by_name('char_from_integer')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 1
assert len(i.state.stacks['_integer']) == 0
assert i.state.stacks['_char'].top_item().char == 'a'


print("Testing char_from_float")
i.reset_pysh_state()
prog = [97.8, ri.get_instruction_by_name('char_from_float')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 1
assert len(i.state.stacks['_float']) == 0
assert i.state.stacks['_char'].top_item().char == 'a'


print("Testing char_is_letter")
i.reset_pysh_state()
prog = [g.Character('G'), ri.get_instruction_by_name('char_is_letter')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [g.Character('7'), ri.get_instruction_by_name('char_is_letter')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False

i.reset_pysh_state()
prog = [g.Character('\n'), ri.get_instruction_by_name('char_is_letter')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


print("Testing char_is_digit")
i.reset_pysh_state()
prog = [g.Character('G'), ri.get_instruction_by_name('char_is_digit')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False

i.reset_pysh_state()
prog = [g.Character('7'), ri.get_instruction_by_name('char_is_digit')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [g.Character('\n'), ri.get_instruction_by_name('char_is_digit')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


print("Testing char_is_white_space")
i.reset_pysh_state()
prog = [g.Character('G'), ri.get_instruction_by_name('char_is_white_space')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False

i.reset_pysh_state()
prog = [g.Character('7'), ri.get_instruction_by_name('char_is_white_space')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False

i.reset_pysh_state()
prog = [g.Character('\n'), ri.get_instruction_by_name('char_is_white_space')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_char']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing exec_noop")
prog = [ri.get_instruction_by_name('exec_noop')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())
assert len(i.state.stacks['_exec']) == 0


i.reset_pysh_state()
print("Testing code_noop")
prog = [ri.get_instruction_by_name('code_noop')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())
assert len(i.state.stacks['_code']) == 0


i.reset_pysh_state()
print("Testing code_from_boolean")
prog = [True, ri.get_instruction_by_name('code_from_boolean')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert len(i.state.stacks['_boolean']) == 0
assert i.state.stacks['_code'].top_item() == True


i.reset_pysh_state()
print("Testing code_from_float")
prog = [1.5, ri.get_instruction_by_name('code_from_float')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert len(i.state.stacks['_float']) == 0
assert i.state.stacks['_code'].top_item() == 1.5


i.reset_pysh_state()
print("Testing code_from_integer")
prog = [5, ri.get_instruction_by_name('code_from_integer')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert len(i.state.stacks['_integer']) == 0
assert i.state.stacks['_code'].top_item() == 5


i.reset_pysh_state()
print("Testing code_from_exec")
prog = [ri.get_instruction_by_name('code_from_exec'), ri.get_instruction_by_name('exec_noop'),]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert len(i.state.stacks['_exec']) == 0
assert i.state.stacks['_code'].top_item().name == 'exec_noop'


i.reset_pysh_state()
print("Testing code_append")
prog = [5, True, ri.get_instruction_by_name('code_from_integer'), ri.get_instruction_by_name('code_from_boolean'), ri.get_instruction_by_name('code_append'),]
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
prog = [5, ri.get_instruction_by_name('code_from_integer'), ri.get_instruction_by_name('code_atom')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [ri.get_instruction_by_name('code_from_exec'), [5, True], ri.get_instruction_by_name('code_atom')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


i.reset_pysh_state()
print("Testing code_car")
prog = [ri.get_instruction_by_name('code_from_exec'), [5, True], ri.get_instruction_by_name('code_car')]
i.run_push(prog)
if not i.state.size() == 1:
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert i.state.stacks['_code'].top_item() == 5

i.reset_pysh_state()
prog = [ri.get_instruction_by_name('code_from_exec'), 5, ri.get_instruction_by_name('code_car')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert i.state.stacks['_code'].top_item() == 5


i.reset_pysh_state()
print("Testing code_cdr")
prog = [ri.get_instruction_by_name('code_from_exec'), [5, True], ri.get_instruction_by_name('code_cdr')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert i.state.stacks['_code'].top_item() == [True]

i.reset_pysh_state()
prog = [ri.get_instruction_by_name('code_from_exec'), 5, ri.get_instruction_by_name('code_cdr')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert i.state.stacks['_code'].top_item() == []


i.reset_pysh_state()
print("Testing code_do")
prog = [ri.get_instruction_by_name('code_from_exec'), [5, True], ri.get_instruction_by_name('code_do')]
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
prog = [ri.get_instruction_by_name('code_from_exec'), [5, True], ri.get_instruction_by_name('code_do*')]
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
prog = [1, 5, ri.get_instruction_by_name('code_from_exec'), True, ri.get_instruction_by_name('code_do*range')]
i.run_push(prog)
if not i.state.size() == 10:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 10." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert len(i.state.stacks['_boolean']) == 5
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing exec_do*range")
prog = [1, 5, ri.get_instruction_by_name('exec_do*range'), True]
i.run_push(prog)
if not i.state.size() == 10:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 10." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert len(i.state.stacks['_boolean']) == 5
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing code_do*count")
prog = [ri.get_instruction_by_name('code_from_exec'), True, 5, ri.get_instruction_by_name('code_do*count')]
i.run_push(prog)
if not i.state.size() == 10:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 10." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert len(i.state.stacks['_boolean']) == 5
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing exec_do*count")
prog = [5, ri.get_instruction_by_name('exec_do*count'), True]
i.run_push(prog)
if not i.state.size() == 10:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 10." % i.state.size())
assert len(i.state.stacks['_boolean']) == 5
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing code_do*times")
prog = [ri.get_instruction_by_name('code_from_exec'), True, 5, ri.get_instruction_by_name('code_do*times')]
i.run_push(prog)
if not i.state.size() == 5:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 5." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert len(i.state.stacks['_boolean']) == 5
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing exec_do*times")
prog = [5, ri.get_instruction_by_name('exec_do*times'), True]
i.run_push(prog)
if not i.state.size() == 5:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 5." % i.state.size())
assert len(i.state.stacks['_boolean']) == 5
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing exec_while")
prog = [False, True, True, True, ri.get_instruction_by_name('exec_while'), 5]
i.run_push(prog)
if not i.state.size() == 3:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 3." % i.state.size())
assert len(i.state.stacks['_integer']) == 3
assert i.state.stacks['_integer'].top_item() == 5


i.reset_pysh_state()
print("Testing exec_do*while")
prog = [False, True, True, True, ri.get_instruction_by_name('exec_do*while'), 5]
i.run_push(prog)
if not i.state.size() == 4:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 4." % i.state.size())
assert len(i.state.stacks['_integer']) == 4
assert i.state.stacks['_integer'].top_item() == 5


i.reset_pysh_state()
print("Testing code_if")
prog = [True, ri.get_instruction_by_name('code_from_exec'), "Hello", ri.get_instruction_by_name('code_from_exec'), "World", ri.get_instruction_by_name('code_if')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_string']) == 1
assert len(i.state.stacks['_boolean']) == 0
assert len(i.state.stacks['_code']) == 0
assert i.state.stacks['_string'].top_item() == "Hello"

i.reset_pysh_state()
prog = [False, ri.get_instruction_by_name('code_from_exec'), "Hello", ri.get_instruction_by_name('code_from_exec'), "World", ri.get_instruction_by_name('code_if')]
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
prog = [True, ri.get_instruction_by_name('exec_if'), "Hello", "World", ]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_string']) == 1
assert len(i.state.stacks['_boolean']) == 0
assert len(i.state.stacks['_code']) == 0
assert i.state.stacks['_string'].top_item() == "Hello"

i.reset_pysh_state()
prog = [False, ri.get_instruction_by_name('exec_if'), "Hello", "World", ]
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
prog = [True, ri.get_instruction_by_name('exec_when'), "Hello", "World", ]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_string']) == 2
assert len(i.state.stacks['_boolean']) == 0
assert len(i.state.stacks['_code']) == 0
assert i.state.stacks['_string'].top_item() == "World"

i.reset_pysh_state()
prog = [False, ri.get_instruction_by_name('exec_when'), "Hello", "World", ]
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
prog = [ri.get_instruction_by_name('code_from_exec'), [1, 2, ri.get_instruction_by_name('integer_add')], ri.get_instruction_by_name('code_length')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert i.state.stacks['_integer'].top_item() == 3

i.reset_pysh_state()
prog = [ri.get_instruction_by_name('code_from_exec'), 5, ri.get_instruction_by_name('code_length')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert i.state.stacks['_integer'].top_item() == 1


i.reset_pysh_state()
print("Testing code_list")
prog = [ri.get_instruction_by_name('code_from_exec'), 5, ri.get_instruction_by_name('code_from_exec'), 4, ri.get_instruction_by_name('code_list')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert i.state.stacks['_code'].top_item() == [5, 4]


i.reset_pysh_state()
print("Testing code_member")
prog = [ri.get_instruction_by_name('code_from_exec'), 5, ri.get_instruction_by_name('code_from_exec'), [5, 4], ri.get_instruction_by_name('code_member')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == True

i.reset_pysh_state()
prog = [ri.get_instruction_by_name('code_from_exec'), 5, ri.get_instruction_by_name('code_from_exec'), [1, 3], ri.get_instruction_by_name('code_member')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 0
assert len(i.state.stacks['_boolean']) == 1
assert i.state.stacks['_boolean'].top_item() == False


i.reset_pysh_state()
print("Testing code_nth")
prog = [ri.get_instruction_by_name('code_from_exec'), [1, 2, 3, 4], 1, ri.get_instruction_by_name('code_nth')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert len(i.state.stacks['_integer']) == 0
assert i.state.stacks['_code'].top_item() == 2

i.reset_pysh_state()
prog = [ri.get_instruction_by_name('code_from_exec'), [1, 2, 3, 4], 5, ri.get_instruction_by_name('code_nth')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert len(i.state.stacks['_integer']) == 0
assert i.state.stacks['_code'].top_item() == 2


i.reset_pysh_state()
print("Testing code_nthcdr")
prog = [ri.get_instruction_by_name('code_from_exec'), [1, 2, 3, 4], 1, ri.get_instruction_by_name('code_nthcdr')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert len(i.state.stacks['_integer']) == 0
assert i.state.stacks['_code'].top_item() == [1, 3, 4]

i.reset_pysh_state()
prog = [ri.get_instruction_by_name('code_from_exec'), [1, 2, 3, 4], 5, ri.get_instruction_by_name('code_nthcdr')]
i.run_push(prog)
if not i.state.size() == 1:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 1." % i.state.size())
assert len(i.state.stacks['_code']) == 1
assert len(i.state.stacks['_integer']) == 0
assert i.state.stacks['_code'].top_item() == [1, 3, 4]


i.reset_pysh_state()
print("Testing exec_pop")
prog = [ri.get_instruction_by_name('exec_pop'), ri.get_instruction_by_name('integer_stack_depth')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())
assert len(i.state.stacks['_integer']) == 0


i.reset_pysh_state()
print("Testing integer_pop")
prog = [5, ri.get_instruction_by_name('integer_pop')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())
assert len(i.state.stacks['_integer']) == 0


i.reset_pysh_state()
print("Testing float_pop")
prog = [5.1, ri.get_instruction_by_name('float_pop')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())
assert len(i.state.stacks['_float']) == 0


i.reset_pysh_state()
print("Testing code_pop")
prog = [ri.get_instruction_by_name('code_from_exec'), [True, 5], ri.get_instruction_by_name('code_pop')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())
assert len(i.state.stacks['_code']) == 0


i.reset_pysh_state()
print("Testing boolean_pop")
prog = [True, ri.get_instruction_by_name('boolean_pop')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())
assert len(i.state.stacks['_boolean']) == 0


i.reset_pysh_state()
print("Testing string_pop")
prog = ["HelloWorld", ri.get_instruction_by_name('string_pop')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())
assert len(i.state.stacks['_string']) == 0


i.reset_pysh_state()
print("Testing char_pop")
prog = [g.Character('G'), ri.get_instruction_by_name('char_pop')]
i.run_push(prog)
if not i.state.size() == 0:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 0." % i.state.size())
assert len(i.state.stacks['_char']) == 0

i.reset_pysh_state()
print("Testing exec_dup")
prog = [ri.get_instruction_by_name('exec_dup'), 5]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_integer']) == 2
assert i.state.stacks['_integer'].top_item() == 5


i.reset_pysh_state()
print("Testing integer_dup")
prog = [5, ri.get_instruction_by_name('integer_dup')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_integer']) == 2
assert i.state.stacks['_integer'].top_item() == 5


i.reset_pysh_state()
print("Testing float_dup")
prog = [5.1, ri.get_instruction_by_name('float_dup')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_float']) == 2
assert i.state.stacks['_float'].top_item() == 5.1


i.reset_pysh_state()
print("Testing code_dup")
prog = [ri.get_instruction_by_name('code_from_exec'), True, ri.get_instruction_by_name('code_dup')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_code']) == 2
assert i.state.stacks['_code'].top_item() == True


i.reset_pysh_state()
print("Testing boolean_dup")
prog = [True, ri.get_instruction_by_name('boolean_dup')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_boolean']) == 2
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing string_dup")
prog = ["HelloWorld", ri.get_instruction_by_name('string_dup')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_string']) == 2
assert i.state.stacks['_string'].top_item() == "HelloWorld"


i.reset_pysh_state()
print("Testing char_dup")
prog = [g.Character('G'), ri.get_instruction_by_name('char_dup')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_char']) == 2
assert i.state.stacks['_char'].top_item().char == "G"


i.reset_pysh_state()
print("Testing exec_swap")
prog = [ri.get_instruction_by_name('exec_swap'), True, False]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_boolean']) == 2
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing integer_swap")
prog = [1, 2, ri.get_instruction_by_name('integer_swap')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_integer']) == 2
assert i.state.stacks['_integer'].top_item() == 1


i.reset_pysh_state()
print("Testing float_swap")
prog = [1.1, 2.1, ri.get_instruction_by_name('float_swap')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_float']) == 2
assert i.state.stacks['_float'].top_item() == 1.1


i.reset_pysh_state()
print("Testing code_swap")
prog = [ri.get_instruction_by_name('code_from_exec'), True, ri.get_instruction_by_name('code_from_exec'), False, ri.get_instruction_by_name('code_swap')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_code']) == 2
assert i.state.stacks['_code'].top_item() == True


i.reset_pysh_state()
print("Testing boolean_swap")
prog = [True, False, ri.get_instruction_by_name('boolean_swap')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_boolean']) == 2
assert i.state.stacks['_boolean'].top_item() == True


i.reset_pysh_state()
print("Testing string_swap")
prog = ["HelloWorld", "HelloWorld", ri.get_instruction_by_name('string_swap')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_string']) == 2
assert i.state.stacks['_string'].top_item() == "HelloWorld"


i.reset_pysh_state()
print("Testing char_swap")
prog = [g.Character('A'), g.Character('B'), ri.get_instruction_by_name('char_swap')]
i.run_push(prog)
if not i.state.size() == 2:
    i.state.pretty_print()
    raise Exception("State has %r items. Should be 2." % i.state.size())
assert len(i.state.stacks['_char']) == 2
assert i.state.stacks['_char'].top_item().char == "A"










