# -*- coding: utf-8 -*-
"""
Created on July 24, 2016

@author: Eddie
"""

from ... import constants as c
from .. import instruction as instr


def print_newline(state):
    """Appends a newline to the stdout string in the output field.
    """
    if len(state.stdout) + 1 > c.max_string_length:
        return
    state.stdout += '\n'


print_newline_instr = instr.PyshInstruction('_print_newline',
                                            print_newline,
                                            stack_types=['_print'])


def printer(pysh_type):
    """Returns a function that takes a state and prints the top item of the
    appropriate stack of the state.
    """
    def prnt(state):
        if len(state[pysh_type]) < 1:
            return
        top_thing = state[pysh_type].ref(0)
        top_thing_str = str(top_thing)
        if len(state.stdout) + len(top_thing_str) > c.max_string_length:
            return
        state[pysh_type].pop()
        state.stdout += top_thing_str
    instruction = instr.PyshInstruction('_print' + pysh_type, prnt,
                                        stack_types=['_print', pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 1
    return instruction


print_exec_instr = printer('_exec')
print_integer_instr = printer('_integer')
print_float_instr = printer('_float')
print_code_instr = printer('_code')
print_boolean_instr = printer('_boolean')
# <instr_open>
# <instr_name>print_exec
# <instr_desc>Prints the top item of the exec stack to the string on the output stack.
# <instr_close>
# <instr_open>
# <instr_name>print_integer
# <instr_desc>Prints the top integer to the string on the output stack.
# <instr_close>
# <instr_open>
# <instr_name>print_float
# <instr_desc>Prints the top float to the string on the output stack.
# <instr_close>
# <instr_open>
# <instr_name>print_code
# <instr_desc>Prints the top item on the code code stack to the string on the output stack.
# <instr_close>
# <instr_open>
# <instr_name>print_boolean
# <instr_desc>Prints the top boolean to the string on the output stack.
# <instr_close>
# <instr_open>
# <instr_name>print_string
# <instr_desc>Prints the top string to the string on the output stack.
# <instr_close>
