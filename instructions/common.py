# -*- coding: utf-8 -*-
"""
Created on July 23, 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import copy

from .. import pysh_state
from .. import pysh_instruction

from . import registered_instructions

def popper(pysh_type):
    '''
    Returns an instruction that takes a state and pops the appropriate
    stack of the state.
    '''
    def pop(state):
        if len(state.stacks[pysh_type]) > 0:
            state.stacks[pysh_type].pop_item()
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_pop',
                                                    pop,
                                                    stack_types = [pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 1
    return instruction
registered_instructions.register_instruction(popper('_exec'))
registered_instructions.register_instruction(popper('_integer'))
registered_instructions.register_instruction(popper('_float'))
registered_instructions.register_instruction(popper('_code'))
registered_instructions.register_instruction(popper('_boolean'))
registered_instructions.register_instruction(popper('_string'))


def duper(pysh_type):
    '''
    Returns an instruction that takes a state and duplicates the top item of
    the appropriate stack of the state.
    '''
    def dup(state):
        if len(state.stacks[pysh_type])>0:
            state.stacks[pysh_type].push_item(state.stacks[pysh_type].top_item())
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_dup',
                                                    dup,
                                                    stack_types = [pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 1
    return instruction
registered_instructions.register_instruction(duper('_exec'))
registered_instructions.register_instruction(duper('_integer'))
registered_instructions.register_instruction(duper('_float'))
registered_instructions.register_instruction(duper('_code'))
registered_instructions.register_instruction(duper('_boolean'))
registered_instructions.register_instruction(duper('_string'))


def swapper(pysh_type):
    '''
    Returns a function that takes a state and swaps the top 2 items of the
    appropriate stack of the state.
    '''
    def swap(state):
        if len(state.stacks[pysh_type])>1:
            first_item = state.stacks[pysh_type].stack_ref(0)
            second_item = state.stacks[pysh_type].stack_ref(1)
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].push_item(first_item)
            state.stacks[pysh_type].push_item(second_item)
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_swap',
                                                    swap,
                                                    stack_types = [pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 2
    return instruction
registered_instructions.register_instruction(swapper('_exec'))
registered_instructions.register_instruction(swapper('_integer'))
registered_instructions.register_instruction(swapper('_float'))
registered_instructions.register_instruction(swapper('_code'))
registered_instructions.register_instruction(swapper('_boolean'))
registered_instructions.register_instruction(swapper('_string'))


def rotter(pysh_type):
    '''
    Returns a function that takes a state and rotates the top 3 items
    of the appropriate stack of the state.
    '''
    def rot(state):
        if len(state.stacks[pysh_type])>2:
            first_item = state.stacks[pysh_type].stack_ref(0)
            second_item = state.stacks[pysh_type].stack_ref(1)
            third_item = state.stacks[pysh_type].stack_ref(2)
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].push_item(second_item)
            state.stacks[pysh_type].push_item(first_item)
            state.stacks[pysh_type].push_item(third_item)
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_rot',
                                                    rot,
                                                    stack_types = [pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 3
    return instruction
registered_instructions.register_instruction(rotter('_exec'))
registered_instructions.register_instruction(rotter('_integer'))
registered_instructions.register_instruction(rotter('_float'))
registered_instructions.register_instruction(rotter('_code'))
registered_instructions.register_instruction(rotter('_boolean'))
registered_instructions.register_instruction(rotter('_string'))


def flusher(pysh_type):
    '''
    Returns an instruction that that empties the stack of the given state.
    '''
    def flush(state):
        state.stacks[pysh_type].stack_flush()
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_flush',
                                                    flush,
                                                    stack_types = [pysh_type])
    return instruction
registered_instructions.register_instruction(flusher('_exec'))
registered_instructions.register_instruction(flusher('_integer'))
registered_instructions.register_instruction(flusher('_float'))
registered_instructions.register_instruction(flusher('_code'))
registered_instructions.register_instruction(flusher('_boolean'))
registered_instructions.register_instruction(flusher('_string'))


def eqer(pysh_type):
    '''
    Returns an instruction that compares the top two items of the appropriate 
    stack of the given state.
    '''
    def eq(state):
        if len(state.stacks[pysh_type])>1:
            first_item = state.stacks[pysh_type].stack_ref(0)
            second_item = state.stacks[pysh_type].stack_ref(1)
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].pop_item()
            state.stacks['_boolean'].push_item(first_item == second_item)
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_eq',
                                                    eq,
                                                    stack_types = [pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 0
    if not pysh_type == '_boolean':
        instruction.stack_types.append('_boolean')
    return instruction
registered_instructions.register_instruction(eqer('_exec'))
registered_instructions.register_instruction(eqer('_integer'))
registered_instructions.register_instruction(eqer('_float'))
registered_instructions.register_instruction(eqer('_code'))
registered_instructions.register_instruction(eqer('_boolean'))
registered_instructions.register_instruction(eqer('_string'))


def stackdepther(pysh_type):
    '''
    Returns an instruction that compares the top two items of the appropriate 
    stack of the given state.
    '''
    def stackdepth(state):
        depth = len(state.stacks[pysh_type])
        state.stacks['_integer'].push_item(depth)
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_stack_depth',
                                                    stackdepth,
                                                    stack_types = [pysh_type])
    if not pysh_type == '_integer':
        instruction.stack_types.append('_integer')
    return instruction
registered_instructions.register_instruction(stackdepther('_exec'))
registered_instructions.register_instruction(stackdepther('_integer'))
registered_instructions.register_instruction(stackdepther('_float'))
registered_instructions.register_instruction(stackdepther('_code'))
registered_instructions.register_instruction(stackdepther('_boolean'))
registered_instructions.register_instruction(stackdepther('_string'))


def yanker(pysh_type):
    '''
    Returns an instruction that yanks an item from deep in the specified stack,
    using the top integer to indicate how deep.
    '''
    def yank(state):
        a = pysh_type == '_integer' and len(state.stacks[pysh_type])>1
        b = pysh_type != '_integer' and len(state.stacks[pysh_type])>0 and len(state.stacks['_integer'])>0
        if a or b:
            raw_index = state.stacks['_integer'].stack_ref(0)
            state.stacks['_integer'].pop_item()
            actual_index = int(max(0, min(raw_index, len(state.stacks[pysh_type]) - 1)))
            item = state.stacks[pysh_type].stack_ref(actual_index)
            del state.stacks[pysh_type][actual_index]
            state.stacks[pysh_type].push_item(item)
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_yank',
                                                    yank,
                                                    stack_types = [pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 0
    if not pysh_type == '_integer':
        instruction.stack_types.append('_integer')
    return instruction
registered_instructions.register_instruction(yanker('_exec'))
registered_instructions.register_instruction(yanker('_integer'))
registered_instructions.register_instruction(yanker('_float'))
registered_instructions.register_instruction(yanker('_code'))
registered_instructions.register_instruction(yanker('_boolean'))
registered_instructions.register_instruction(yanker('_string'))


def yankduper(pysh_type):
    '''
    Returns an instruction that yanks a copy of an item from deep in the specified stack,
   using the top integer to indicate how deep.
    '''
    def yankdup(state):
        a = pysh_type == '_integer' and len(state.stacks[pysh_type])>1
        b = pysh_type != '_integer' and len(state.stacks[pysh_type])>0 and len(state.stacks['_integer'])>0
        if a or b:
            raw_index = state.stacks['_integer'].stack_ref(0)
            state.stacks['_integer'].pop_item()
            actual_index = int(max(0, min(raw_index, len(state.stacks[pysh_type]) - 1)))
            item = state.stacks[pysh_type].stack_ref(actual_index)
            state.stacks[pysh_type].push_item(item)
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_yankdup',
                                                    yankdup,
                                                    stack_types = [pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 0
    if not pysh_type == '_integer':
        instruction.stack_types.append('_integer')
    return instruction
registered_instructions.register_instruction(yankduper('_exec'))
registered_instructions.register_instruction(yankduper('_integer'))
registered_instructions.register_instruction(yankduper('_float'))
registered_instructions.register_instruction(yankduper('_code'))
registered_instructions.register_instruction(yankduper('_boolean'))
registered_instructions.register_instruction(yankduper('_string'))

def shover(pysh_type):
    '''
    Returns an instruction that yanks an item from deep in the specified stack,
    using the top integer to indicate how deep.
    '''
    def shove(state):
        a = pysh_type == '_integer' and len(state.stacks[pysh_type])>1
        b = pysh_type != '_integer' and len(state.stacks[pysh_type])>0 and len(state.stacks['_integer'])>0
        if a or b:
            raw_index = state.stacks['_integer'].stack_ref(0)
            state.stacks['_integer'].pop_item()
            item = state.stacks[pysh_type].stack_ref(0)
            state.stacks[pysh_type].pop_item()
            actual_index = int(max(0, min(raw_index, len(state.stacks[pysh_type]))))
            state.stacks[pysh_type].stack_insert(actual_index, item)
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_shove',
                                                    shove,
                                                    stack_types = [pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 1
    if not pysh_type == '_integer':
        instruction.stack_types.append('_integer')
    return instruction
registered_instructions.register_instruction(shover('_exec'))
registered_instructions.register_instruction(shover('_integer'))
registered_instructions.register_instruction(shover('_float'))
registered_instructions.register_instruction(shover('_code'))
registered_instructions.register_instruction(shover('_boolean'))
registered_instructions.register_instruction(shover('_string'))


def emptyer(pysh_type):
    '''
    Returns an instruction that takes a state and tells whether that stack is empty.
    '''
    def empty(state):
        state.stacks['_boolean'].push_item(len(state.stacks[pysh_type])==0)
    instruction = pysh_instruction.Pysh_Instruction(pysh_type[1:] + '_empty',
                                                    empty,
                                                    stack_types = [pysh_type])
    if not pysh_type == '_boolean':
        instruction.stack_types.append('_boolean')
    return instruction
registered_instructions.register_instruction(emptyer('_exec'))
registered_instructions.register_instruction(emptyer('_integer'))
registered_instructions.register_instruction(emptyer('_float'))
registered_instructions.register_instruction(emptyer('_code'))
registered_instructions.register_instruction(emptyer('_boolean'))
registered_instructions.register_instruction(emptyer('_string'))