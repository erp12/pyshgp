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























