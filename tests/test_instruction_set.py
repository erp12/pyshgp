from __future__ import absolute_import, division, print_function, unicode_literals 

import pysh.pysh_interpreter as interp
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
assert i.state.stacks['_boolean'].top_item() == False






