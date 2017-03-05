# -*- coding: utf-8 -*-
"""
Created on July 23, 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from .. import instruction as instr

from . import registered_instructions

def popper(pysh_type):
    '''
    Returns an instruction that takes a state and pops the appropriate
    stack of the state.
    '''
    def pop(state):
        if len(state.stacks[pysh_type]) > 0:
            state.stacks[pysh_type].pop_item()
    instruction = instr.PyshInstruction(pysh_type + '_pop',
                                        pop,
                                        stack_types = [pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 1
    return instruction
registered_instructions.register_instruction(popper('_exec'))
#<instr_open>
#<instr_name>exec_pop
#<instr_desc>Pops the top item off the 'exec' stack.
#<instr_close>
registered_instructions.register_instruction(popper('_integer'))
#<instr_open>
#<instr_name>integer_pop
#<instr_desc>Pops the top item off the 'integer' stack.
#<instr_close>
registered_instructions.register_instruction(popper('_float'))
#<instr_open>
#<instr_name>float_pop
#<instr_desc>Pops the top item off the 'float' stack.
#<instr_close>
registered_instructions.register_instruction(popper('_code'))
#<instr_open>
#<instr_name>code_pop
#<instr_desc>Pops the top item off the 'code' stack.
#<instr_close>
registered_instructions.register_instruction(popper('_boolean'))
#<instr_open>
#<instr_name>boolean_pop
#<instr_desc>Pops the top item off the 'boolean' stack.
#<instr_close>
registered_instructions.register_instruction(popper('_string'))
#<instr_open>
#<instr_name>string_pop
#<instr_desc>Pops the top item off the 'string' stack.
#<instr_close>
registered_instructions.register_instruction(popper('_char'))
#<instr_open>
#<instr_name>char_pop
#<instr_desc>Pops the top item off the 'char' stack.
#<instr_close>


def duper(pysh_type):
    '''
    Returns an instruction that takes a state and duplicates the top item of
    the appropriate stack of the state.
    '''
    def dup(state):
        if len(state.stacks[pysh_type]) > 0:
            state.stacks[pysh_type].push_item(state.stacks[pysh_type].top_item())
    instruction = instr.PyshInstruction(pysh_type + '_dup',
                                        dup,
                                        stack_types = [pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 1
    return instruction
registered_instructions.register_instruction(duper('_exec'))
#<instr_open>
#<instr_name>exec_dup
#<instr_desc>Duplicates the top item of the `exec` stack.
#<instr_close>
registered_instructions.register_instruction(duper('_integer'))
#<instr_open>
#<instr_name>integer_dup
#<instr_desc>Duplicates the top item of the `integer` stack.
#<instr_close>
registered_instructions.register_instruction(duper('_float'))
#<instr_open>
#<instr_name>float_dup
#<instr_desc>Duplicates the top item of the `float` stack.
#<instr_close>
registered_instructions.register_instruction(duper('_code'))
#<instr_open>
#<instr_name>code_dup
#<instr_desc>Duplicates the top item of the `code` stack.
#<instr_close>
registered_instructions.register_instruction(duper('_boolean'))
#<instr_open>
#<instr_name>boolean_dup
#<instr_desc>Duplicates the top item of the `boolean` stack.
#<instr_close>
registered_instructions.register_instruction(duper('_string'))
#<instr_open>
#<instr_name>string_dup
#<instr_desc>Duplicates the top item of the `string` stack.
#<instr_close>
registered_instructions.register_instruction(duper('_char'))
#<instr_open>
#<instr_name>char_dup
#<instr_desc>Duplicates the top item of the `char` stack.
#<instr_close>


def swapper(pysh_type):
    '''
    Returns a function that takes a state and swaps the top 2 items of the
    appropriate stack of the state.
    '''
    def swap(state):
        if len(state.stacks[pysh_type])>1:
            first_item = state.stacks[pysh_type].ref(0)
            second_item = state.stacks[pysh_type].ref(1)
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].push_item(first_item)
            state.stacks[pysh_type].push_item(second_item)
    instruction = instr.PyshInstruction(pysh_type + '_swap',
                                        swap,
                                        stack_types = [pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 2
    return instruction
registered_instructions.register_instruction(swapper('_exec'))
#<instr_open>
#<instr_name>exec_swap
#<instr_desc>Swaps the top 2 items of the `exec` stack.
#<instr_close>
registered_instructions.register_instruction(swapper('_integer'))
#<instr_open>
#<instr_name>integer_swap
#<instr_desc>Swaps the top 2 items of the `integer` stack.
#<instr_close>
registered_instructions.register_instruction(swapper('_float'))
#<instr_open>
#<instr_name>float_swap
#<instr_desc>Swaps the top 2 items of the `float` stack.
#<instr_close>
registered_instructions.register_instruction(swapper('_code'))
#<instr_open>
#<instr_name>code_swap
#<instr_desc>Swaps the top 2 items of the `code` stack.
#<instr_close>
registered_instructions.register_instruction(swapper('_boolean'))
#<instr_open>
#<instr_name>boolean_swap
#<instr_desc>Swaps the top 2 items of the `boolean` stack.
#<instr_close>
registered_instructions.register_instruction(swapper('_string'))
#<instr_open>
#<instr_name>string_swap
#<instr_desc>Swaps the top 2 items of the `string` stack.
#<instr_close>
registered_instructions.register_instruction(swapper('_char'))
#<instr_open>
#<instr_name>char_swap
#<instr_desc>Swaps the top 2 items of the `char` stack.
#<instr_close>



def rotter(pysh_type):
    '''
    Returns a function that takes a state and rotates the top 3 items
    of the appropriate stack of the state.
    '''
    def rot(state):
        if len(state.stacks[pysh_type])>2:
            first_item = state.stacks[pysh_type].ref(0)
            second_item = state.stacks[pysh_type].ref(1)
            third_item = state.stacks[pysh_type].ref(2)
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].push_item(second_item)
            state.stacks[pysh_type].push_item(first_item)
            state.stacks[pysh_type].push_item(third_item)
    instruction = instr.PyshInstruction(pysh_type + '_rot',
                                        rot,
                                        stack_types = [pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 3
    return instruction
registered_instructions.register_instruction(rotter('_exec'))
#<instr_open>
#<instr_name>exec_rot
#<instr_desc>Rotates the top 3 items of the `exec` stack.
#<instr_close>
registered_instructions.register_instruction(rotter('_integer'))
#<instr_open>
#<instr_name>integer_rot
#<instr_desc>Rotates the top 3 items of the `integer` stack.
#<instr_close>
registered_instructions.register_instruction(rotter('_float'))
#<instr_open>
#<instr_name>float_rot
#<instr_desc>Rotates the top 3 items of the `float` stack.
#<instr_close>
registered_instructions.register_instruction(rotter('_code'))
#<instr_open>
#<instr_name>code_rot
#<instr_desc>Rotates the top 3 items of the `code` stack.
#<instr_close>
registered_instructions.register_instruction(rotter('_boolean'))
#<instr_open>
#<instr_name>boolean_rot
#<instr_desc>Rotates the top 3 items of the `boolean` stack.
#<instr_close>
registered_instructions.register_instruction(rotter('_string'))
#<instr_open>
#<instr_name>string_rot
#<instr_desc>Rotates the top 3 items of the `string` stack.
#<instr_close>
registered_instructions.register_instruction(rotter('_char'))
#<instr_open>
#<instr_name>char_rot
#<instr_desc>Rotates the top 3 items of the `char` stack.
#<instr_close>


def flusher(pysh_type):
    '''
    Returns an instruction that that empties the stack of the given state.
    '''
    def flush(state):
        state.stacks[pysh_type].flush()
    instruction = instr.PyshInstruction(pysh_type + '_flush',
                                        flush,
                                        stack_types = [pysh_type])
    return instruction
registered_instructions.register_instruction(flusher('_exec'))
#<instr_open>
#<instr_name>exec_flush
#<instr_desc>Empties the 'exec' stack.
#<instr_close>
registered_instructions.register_instruction(flusher('_integer'))
#<instr_open>
#<instr_name>integer_flush
#<instr_desc>Empties the 'integer' stack.
#<instr_close>
registered_instructions.register_instruction(flusher('_float'))
#<instr_open>
#<instr_name>float_flush
#<instr_desc>Empties the 'float' stack.
#<instr_close>
registered_instructions.register_instruction(flusher('_code'))
#<instr_open>
#<instr_name>code_flush
#<instr_desc>Empties the 'code' stack.
#<instr_close>
registered_instructions.register_instruction(flusher('_boolean'))
#<instr_open>
#<instr_name>boolean_flush
#<instr_desc>Empties the 'boolean' stack.
#<instr_close>
registered_instructions.register_instruction(flusher('_string'))
#<instr_open>
#<instr_name>string_flush
#<instr_desc>Empties the 'string' stack.
#<instr_close>
registered_instructions.register_instruction(flusher('_char'))
#<instr_open>
#<instr_name>char_flush
#<instr_desc>Empties the 'char' stack.
#<instr_close>


def eqer(pysh_type):
    '''
    Returns an instruction that compares the top two items of the appropriate 
    stack of the given state.
    '''
    def eq(state):
        if len(state.stacks[pysh_type])>1:
            first_item = state.stacks[pysh_type].ref(0)
            second_item = state.stacks[pysh_type].ref(1)
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].pop_item()
            state.stacks['_boolean'].push_item(first_item == second_item)
    instruction = instr.PyshInstruction(pysh_type + '_eq',
                                        eq,
                                        stack_types = [pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 0
    if not pysh_type == '_boolean':
        instruction.stack_types.append('_boolean')
    return instruction
registered_instructions.register_instruction(eqer('_exec'))
#<instr_open>
#<instr_name>exec_eq
#<instr_desc>Pushes True if top two items on the `exec` stack are equal. Pushes False otherwise.
#<instr_close>
registered_instructions.register_instruction(eqer('_integer'))
#<instr_open>
#<instr_name>integer_eq
#<instr_desc>Pushes True if top two items on the `integer` stack are equal. Pushes False otherwise.
#<instr_close>
registered_instructions.register_instruction(eqer('_float'))
#<instr_open>
#<instr_name>float_eq
#<instr_desc>Pushes True if top two items on the `float` stack are equal. Pushes False otherwise.
#<instr_close>
registered_instructions.register_instruction(eqer('_code'))
#<instr_open>
#<instr_name>code_eq
#<instr_desc>Pushes True if top two items on the `code` stack are equal. Pushes False otherwise.
#<instr_close>
registered_instructions.register_instruction(eqer('_boolean'))
#<instr_open>
#<instr_name>boolean_eq
#<instr_desc>Pushes True if top two items on the `boolean` stack are equal. Pushes False otherwise.
#<instr_close>
registered_instructions.register_instruction(eqer('_string'))
#<instr_open>
#<instr_name>string_eq
#<instr_desc>Pushes True if top two items on the `string` stack are equal. Pushes False otherwise.
#<instr_close>
registered_instructions.register_instruction(eqer('_char'))
#<instr_open>
#<instr_name>char_eq
#<instr_desc>Pushes True if top two items on the `char` stack are equal. Pushes False otherwise.
#<instr_close>


def stackdepther(pysh_type):
    '''
    Returns an instruction that puses the depth of the appropiate stack of the state.
    '''
    def stackdepth(state):
        depth = len(state.stacks[pysh_type])
        state.stacks['_integer'].push_item(depth)
    instruction = instr.PyshInstruction(pysh_type + '_stack_depth',
                                        stackdepth,
                                        stack_types = [pysh_type])
    if not pysh_type == '_integer':
        instruction.stack_types.append('_integer')
    return instruction
registered_instructions.register_instruction(stackdepther('_exec'))
#<instr_open>
#<instr_name>exec_stack_depth
#<instr_desc>Pushes the depth of the `exec` stack to the `integer` stack.
#<instr_close>
registered_instructions.register_instruction(stackdepther('_integer'))
#<instr_open>
#<instr_name>integer_stack_depth
#<instr_desc>Pushes the depth of the `integer` stack to the `integer` stack.
#<instr_close>
registered_instructions.register_instruction(stackdepther('_float'))
#<instr_open>
#<instr_name>float_stack_depth
#<instr_desc>Pushes the depth of the `float` stack to the `integer` stack.
#<instr_close>
registered_instructions.register_instruction(stackdepther('_code'))
#<instr_open>
#<instr_name>code_stack_depth
#<instr_desc>Pushes the depth of the `code` stack to the `integer` stack.
#<instr_close>
registered_instructions.register_instruction(stackdepther('_boolean'))
#<instr_open>
#<instr_name>boolean_stack_depth
#<instr_desc>Pushes the depth of the `boolean` stack to the `integer` stack.
#<instr_close>
registered_instructions.register_instruction(stackdepther('_string'))
#<instr_open>
#<instr_name>string_stack_depth
#<instr_desc>Pushes the depth of the `string` stack to the `integer` stack.
#<instr_close>
registered_instructions.register_instruction(stackdepther('_char'))
#<instr_open>
#<instr_name>char_stack_depth
#<instr_desc>Pushes the depth of the `char` stack to the `integer` stack.
#<instr_close>


def yanker(pysh_type):
    '''
    Returns an instruction that yanks an item from deep in the specified stack,
    using the top integer to indicate how deep.
    '''
    def yank(state):
        a = pysh_type == '_integer' and len(state.stacks[pysh_type])>1
        b = pysh_type != '_integer' and len(state.stacks[pysh_type])>0 and len(state.stacks['_integer'])>0
        if a or b:
            raw_index = state.stacks['_integer'].ref(0)
            state.stacks['_integer'].pop_item()
            actual_index = int(max(0, min(raw_index, len(state.stacks[pysh_type]) - 1)))
            item = state.stacks[pysh_type].ref(actual_index)
            del state.stacks[pysh_type][-actual_index-1]
            state.stacks[pysh_type].push_item(item)
    instruction = instr.PyshInstruction(pysh_type + '_yank',
                                        yank,
                                        stack_types = [pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 0
    if not pysh_type == '_integer':
        instruction.stack_types.append('_integer')
    return instruction
registered_instructions.register_instruction(yanker('_exec'))
#<instr_open>
#<instr_name>exec_yank
#<instr_desc>Yanks an item from deep in the `exec` stack, using the top `integer` to indicate how deep.
#<instr_close>
registered_instructions.register_instruction(yanker('_integer'))
#<instr_open>
#<instr_name>integer_yank
#<instr_desc>Yanks an item from deep in the `integer` stack, using the top `integer` to indicate how deep.
#<instr_close>
registered_instructions.register_instruction(yanker('_float'))
#<instr_open>
#<instr_name>float_yank
#<instr_desc>Yanks an item from deep in the `float` stack, using the top `integer` to indicate how deep.
#<instr_close>
registered_instructions.register_instruction(yanker('_code'))
#<instr_open>
#<instr_name>code_yank
#<instr_desc>Yanks an item from deep in the `code` stack, using the top `integer` to indicate how deep.
#<instr_close>
registered_instructions.register_instruction(yanker('_boolean'))
#<instr_open>
#<instr_name>boolean_yank
#<instr_desc>Yanks an item from deep in the `boolean` stack, using the top `integer` to indicate how deep.
#<instr_close>
registered_instructions.register_instruction(yanker('_string'))
#<instr_open>
#<instr_name>string_yank
#<instr_desc>Yanks an item from deep in the `string` stack, using the top `integer` to indicate how deep.
#<instr_close>
registered_instructions.register_instruction(yanker('_char'))
#<instr_open>
#<instr_name>char_yank
#<instr_desc>Yanks an item from deep in the `char` stack, using the top `integer` to indicate how deep.
#<instr_close>


def yankduper(pysh_type):
    '''
    Returns an instruction that yanks a copy of an item from deep in the specified stack,
   using the top integer to indicate how deep.
    '''
    def yankdup(state):
        a = pysh_type == '_integer' and len(state.stacks[pysh_type])>1
        b = pysh_type != '_integer' and len(state.stacks[pysh_type])>0 and len(state.stacks['_integer'])>0
        if a or b:
            raw_index = state.stacks['_integer'].ref(0)
            state.stacks['_integer'].pop_item()
            actual_index = int(max(0, min(raw_index, len(state.stacks[pysh_type]) - 1)))
            item = state.stacks[pysh_type].ref(actual_index)
            state.stacks[pysh_type].push_item(item)
    instruction = instr.PyshInstruction(pysh_type + '_yankdup',
                                        yankdup,
                                        stack_types = [pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 0
    if not pysh_type == '_integer':
        instruction.stack_types.append('_integer')
    return instruction
registered_instructions.register_instruction(yankduper('_exec'))
#<instr_open>
#<instr_name>exec_yankdup
#<instr_desc>Yanks a copy of an item from deep in the `exec` stack, using the top `integer` to indicate how deep.
#<instr_close>
registered_instructions.register_instruction(yankduper('_integer'))
#<instr_open>
#<instr_name>integer_yankdup
#<instr_desc>Yanks a copy of an item from deep in the `integer` stack, using the top `integer` to indicate how deep.
#<instr_close>
registered_instructions.register_instruction(yankduper('_float'))
#<instr_open>
#<instr_name>float_yankdup
#<instr_desc>Yanks a copy of an item from deep in the `float` stack, using the top `integer` to indicate how deep.
#<instr_close>
registered_instructions.register_instruction(yankduper('_code'))
#<instr_open>
#<instr_name>code_yankdup
#<instr_desc>Yanks a copy of an item from deep in the `code` stack, using the top `integer` to indicate how deep.
#<instr_close>
registered_instructions.register_instruction(yankduper('_boolean'))
#<instr_open>
#<instr_name>boolean_yankdup
#<instr_desc>Yanks a copy of an item from deep in the `boolean` stack, using the top `integer` to indicate how deep.
#<instr_close>
registered_instructions.register_instruction(yankduper('_string'))
#<instr_open>
#<instr_name>string_yankdup
#<instr_desc>Yanks a copy of an item from deep in the `string` stack, using the top `integer` to indicate how deep.
#<instr_close>
registered_instructions.register_instruction(yankduper('_char'))
#<instr_open>
#<instr_name>char_yankdup
#<instr_desc>Yanks a copy of an item from deep in the `char` stack, using the top `integer` to indicate how deep.
#<instr_close>


def shover(pysh_type):
    '''
    Returns an instruction that shoves an item deep in the specified stack, using the top
    integer to indicate how deep.
    '''
    def shove(state):
        a = pysh_type == '_integer' and len(state.stacks[pysh_type])>1
        b = pysh_type != '_integer' and len(state.stacks[pysh_type])>0 and len(state.stacks['_integer'])>0
        if a or b:
            raw_index = state.stacks['_integer'].ref(0)
            state.stacks['_integer'].pop_item()
            item = state.stacks[pysh_type].ref(0)
            state.stacks[pysh_type].pop_item()
            actual_index = int(max(0, min(raw_index, len(state.stacks[pysh_type]))))
            state.stacks[pysh_type].insert(actual_index, item)
    instruction = instr.PyshInstruction(pysh_type + '_shove',
                                        shove,
                                        stack_types = [pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 1
    if not pysh_type == '_integer':
        instruction.stack_types.append('_integer')
    return instruction
registered_instructions.register_instruction(shover('_exec'))
#<instr_open>
#<instr_name>exec_shove
#<instr_desc>Shoves an item deep in the `exec` stack, using the top `integer` to indicate how deep.
#<instr_close>
registered_instructions.register_instruction(shover('_integer'))
#<instr_open>
#<instr_name>integer_shove
#<instr_desc>Shoves an item deep in the `integer` stack, using the top `integer` to indicate how deep.
#<instr_close>
registered_instructions.register_instruction(shover('_float'))
#<instr_open>
#<instr_name>float_shove
#<instr_desc>Shoves an item deep in the `float` stack, using the top `integer` to indicate how deep.
#<instr_close>
registered_instructions.register_instruction(shover('_code'))
#<instr_open>
#<instr_name>code_shove
#<instr_desc>Shoves an item deep in the `code` stack, using the top `integer` to indicate how deep.
#<instr_close>
registered_instructions.register_instruction(shover('_boolean'))
#<instr_open>
#<instr_name>boolean_shove
#<instr_desc>Shoves an item deep in the `boolean` stack, using the top `integer` to indicate how deep.
#<instr_close>
registered_instructions.register_instruction(shover('_string'))
#<instr_open>
#<instr_name>string_shove
#<instr_desc>Shoves an item deep in the `string` stack, using the top `integer` to indicate how deep.
#<instr_close>
registered_instructions.register_instruction(shover('_char'))
#<instr_open>
#<instr_name>char_shove
#<instr_desc>Shoves an item deep in the `char` stack, using the top `integer` to indicate how deep.
#<instr_close>


def emptyer(pysh_type):
    '''
    Returns an instruction that takes a state and tells whether that stack is empty.
    '''
    def empty(state):
        state.stacks['_boolean'].push_item(len(state.stacks[pysh_type])==0)
    instruction = instr.PyshInstruction(pysh_type + '_empty',
                                        empty,
                                        stack_types = [pysh_type])
    if not pysh_type == '_boolean':
        instruction.stack_types.append('_boolean')
    return instruction
registered_instructions.register_instruction(emptyer('_exec'))
#<instr_open>
#<instr_name>exec_empty
#<instr_desc>Pushes True if the `exec` stack is empty. Pushes False otherwise.
#<instr_close>
registered_instructions.register_instruction(emptyer('_integer'))
#<instr_open>
#<instr_name>integer_empty
#<instr_desc>Pushes True if the `integer` stack is empty. Pushes False otherwise.
#<instr_close>
registered_instructions.register_instruction(emptyer('_float'))
#<instr_open>
#<instr_name>float_empty
#<instr_desc>Pushes True if the `float` stack is empty. Pushes False otherwise.
#<instr_close>
registered_instructions.register_instruction(emptyer('_code'))
#<instr_open>
#<instr_name>code_empty
#<instr_desc>Pushes True if the `code` stack is empty. Pushes False otherwise.
#<instr_close>
registered_instructions.register_instruction(emptyer('_boolean'))
#<instr_open>
#<instr_name>boolean_empty
#<instr_desc>Pushes True if the `boolean` stack is empty. Pushes False otherwise.
#<instr_close>
registered_instructions.register_instruction(emptyer('_string'))
#<instr_open>
#<instr_name>string_empty
#<instr_desc>Pushes True if the `string` stack is empty. Pushes False otherwise.
#<instr_close>
registered_instructions.register_instruction(emptyer('_char'))
#<instr_open>
#<instr_name>char_empty
#<instr_desc>Pushes True if the `char` stack is empty. Pushes False otherwise.
#<instr_close>