from __future__ import absolute_import, division, print_function, unicode_literals

import pyshgp.utils as u
import pyshgp.push.interpreter as interp
import pyshgp.push.instruction as instr
import pyshgp.push.instructions.registered_instructions as ri
from pyshgp.push.instructions import *


def dict_matches_state(interpreter, state_dict):
    i = 0
    for k in state_dict.keys():
        if not state_dict[k] == interpreter.state[k]:
            return False
        i += len(state_dict[k])
    if i == len(interpreter.state):
        return True
    else:
        return False


def run_test(test_info, print_test=False):
    interpreter = interp.PushInterpreter()
    interpreter.state.from_dict(test_info[0])

    instruction = test_info[1]
    if not isinstance(test_info[1], instr.PyshInstruction):
        instruction = ri.get_instruction(test_info[1])

    if print_test:
        print(instruction.name)
        print("Before:")
        interpreter.state.pretty_print()

    if type(test_info[2]) == dict:
        interpreter.execute_instruction(instruction)
        if print_test:
            print("After:")
            interpreter.state.pretty_print()
            print()
        return dict_matches_state(interpreter, test_info[2])
    else:
        try:
            interpreter.execute_instruction(instruction)
        except Exception as e:
            if print_test:
                print("Raises error: ", type(e))
                print()
            if isinstance(e, test_info[2]):
                return True
            else:
                return False
