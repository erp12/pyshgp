# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 14:54:49 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import math

from .. import pysh_state
from .. import instruction as instr
from .. import utils as u

from . import registered_instructions


def adder(pysh_type):
    '''
    Returns an instruction that pushes the sum of the top two items.
    '''
    def add(state):
        if len(state.stacks[pysh_type])>1:
            new_num = state.stacks[pysh_type].stack_ref(1) + state.stacks[pysh_type].stack_ref(0)
            new_num = u.keep_number_reasonable(new_num)
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].push_item(new_num)
    instruction = instr.Pysh_Instruction(pysh_type[1:] + '_add',
                                                    add,
                                                    stack_types = [pysh_type])
    return instruction
registered_instructions.register_instruction(adder('_integer'))
registered_instructions.register_instruction(adder('_float'))
#<instr_open>
#<instr_name>integer_add
#<instr_desc>
#<instr_close>
#<instr_open>
#<instr_name>float_add
#<instr_desc>
#<instr_close>


def subtracter(pysh_type):
    '''
    Returns an instruction that pushes the difference  of the top two items.
    '''
    def sub(state):
        if len(state.stacks[pysh_type])>1:
            new_num = state.stacks[pysh_type].stack_ref(1) - state.stacks[pysh_type].stack_ref(0)
            new_num = u.keep_number_reasonable(new_num)
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].push_item(new_num)
    instruction = instr.Pysh_Instruction(pysh_type[1:] + '_sub',
                                                    sub,
                                                    stack_types = [pysh_type])
    return instruction
registered_instructions.register_instruction(subtracter('_integer'))
registered_instructions.register_instruction(subtracter('_float'))
#<instr_open>
#<instr_name>integer_sub
#<instr_desc>
#<instr_close>
#<instr_open>
#<instr_name>float_sub
#<instr_desc>
#<instr_close>


def multiplier(pysh_type):
    '''
    Returns an instruction that pushes the product  of the top two items.
    '''
    def mult(state):
        if len(state.stacks[pysh_type])>1:
            new_num = state.stacks[pysh_type].stack_ref(1) * state.stacks[pysh_type].stack_ref(0)
            new_num = u.keep_number_reasonable(new_num)
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].push_item(new_num)
    instruction = instr.Pysh_Instruction(pysh_type[1:] + '_mult',
                                                    mult,
                                                    stack_types = [pysh_type])
    return instruction
registered_instructions.register_instruction(multiplier('_integer'))
registered_instructions.register_instruction(multiplier('_float'))
#<instr_open>
#<instr_name>integer_mult
#<instr_desc>
#<instr_close>
#<instr_open>
#<instr_name>float_mult
#<instr_desc>
#<instr_close>


def divider(pysh_type):
    '''
    Returns a function that pushes the quotient of the top two items.
    Retirms previous state if the denominator would be zero.
    '''
    def div(state):
        if len(state.stacks[pysh_type])>1:
            if state.stacks[pysh_type].stack_ref(0) != 0:
                new_num = state.stacks[pysh_type].stack_ref(1) // state.stacks[pysh_type].stack_ref(0)
                new_num = u.keep_number_reasonable(new_num)
                state.stacks[pysh_type].pop_item()
                state.stacks[pysh_type].pop_item()
                state.stacks[pysh_type].push_item(new_num)
    instruction = instr.Pysh_Instruction(pysh_type[1:] + '_div',
                                                    div,
                                                    stack_types = [pysh_type])
    return instruction
registered_instructions.register_instruction(divider('_integer'))
registered_instructions.register_instruction(divider('_float'))
#<instr_open>
#<instr_name>integer_div
#<instr_desc>
#<instr_close>
#<instr_open>
#<instr_name>float_div
#<instr_desc>
#<instr_close>


def modder(pysh_type):
    '''
    Returns a function that pushes the modulus of the top two items. Does 
    nothing if the denominator would be zero.
    '''
    def mod(state):
        if len(state.stacks[pysh_type])>1:
            if state.stacks[pysh_type].stack_ref(0) != 0:
                new_num = state.stacks[pysh_type].stack_ref(1) % state.stacks[pysh_type].stack_ref(0)
                new_num = u.keep_number_reasonable(new_num)
                state.stacks[pysh_type].pop_item()
                state.stacks[pysh_type].pop_item()
                state.stacks[pysh_type].push_item(new_num)
    instruction = instr.Pysh_Instruction(pysh_type[1:] + '_mod',
                                                    mod,
                                                    stack_types = [pysh_type])
    return instruction
registered_instructions.register_instruction(modder('_integer'))
registered_instructions.register_instruction(modder('_float'))
#<instr_open>
#<instr_name>integer_mod
#<instr_desc>
#<instr_close>
#<instr_open>
#<instr_name>float_mod
#<instr_desc>
#<instr_close>


def less_than(pysh_type):
    '''
    Returns a function that pushes TRUE to the bool stack if the 
    second item on the stack is less than the first item.
    '''
    def lt(state):
        if len(state.stacks[pysh_type])>1:
            new_bool = state.stacks[pysh_type].stack_ref(1) < state.stacks[pysh_type].stack_ref(0)
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].pop_item()
            state.stacks['_boolean'].push_item(new_bool)
    instruction = instr.Pysh_Instruction(pysh_type[1:] + '_lt',
                                                    lt,
                                                    stack_types = [pysh_type, '_boolean'])
    return instruction
registered_instructions.register_instruction(less_than('_integer'))
registered_instructions.register_instruction(less_than('_float'))
#<instr_open>
#<instr_name>integer_lt
#<instr_desc>
#<instr_close>
#<instr_open>
#<instr_name>float_lt
#<instr_desc>
#<instr_close>


def less_than_equal(pysh_type):
    '''
    Returns a function that pushes TRUE to the bool stack if the 
    second item on the stack is less than, or equal to, the first item.
    '''
    def lte(state):
        if len(state.stacks[pysh_type])>1:
            new_bool = state.stacks[pysh_type].stack_ref(1) <= state.stacks[pysh_type].stack_ref(0)
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].pop_item()
            state.stacks['_boolean'].push_item(new_bool)
    instruction = instr.Pysh_Instruction(pysh_type[1:] + '_lte',
                                                    lte,
                                                    stack_types = [pysh_type, '_boolean'])
    return instruction
registered_instructions.register_instruction(less_than_equal('_integer'))
registered_instructions.register_instruction(less_than_equal('_float'))
#<instr_open>
#<instr_name>integer_lte
#<instr_desc>
#<instr_close>
#<instr_open>
#<instr_name>float_lte
#<instr_desc>
#<instr_close>


def greater_than(pysh_type):
    '''
    Returns a function that pushes TRUE to the bool stack if the 
    second item on the stack is greater than the first item.
    '''
    def gt(state):
        if len(state.stacks[pysh_type])>1:
            new_bool = state.stacks[pysh_type].stack_ref(1) > state.stacks[pysh_type].stack_ref(0)
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].pop_item()
            state.stacks['_boolean'].push_item(new_bool)
    instruction = instr.Pysh_Instruction(pysh_type[1:] + '_gt',
                                                    gt,
                                                    stack_types = [pysh_type, '_boolean'])
    return instruction
registered_instructions.register_instruction(greater_than('_integer'))
registered_instructions.register_instruction(greater_than('_float'))
#<instr_open>
#<instr_name>integer_gt
#<instr_desc>
#<instr_close>
#<instr_open>
#<instr_name>float_gt
#<instr_desc>
#<instr_close>


def greater_than_equal(pysh_type):
    '''
    Returns a function that pushes TRUE to the bool stack if the 
    second item on the stack is greater than, or equal, the first item.
    '''
    def gte(state):
        if len(state.stacks[pysh_type])>1:
            new_bool = state.stacks[pysh_type].stack_ref(1) > state.stacks[pysh_type].stack_ref(0)
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].pop_item()
            state.stacks['_boolean'].push_item(new_bool)
    instruction = instr.Pysh_Instruction(pysh_type[1:] + '_gte',
                                                    gte,
                                                    stack_types = [pysh_type, '_boolean'])
    return instruction
registered_instructions.register_instruction(greater_than_equal('_integer'))
registered_instructions.register_instruction(greater_than_equal('_float'))
#<instr_open>
#<instr_name>integer_gte
#<instr_desc>
#<instr_close>
#<instr_open>
#<instr_name>float_gte
#<instr_desc>
#<instr_close>


def minner(pysh_type):
    '''
    Returns a function that pushes the minimum of the top two items.
    '''
    def min_pysh(state):
        if len(state.stacks[pysh_type])>1:
            new_num = min(state.stacks[pysh_type].stack_ref(1), state.stacks[pysh_type].stack_ref(0))
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].push_item(new_num)
    instruction = instr.Pysh_Instruction(pysh_type[1:] + '_min',
                                                    min_pysh,
                                                    stack_types = [pysh_type])
    return instruction
registered_instructions.register_instruction(minner('_integer'))
registered_instructions.register_instruction(minner('_float'))
#<instr_open>
#<instr_name>integer_min
#<instr_desc>
#<instr_close>
#<instr_open>
#<instr_name>float_min
#<instr_desc>
#<instr_close>


def maxer(pysh_type):
    '''
    Returns a function that pushes the maximum of the top two items.
    '''
    def max_pysh(state):
        if len(state.stacks[pysh_type])>1:
            new_num = max(state.stacks[pysh_type].stack_ref(1), state.stacks[pysh_type].stack_ref(0))
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].push_item(new_num)
    instruction = instr.Pysh_Instruction(pysh_type[1:] + '_max',
                                                    max_pysh,
                                                    stack_types = [pysh_type])
    return instruction
registered_instructions.register_instruction(maxer('_integer'))
registered_instructions.register_instruction(maxer('_float'))
#<instr_open>
#<instr_name>integer_max
#<instr_desc>
#<instr_close>
#<instr_open>
#<instr_name>float_max
#<instr_desc>
#<instr_close>


def incrementer(pysh_type):
    '''
    Returns a function that increments the first item on the stack.
    '''
    def inc(state):
        if len(state.stacks[pysh_type])>0:
            new_num = state.stacks[pysh_type].stack_ref(0) + 1
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].push_item(new_num)
    instruction = instr.Pysh_Instruction(pysh_type[1:] + '_inc',
                                                    inc,
                                                    stack_types = [pysh_type])
    return instruction
registered_instructions.register_instruction(incrementer('_integer'))
registered_instructions.register_instruction(incrementer('_float'))
#<instr_open>
#<instr_name>integer_inc
#<instr_desc>
#<instr_close>
#<instr_open>
#<instr_name>float_inc
#<instr_desc>
#<instr_close>


def decrementer(pysh_type):
    '''
    Returns a function that increments the first item on the stack.
    '''
    def dec(state):
        if len(state.stacks[pysh_type])>0:
            new_num = state.stacks[pysh_type].stack_ref(0) - 1
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].push_item(new_num)
    instruction = instr.Pysh_Instruction(pysh_type[1:] + '_dec',
                                                    dec,
                                                    stack_types = [pysh_type])
    return instruction
registered_instructions.register_instruction(decrementer('_integer'))
registered_instructions.register_instruction(decrementer('_float'))
#<instr_open>
#<instr_name>integer_dec
#<instr_desc>
#<instr_close>
#<instr_open>
#<instr_name>float_dec
#<instr_desc>
#<instr_close>


def float_sin(state):
    '''

    '''
    if len(state.stacks['_float']) > 0:
        new_float = math.sin(state.stacks['_float'].stack_ref(0))
        state.stacks['_float'].pop_item()
        state.stacks['_float'].push_item(new_float)
float_sin_instruction = instr.Pysh_Instruction('float_sin',
                                                          float_sin,
                                                          stack_types = ['_float'])
registered_instructions.register_instruction(float_sin_instruction)
#<instr_open>
#<instr_name>float_sin
#<instr_desc>
#<instr_close>


def float_cos(state):
    '''

    '''
    if len(state.stacks['_float']) > 0:
        new_float = math.cos(state.stacks['_float'].stack_ref(0))
        state.stacks['_float'].pop_item()
        state.stacks['_float'].push_item(new_float)
float_cos_instruction = instr.Pysh_Instruction('float_cos',
                                                          float_cos,
                                                          stack_types = ['_float'])
registered_instructions.register_instruction(float_cos_instruction)
#<instr_open>
#<instr_name>float_cos
#<instr_desc>
#<instr_close>


def float_tan(state):
    '''

    '''
    if len(state.stacks['_float']) > 0:
        new_float = math.tan(state.stacks['_float'].stack_ref(0))
        state.stacks['_float'].pop_item()
        state.stacks['_float'].push_item(new_float)
float_tan_instruction = instr.Pysh_Instruction('float_tan',
                                                          float_tan,
                                                          stack_types = ['_float'])
registered_instructions.register_instruction(float_tan_instruction)
#<instr_open>
#<instr_name>float_tan
#<instr_desc>
#<instr_close>


def integer_from_float(state):
    if len(state.stacks['_float']) > 0:
        new_int = int(state.stacks['_float'].stack_ref(0))
        state.stacks['_float'].pop_item()
        state.stacks['_integer'].push_item(new_int)
int_from_float_instrc = instr.Pysh_Instruction('integer_from_float',
                                                          integer_from_float,
                                                          stack_types = ['_integer', '_float'])
registered_instructions.register_instruction(int_from_float_instrc)
#<instr_open>
#<instr_name>integer_from_float
#<instr_desc>
#<instr_close>


def integer_from_boolean(state):
    if len(state.stacks['_boolean']) > 0:
        new_int = int(state.stacks['_boolean'].stack_ref(0))
        state.stacks['_boolean'].pop_item()
        state.stacks['_integer'].push_item(new_int)
int_from_boolean_instrc = instr.Pysh_Instruction('integer_from_boolean',
                                                            integer_from_boolean,
                                                            stack_types = ['_integer', '_boolean'])
registered_instructions.register_instruction(int_from_boolean_instrc)
#<instr_open>
#<instr_name>integer_from_boolean
#<instr_desc>
#<instr_close>


def float_from_integer(state):
    if len(state.stacks['_integer']) > 0:
        new_float = float(state.stacks['_integer'].stack_ref(0))
        state.stacks['_integer'].pop_item()
        state.stacks['_float'].push_item(new_float)
float_from_int_instrc = instr.Pysh_Instruction('float_from_integer',
                                                          float_from_integer,
                                                          stack_types = ['_float', '_integer'])
registered_instructions.register_instruction(float_from_int_instrc)
#<instr_open>
#<instr_name>float_from_integer
#<instr_desc>
#<instr_close>


def float_from_boolean(state):
    if len(state.stacks['_boolean']) > 0:
        new_float = float(state.stacks['_boolean'].stack_ref(0))
        state.stacks['_boolean'].pop_item()
        state.stacks['_float'].push_item(new_float)
float_from_bool_instrc = instr.Pysh_Instruction('foat_from_boolean',
                                                           float_from_boolean,
                                                           stack_types = ['_float', '_boolean'])
registered_instructions.register_instruction(float_from_bool_instrc)
#<instr_open>
#<instr_name>foat_from_boolean
#<instr_desc>
#<instr_close>
