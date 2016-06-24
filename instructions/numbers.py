# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 14:54:49 2016

@author: Eddie
"""
import math

import pysh_state
import pysh_instruction
import pysh_utils

import registered_instructions


def adder(pysh_type):
    '''
    Returns an instruction that pushes the sum of the top two items.
    '''
    def add(state):
        if len(state.stacks[pysh_type])>1:
            new_num = state.stacks[pysh_type].stack_ref(1) + state.stacks[pysh_type].stack_ref(0)
            new_num = pysh_utils.keep_number_reasonable(new_num)
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].push_item(new_num)
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_add',
                                                    add,
                                                    stack_types = [pysh_type])
    return instruction
registered_instructions.register_instruction(adder('_integer'))
registered_instructions.register_instruction(adder('_float'))


def subtracter(pysh_type):
    '''
    Returns an instruction that pushes the difference  of the top two items.
    '''
    def sub(state):
        if len(state.stacks[pysh_type])>1:
            new_num = state.stacks[pysh_type].stack_ref(1) - state.stacks[pysh_type].stack_ref(0)
            new_num = pysh_utils.keep_number_reasonable(new_num)
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].push_item(new_num)
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_sub',
                                                    sub,
                                                    stack_types = [pysh_type])
    return instruction
registered_instructions.register_instruction(subtracter('_integer'))
registered_instructions.register_instruction(subtracter('_float'))


def multiplier(pysh_type):
    '''
    Returns an instruction that pushes the product  of the top two items.
    '''
    def mult(state):
        if len(state.stacks[pysh_type])>1:
            new_num = state.stacks[pysh_type].stack_ref(1) * state.stacks[pysh_type].stack_ref(0)
            new_num = pysh_utils.keep_number_reasonable(new_num)
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].push_item(new_num)
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_mult',
                                                    mult,
                                                    stack_types = [pysh_type])
    return instruction
registered_instructions.register_instruction(multiplier('_integer'))
registered_instructions.register_instruction(multiplier('_float'))


def divider(pysh_type):
    '''
    Returns a function that pushes the quotient of the top two items.
    Retirms previous state if the denominator would be zero.
    '''
    def div(state):
        if len(state.stacks[pysh_type])>1:
            if state.stacks[pysh_type].stack_ref(0) != 0:
                new_num = state.stacks[pysh_type].stack_ref(1) / state.stacks[pysh_type].stack_ref(0)
                new_num = pysh_utils.keep_number_reasonable(new_num)
                state.stacks[pysh_type].pop_item()
                state.stacks[pysh_type].pop_item()
                state.stacks[pysh_type].push_item(new_num)
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_div',
                                                    div,
                                                    stack_types = [pysh_type])
    return instruction
registered_instructions.register_instruction(divider('_integer'))
registered_instructions.register_instruction(divider('_float'))

def modder(pysh_type):
    '''
    Returns a function that pushes the modulus of the top two items. Does 
    nothing if the denominator would be zero.
    '''
    def mod(state):
        if len(state.stacks[pysh_type])>1:
            if state.stacks[pysh_type].stack_ref(0) != 0:
                new_num = state.stacks[pysh_type].stack_ref(1) % state.stacks[pysh_type].stack_ref(0)
                new_num = pysh_utils.keep_number_reasonable(new_num)
                state.stacks[pysh_type].pop_item()
                state.stacks[pysh_type].pop_item()
                state.stacks[pysh_type].push_item(new_num)
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_mod',
                                                    mod,
                                                    stack_types = [pysh_type])
    return instruction
registered_instructions.register_instruction(modder('_integer'))
registered_instructions.register_instruction(modder('_float'))

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
            state.stacks['_bool'].push_item(new_bool)
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_lt',
                                                    lt,
                                                    stack_types = [pysh_type, '_bool'])
    return instruction
registered_instructions.register_instruction(less_than('_integer'))
registered_instructions.register_instruction(less_than('_float'))

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
            state.stacks['_bool'].push_item(new_bool)
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_lte',
                                                    lte,
                                                    stack_types = [pysh_type, '_bool'])
    return instruction
registered_instructions.register_instruction(less_than_equal('_integer'))
registered_instructions.register_instruction(less_than_equal('_float'))

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
            state.stacks['_bool'].push_item(new_bool)
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_gt',
                                                    gt,
                                                    stack_types = [pysh_type, '_bool'])
    return instruction
registered_instructions.register_instruction(greater_than('_integer'))
registered_instructions.register_instruction(greater_than('_float'))

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
            state.stacks['_bool'].push_item(new_bool)
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_gte',
                                                    gte,
                                                    stack_types = [pysh_type, '_bool'])
    return instruction
registered_instructions.register_instruction(greater_than_equal('_integer'))
registered_instructions.register_instruction(greater_than_equal('_float'))

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
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_min',
                                                    min_pysh,
                                                    stack_types = [pysh_type])
    return instruction
registered_instructions.register_instruction(minner('_integer'))
registered_instructions.register_instruction(minner('_float'))

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
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_max',
                                                    max_pysh,
                                                    stack_types = [pysh_type])
    return instruction
registered_instructions.register_instruction(maxer('_integer'))
registered_instructions.register_instruction(maxer('_float'))

def incrementer(pysh_type):
    '''
    Returns a function that increments the first item on the stack.
    '''
    def inc(state):
        if len(state.stacks[pysh_type])>0:
            new_num = state.stacks[pysh_type].stack_ref(0) + 1
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].push_item(new_num)
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_inc',
                                                    inc,
                                                    stack_types = [pysh_type])
    return instruction
registered_instructions.register_instruction(incrementer('_integer'))
registered_instructions.register_instruction(incrementer('_float'))

def decrementer(pysh_type):
    '''
    Returns a function that increments the first item on the stack.
    '''
    def dec(state):
        if len(state.stacks[pysh_type])>0:
            new_num = state.stacks[pysh_type].stack_ref(0) - 1
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].push_item(new_num)
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_dec',
                                                    dec,
                                                    stack_types = [pysh_type])
    return instruction
registered_instructions.register_instruction(decrementer('_integer'))
registered_instructions.register_instruction(decrementer('_float'))





