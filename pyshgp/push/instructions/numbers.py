# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 14:54:49 2016

@author: Eddie
"""

import math

from ... import utils as u
from ..instruction import Instruction


def adder(pysh_type):
    '''
    Returns an instruction that pushes the sum of the top two items.
    '''
    def add(state):
        if len(state[pysh_type]) > 1:
            new_num = state[pysh_type].ref(1) + state[pysh_type].ref(0)
            new_num = u.keep_number_reasonable(new_num)
            state[pysh_type].pop()
            state[pysh_type].pop()
            state[pysh_type].push(new_num)
    instruction = Instruction(pysh_type + '_add',
                              add,
                              stack_types=[pysh_type])
    return instruction


I_add_integer = adder('_integer')
I_add_float = adder('_float')
# <instr_open>
# <instr_name>integer_add
# <instr_desc>Pushes the result of adding the top two integers.
# <instr_close>
# <instr_open>
# <instr_name>float_add
# <instr_desc>Pushes the result of adding the top two floats.
# <instr_close>


def subtracter(pysh_type):
    '''
    Returns an instruction that pushes the difference  of the top two items.
    '''
    def sub(state):
        if len(state[pysh_type]) > 1:
            new_num = state[pysh_type].ref(1) - state[pysh_type].ref(0)
            new_num = u.keep_number_reasonable(new_num)
            state[pysh_type].pop()
            state[pysh_type].pop()
            state[pysh_type].push(new_num)
    instruction = Instruction(pysh_type + '_sub',
                              sub,
                              stack_types=[pysh_type])
    return instruction


I_sub_integer = subtracter('_integer')
I_sub_float = subtracter('_float')
# <instr_open>
# <instr_name>integer_sub
# <instr_desc>Pushes the difference of the top two integers.
# <instr_close>
# <instr_open>
# <instr_name>float_sub
# <instr_desc>Pushes the difference of the top two floats.
# <instr_close>


def multiplier(pysh_type):
    '''
    Returns an instruction that pushes the product  of the top two items.
    '''
    def mult(state):
        if len(state[pysh_type]) > 1:
            new_num = state[pysh_type].ref(1) * state[pysh_type].ref(0)
            new_num = u.keep_number_reasonable(new_num)
            state[pysh_type].pop()
            state[pysh_type].pop()
            state[pysh_type].push(new_num)
    instruction = Instruction(pysh_type + '_mult',
                              mult,
                              stack_types=[pysh_type])
    return instruction


I_mult_integer = multiplier('_integer')
I_mult_float = multiplier('_float')
# <instr_open>
# <instr_name>integer_mult
# <instr_desc>Pushes the product of the top two integers.
# <instr_close>
# <instr_open>
# <instr_name>float_mult
# <instr_desc>Pushes the product of the top two floats.
# <instr_close>


def divider(pysh_type):
    '''
    Returns a function that pushes the quotient of the top two items.
    Retirms previous state if the denominator would be zero.
    '''
    def div(state):
        if len(state[pysh_type]) > 1:
            if state[pysh_type].ref(0) != 0:
                new_num = None
                new_num = state[pysh_type].ref(1) / state[pysh_type].ref(0)
                if pysh_type == '_integer':
                    new_num = int(new_num)
                new_num = u.keep_number_reasonable(new_num)
                state[pysh_type].pop()
                state[pysh_type].pop()
                state[pysh_type].push(new_num)
    instruction = Instruction(pysh_type + '_div',
                              div,
                              stack_types=[pysh_type])
    return instruction


I_div_integer = divider('_integer')
I_div_float = divider('_float')
# <instr_open>
# <instr_name>integer_div
# <instr_desc>Pushes the quotient of the top two integers.
# <instr_close>
# <instr_open>
# <instr_name>float_div
# <instr_desc>Pushes the quotient of the top two floats.
# <instr_close>


def modder(pysh_type):
    '''
    Returns a function that pushes the modulus of the top two items. Does
    nothing if the denominator would be zero.
    '''
    def mod(state):
        if len(state[pysh_type]) > 1:
            if state[pysh_type].ref(0) != 0:
                new_num = state[pysh_type].ref(1) % state[pysh_type].ref(0)
                new_num = u.keep_number_reasonable(new_num)
                state[pysh_type].pop()
                state[pysh_type].pop()
                state[pysh_type].push(new_num)
    instruction = Instruction(pysh_type + '_mod',
                              mod,
                              stack_types=[pysh_type])
    return instruction


I_mod_integer = modder('_integer')
I_mod_float = modder('_float')
# <instr_open>
# <instr_name>integer_mod
# <instr_desc>Pushes the result of the second integer modulous the first integer.
# <instr_close>
# <instr_open>
# <instr_name>float_mod
# <instr_desc>Pushes the result of the second float modulous the first float.
# <instr_close>


def less_than(pysh_type):
    '''
    Returns a function that pushes TRUE to the bool stack if the
    second item on the stack is less than the first item.
    '''
    def lt(state):
        if len(state[pysh_type]) > 1:
            new_bool = state[pysh_type].ref(1) < state[pysh_type].ref(0)
            state[pysh_type].pop()
            state[pysh_type].pop()
            state['_boolean'].push(new_bool)
    instruction = Instruction(pysh_type + '_lt',
                              lt,
                              stack_types=[pysh_type, '_boolean'])
    return instruction


I_lt_integer = less_than('_integer')
I_lt_float = less_than('_float')
# <instr_open>
# <instr_name>integer_lt
# <instr_desc>Push a boolean based on if the second integer is less than the top integer.
# <instr_close>
# <instr_open>
# <instr_name>float_lt
# <instr_desc>Push a boolean based on if the second float is less than the top float.
# <instr_close>


def less_than_equal(pysh_type):
    '''
    Returns a function that pushes TRUE to the bool stack if the
    second item on the stack is less than, or equal to, the first item.
    '''
    def lte(state):
        if len(state[pysh_type]) > 1:
            new_bool = state[pysh_type].ref(1) <= state[pysh_type].ref(0)
            state[pysh_type].pop()
            state[pysh_type].pop()
            state['_boolean'].push(new_bool)
    instruction = Instruction(pysh_type + '_lte',
                              lte,
                              stack_types=[pysh_type, '_boolean'])
    return instruction


I_lte_integer = less_than_equal('_integer')
I_lte_float = less_than_equal('_float')
# <instr_open>
# <instr_name>integer_lte
# <instr_desc>Push a boolean based on if the second integer is less than, or equal to, the top integer.
# <instr_close>
# <instr_open>
# <instr_name>float_lte
# <instr_desc>Push a boolean based on if the second float is less than, or equal to, the top float.
# <instr_close>


def greater_than(pysh_type):
    '''
    Returns a function that pushes TRUE to the bool stack if the
    second item on the stack is greater than the first item.
    '''
    def gt(state):
        if len(state[pysh_type]) > 1:
            new_bool = state[pysh_type].ref(1) > state[pysh_type].ref(0)
            state[pysh_type].pop()
            state[pysh_type].pop()
            state['_boolean'].push(new_bool)
    instruction = Instruction(pysh_type + '_gt',
                              gt,
                              stack_types=[pysh_type, '_boolean'])
    return instruction


I_gt_integer = greater_than('_integer')
I_gt_float = greater_than('_float')
# <instr_open>
# <instr_name>integer_gt
# <instr_desc>Push a boolean based on if the second integer is greater than the top integer.
# <instr_close>
# <instr_open>
# <instr_name>float_gt
# <instr_desc>Push a boolean based on if the second float is greater than the top float.
# <instr_close>


def greater_than_equal(pysh_type):
    '''
    Returns a function that pushes TRUE to the bool stack if the
    second item on the stack is greater than, or equal, the first item.
    '''
    def gte(state):
        if len(state[pysh_type]) > 1:
            new_bool = state[pysh_type].ref(1) >= state[pysh_type].ref(0)
            state[pysh_type].pop()
            state[pysh_type].pop()
            state['_boolean'].push(new_bool)
    instruction = Instruction(pysh_type + '_gte',
                              gte,
                              stack_types=[pysh_type, '_boolean'])
    return instruction


I_gte_integer = greater_than_equal('_integer')
I_gte_float = greater_than_equal('_float')
# <instr_open>
# <instr_name>integer_gte
# <instr_desc>Push a boolean based on if the second integer is greater than, or equal to, the top integer.
# <instr_close>
# <instr_open>
# <instr_name>float_gte
# <instr_desc>Push a boolean based on if the second float is greater than, or equal to, the top float.
# <instr_close>


def minner(pysh_type):
    '''
    Returns a function that pushes the minimum of the top two items.
    '''
    def min_pysh(state):
        if len(state[pysh_type]) > 1:
            new_num = min(state[pysh_type].ref(1), state[pysh_type].ref(0))
            state[pysh_type].pop()
            state[pysh_type].pop()
            state[pysh_type].push(new_num)
    instruction = Instruction(pysh_type + '_min',
                              min_pysh,
                              stack_types=[pysh_type])
    return instruction


I_min_integer = minner('_integer')
I_min_float = minner('_float')
# <instr_open>
# <instr_name>integer_min
# <instr_desc>Pushes the minimum of the top two integers.
# <instr_close>
# <instr_open>
# <instr_name>float_min
# <instr_desc>Pushes the minimum of the top two floats.
# <instr_close>


def maxer(pysh_type):
    '''
    Returns a function that pushes the maximum of the top two items.
    '''
    def max_pysh(state):
        if len(state[pysh_type]) > 1:
            new_num = max(state[pysh_type].ref(1), state[pysh_type].ref(0))
            state[pysh_type].pop()
            state[pysh_type].pop()
            state[pysh_type].push(new_num)
    instruction = Instruction(pysh_type + '_max',
                              max_pysh,
                              stack_types=[pysh_type])
    return instruction


I_max_integer = maxer('_integer')
I_max_float = maxer('_float')
# <instr_open>
# <instr_name>integer_max
# <instr_desc>Pushes the maximum of the top two integers.
# <instr_close>
# <instr_open>
# <instr_name>float_max
# <instr_desc>Pushes the maximum of the top two floats.
# <instr_close>


def incrementer(pysh_type):
    '''
    Returns a function that increments the first item on the stack.
    '''
    def inc(state):
        if len(state[pysh_type]) > 0:
            new_num = state[pysh_type].ref(0) + 1
            state[pysh_type].pop()
            state[pysh_type].push(new_num)
    instruction = Instruction(pysh_type + '_inc',
                              inc,
                              stack_types=[pysh_type])
    return instruction


I_inc_integer = incrementer('_integer')
I_inc_float = incrementer('_float')
# <instr_open>
# <instr_name>integer_inc
# <instr_desc>Pushes the result of incrementing the top integer by 1.
# <instr_close>
# <instr_open>
# <instr_name>float_inc
# <instr_desc>Pushes the result of incrementing the top float by 1.0.
# <instr_close>


def decrementer(pysh_type):
    '''
    Returns a function that increments the first item on the stack.
    '''
    def dec(state):
        if len(state[pysh_type]) > 0:
            new_num = state[pysh_type].ref(0) - 1
            state[pysh_type].pop()
            state[pysh_type].push(new_num)
    instruction = Instruction(pysh_type + '_dec',
                              dec,
                              stack_types=[pysh_type])
    return instruction


I_dec_integer = decrementer('_integer')
I_dec_float = decrementer('_float')
# <instr_open>
# <instr_name>integer_dec
# <instr_desc>Pushes the result of decrementing the top integer by 1.
# <instr_close>
# <instr_open>
# <instr_name>float_dec
# <instr_desc>Pushes the result of decrementing the top float by 1.0.
# <instr_close>


def float_sin(state):
    """Function for the sin Push instruction.
    """
    if len(state['_float']) > 0:
        new_float = math.sin(state['_float'].ref(0))
        state['_float'].pop()
        state['_float'].push(new_float)


I_float_sin = Instruction('_float_sin',
                          float_sin,
                          stack_types=['_float'])
# <instr_open>
# <instr_name>float_sin
# <instr_desc>Puses the sin of the top float.
# <instr_close>


def float_cos(state):
    """Function for the cos Push instruction.
    """
    if len(state['_float']) > 0:
        new_float = math.cos(state['_float'].ref(0))
        state['_float'].pop()
        state['_float'].push(new_float)


I_float_cos = Instruction('_float_cos',
                          float_cos,
                          stack_types=['_float'])
# <instr_open>
# <instr_name>float_cos
# <instr_desc>Pushes the cos of the top float.
# <instr_close>


def float_tan(state):
    """Function for the tan Push instruction.
    """
    if len(state['_float']) > 0:
        new_float = math.tan(state['_float'].ref(0))
        state['_float'].pop()
        state['_float'].push(new_float)


I_float_tan = Instruction('_float_tan',
                          float_tan,
                          stack_types=['_float'])
# <instr_open>
# <instr_name>float_tan
# <instr_desc>Pushes the tangent of the top float.
# <instr_close>


def integer_from_float(state):
    if len(state['_float']) > 0:
        new_int = int(state['_float'].ref(0))
        state['_float'].pop()
        state['_integer'].push(new_int)


I_int_from_float = Instruction('_integer_from_float',
                               integer_from_float,
                               stack_types=['_integer', '_float'])
# <instr_open>
# <instr_name>integer_from_float
# <instr_desc>Pushes the top float cast to an integer.
# <instr_close>


def integer_from_boolean(state):
    if len(state['_boolean']) > 0:
        new_int = int(state['_boolean'].ref(0))
        state['_boolean'].pop()
        state['_integer'].push(new_int)


I_int_from_boolean = Instruction('_integer_from_boolean',
                                 integer_from_boolean,
                                 stack_types=['_integer', '_boolean'])
# <instr_open>
# <instr_name>integer_from_boolean
# <instr_desc>Pushes the top boolean cast to an integer.
# <instr_close>


def integer_from_string(state):
    if len(state['_string']) > 0:
        new_int = None
        try:
            new_int = int(state['_string'].ref(0))
        except ValueError:
            return
        state['_string'].pop()
        state['_integer'].push(new_int)


I_int_from_string = Instruction('_integer_from_string',
                                integer_from_string,
                                stack_types=['_integer', '_string'])
# <instr_open>
# <instr_name>integer_from_string
# <instr_desc>Pushes the top string cast to an integer.
# <instr_close>


def integer_from_char(state):
    if len(state['_char']) > 0:
        item = ord(state['_char'].ref(0).char)
        state['_char'].pop()
        state['_integer'].push(item)


I_integer_from_char = Instruction('_integer_from_char',
                                  integer_from_char,
                                  stack_types=['_integer', '_char'])
# <instr_open>
# <instr_name>integer_from_char
# <instr_desc>Pushes the top `char` cast to an `integer`.
# <instr_close>


def float_from_integer(state):
    if len(state['_integer']) > 0:
        new_float = float(state['_integer'].ref(0))
        state['_integer'].pop()
        state['_float'].push(new_float)


I_float_from_int = Instruction('_float_from_integer',
                               float_from_integer,
                               stack_types=['_float', '_integer'])
# <instr_open>
# <instr_name>float_from_integer
# <instr_desc>Push the top integer cast to a float.
# <instr_close>


def float_from_boolean(state):
    if len(state['_boolean']) > 0:
        new_float = float(state['_boolean'].ref(0))
        state['_boolean'].pop()
        state['_float'].push(new_float)


I_float_from_bool = Instruction('_float_from_boolean',
                                float_from_boolean,
                                stack_types=['_float', '_boolean'])
# <instr_open>
# <instr_name>foat_from_boolean
# <instr_desc>Pushes top boolean cast to a float.
# <instr_close>


def float_from_string(state):
    if len(state['_string']) > 0:
        new_float = None
        try:
            new_float = float(state['_string'].ref(0))
        except ValueError:
            return
        state['_string'].pop()
        state['_float'].push(new_float)


I_float_from_string = Instruction('_float_from_string',
                                  float_from_string,
                                  stack_types=['_float', '_string'])
# <instr_open>
# <instr_name>float_from_string
# <instr_desc>Pushes the top string cast to an float.
# <instr_close>


def float_from_char(state):
    if len(state['_char']) > 0:
        item = float(ord(state['_char'].ref(0).char))
        state['_char'].pop()
        state['_float'].push(item)


I_float_from_char = Instruction('_float_from_char',
                                float_from_char,
                                stack_types=['_float', '_char'])
# <instr_open>
# <instr_name>float_from_char
# <instr_desc>Pushes the top `char` cast to an `float`.
# <instr_close>
