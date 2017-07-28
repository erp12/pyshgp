# -*- coding: utf-8 -*-
"""
Created on July 23, 2016

@author: Eddie
"""
from .. import instruction as instr


def popper(pysh_type):
    '''
    Returns an instruction that takes a state and pops the appropriate
    stack of the state.
    '''
    def pop(state):
        if len(state[pysh_type]) > 0:
            state[pysh_type].pop()
    instruction = instr.PyshInstruction(pysh_type + '_pop',
                                        pop,
                                        stack_types=[pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 1
    return instruction


pop_exec_instr = popper('_exec')
pop_integer_instr = popper('_integer')
pop_float_instr = popper('_float')
pop_code_instr = popper('_code')
pop_boolean_instr = popper('_boolean')
pop_string_instr = popper('_string')
pop_char_instr = popper('_char')
# <instr_open>
# <instr_name>exec_pop
# <instr_desc>Pops the top item off the 'exec' stack.
# <instr_close>
# <instr_open>
# <instr_name>integer_pop
# <instr_desc>Pops the top item off the 'integer' stack.
# <instr_close>
# <instr_open>
# <instr_name>float_pop
# <instr_desc>Pops the top item off the 'float' stack.
# <instr_close>
# <instr_open>
# <instr_name>code_pop
# <instr_desc>Pops the top item off the 'code' stack.
# <instr_close>
# <instr_open>
# <instr_name>boolean_pop
# <instr_desc>Pops the top item off the 'boolean' stack.
# <instr_close>
# <instr_open>
# <instr_name>string_pop
# <instr_desc>Pops the top item off the 'string' stack.
# <instr_close>
# <instr_open>
# <instr_name>char_pop
# <instr_desc>Pops the top item off the 'char' stack.
# <instr_close>


def duper(pysh_type):
    '''
    Returns an instruction that takes a state and duplicates the top item of
    the appropriate stack of the state.
    '''
    def dup(state):
        if len(state[pysh_type]) > 0:
            state[pysh_type].push(state[pysh_type].top_item())
    instruction = instr.PyshInstruction(pysh_type + '_dup',
                                        dup,
                                        stack_types=[pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 1
    return instruction


dup_exec_instr = duper('_exec')
dup_integer_instr = duper('_integer')
dup_float_instr = duper('_float')
dup_code_instr = duper('_code')
dup_boolean_instr = duper('_boolean')
dup_string_instr = duper('_string')
dup_char_instr = duper('_char')
# <instr_open>
# <instr_name>exec_dup
# <instr_desc>Duplicates the top item of the `exec` stack.
# <instr_close>
# <instr_open>
# <instr_name>integer_dup
# <instr_desc>Duplicates the top item of the `integer` stack.
# <instr_close>
# <instr_open>
# <instr_name>float_dup
# <instr_desc>Duplicates the top item of the `float` stack.
# <instr_close>
# <instr_open>
# <instr_name>code_dup
# <instr_desc>Duplicates the top item of the `code` stack.
# <instr_close>
# <instr_open>
# <instr_name>boolean_dup
# <instr_desc>Duplicates the top item of the `boolean` stack.
# <instr_close>
# <instr_open>
# <instr_name>string_dup
# <instr_desc>Duplicates the top item of the `string` stack.
# <instr_close>
# <instr_open>
# <instr_name>char_dup
# <instr_desc>Duplicates the top item of the `char` stack.
# <instr_close>


def swapper(pysh_type):
    '''
    Returns a function that takes a state and swaps the top 2 items of the
    appropriate stack of the state.
    '''
    def swap(state):
        if len(state[pysh_type]) > 1:
            first_item = state[pysh_type].ref(0)
            second_item = state[pysh_type].ref(1)
            state[pysh_type].pop()
            state[pysh_type].pop()
            state[pysh_type].push(first_item)
            state[pysh_type].push(second_item)
    instruction = instr.PyshInstruction(pysh_type + '_swap',
                                        swap,
                                        stack_types=[pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 2
    return instruction


swap_exec_instr = swapper('_exec')
swap_integer_instr = swapper('_integer')
swap_float_instr = swapper('_float')
swap_code_instr = swapper('_code')
swap_boolean_instr = swapper('_boolean')
swap_string_instr = swapper('_string')
swap_char_instr = swapper('_char')
# <instr_open>
# <instr_name>exec_swap
# <instr_desc>Swaps the top 2 items of the `exec` stack.
# <instr_close>
# <instr_open>
# <instr_name>integer_swap
# <instr_desc>Swaps the top 2 items of the `integer` stack.
# <instr_close>
# <instr_open>
# <instr_name>float_swap
# <instr_desc>Swaps the top 2 items of the `float` stack.
# <instr_close>
# <instr_open>
# <instr_name>code_swap
# <instr_desc>Swaps the top 2 items of the `code` stack.
# <instr_close>
# <instr_open>
# <instr_name>boolean_swap
# <instr_desc>Swaps the top 2 items of the `boolean` stack.
# <instr_close>
# <instr_open>
# <instr_name>string_swap
# <instr_desc>Swaps the top 2 items of the `string` stack.
# <instr_close>
# <instr_open>
# <instr_name>char_swap
# <instr_desc>Swaps the top 2 items of the `char` stack.
# <instr_close>


def rotter(pysh_type):
    '''
    Returns a function that takes a state and rotates the top 3 items
    of the appropriate stack of the state.
    '''
    def rot(state):
        if len(state[pysh_type]) > 2:
            first_item = state[pysh_type].ref(0)
            second_item = state[pysh_type].ref(1)
            third_item = state[pysh_type].ref(2)
            state[pysh_type].pop()
            state[pysh_type].pop()
            state[pysh_type].pop()
            state[pysh_type].push(second_item)
            state[pysh_type].push(first_item)
            state[pysh_type].push(third_item)
    instruction = instr.PyshInstruction(pysh_type + '_rot',
                                        rot,
                                        stack_types=[pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 3
    return instruction


rot_exec_instr = rotter('_exec')
rot_integer_instr = rotter('_integer')
rot_float_instr = rotter('_float')
rot_code_instr = rotter('_code')
rot_boolean_instr = rotter('_boolean')
rot_string_instr = rotter('_string')
rot_char_instr = rotter('_char')
# <instr_open>
# <instr_name>exec_rot
# <instr_desc>Rotates the top 3 items of the `exec` stack.
# <instr_close>
# <instr_open>
# <instr_name>integer_rot
# <instr_desc>Rotates the top 3 items of the `integer` stack.
# <instr_close>
# <instr_open>
# <instr_name>float_rot
# <instr_desc>Rotates the top 3 items of the `float` stack.
# <instr_close>
# <instr_open>
# <instr_name>code_rot
# <instr_desc>Rotates the top 3 items of the `code` stack.
# <instr_close>
# <instr_open>
# <instr_name>boolean_rot
# <instr_desc>Rotates the top 3 items of the `boolean` stack.
# <instr_close>
# <instr_open>
# <instr_name>string_rot
# <instr_desc>Rotates the top 3 items of the `string` stack.
# <instr_close>
# <instr_open>
# <instr_name>char_rot
# <instr_desc>Rotates the top 3 items of the `char` stack.
# <instr_close>


def flusher(pysh_type):
    '''
    Returns an instruction that that empties the stack of the given state.
    '''
    def flush(state):
        state[pysh_type].flush()
    instruction = instr.PyshInstruction(pysh_type + '_flush',
                                        flush,
                                        stack_types=[pysh_type])
    return instruction


flush_exec_instr = flusher('_exec')
flush_integer_instr = flusher('_integer')
flush_float_instr = flusher('_float')
flush_code_instr = flusher('_code')
flush_boolean_instr = flusher('_boolean')
flush_string_instr = flusher('_string')
flush_char_instr = flusher('_char')
# <instr_open>
# <instr_name>exec_flush
# <instr_desc>Empties the 'exec' stack.
# <instr_close>
# <instr_open>
# <instr_name>integer_flush
# <instr_desc>Empties the 'integer' stack.
# <instr_close>
# <instr_open>
# <instr_name>float_flush
# <instr_desc>Empties the 'float' stack.
# <instr_close>
# <instr_open>
# <instr_name>code_flush
# <instr_desc>Empties the 'code' stack.
# <instr_close>
# <instr_open>
# <instr_name>boolean_flush
# <instr_desc>Empties the 'boolean' stack.
# <instr_close>
# <instr_open>
# <instr_name>string_flush
# <instr_desc>Empties the 'string' stack.
# <instr_close>
# <instr_open>
# <instr_name>char_flush
# <instr_desc>Empties the 'char' stack.
# <instr_close>


def eqer(pysh_type):
    '''
    Returns an instruction that compares the top two items of the appropriate
    stack of the given state.
    '''
    def eq(state):
        if len(state[pysh_type]) > 1:
            first_item = state[pysh_type].ref(0)
            second_item = state[pysh_type].ref(1)
            state[pysh_type].pop()
            state[pysh_type].pop()
            state['_boolean'].push(first_item == second_item)
    instruction = instr.PyshInstruction(pysh_type + '_eq',
                                        eq,
                                        stack_types=[pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 0
    if not pysh_type == '_boolean':
        instruction.stack_types.append('_boolean')
    return instruction


eq_exec_instr = eqer('_exec')
eq_integer_instr = eqer('_integer')
eq_float_instr = eqer('_float')
eq_code_instr = eqer('_code')
eq_boolean_instr = eqer('_boolean')
eq_string_instr = eqer('_string')
eq_char_instr = eqer('_char')
# <instr_open>
# <instr_name>exec_eq
# <instr_desc>Pushes True if top two items on the `exec` stack are equal. Pushes False otherwise.
# <instr_close>
# <instr_open>
# <instr_name>integer_eq
# <instr_desc>Pushes True if top two items on the `integer` stack are equal. Pushes False otherwise.
# <instr_close>
# <instr_open>
# <instr_name>float_eq
# <instr_desc>Pushes True if top two items on the `float` stack are equal. Pushes False otherwise.
# <instr_close>
# <instr_open>
# <instr_name>code_eq
# <instr_desc>Pushes True if top two items on the `code` stack are equal. Pushes False otherwise.
# <instr_close>
# <instr_open>
# <instr_name>boolean_eq
# <instr_desc>Pushes True if top two items on the `boolean` stack are equal. Pushes False otherwise.
# <instr_close>
# <instr_open>
# <instr_name>string_eq
# <instr_desc>Pushes True if top two items on the `string` stack are equal. Pushes False otherwise.
# <instr_close>
# <instr_open>
# <instr_name>char_eq
# <instr_desc>Pushes True if top two items on the `char` stack are equal. Pushes False otherwise.
# <instr_close>


def stackdepther(pysh_type):
    '''
    Returns an instruction that puses the depth of the appropiate stack of the state.
    '''
    def stackdepth(state):
        depth = len(state[pysh_type])
        state['_integer'].push(depth)
    instruction = instr.PyshInstruction(pysh_type + '_stack_depth',
                                        stackdepth,
                                        stack_types=[pysh_type])
    if not pysh_type == '_integer':
        instruction.stack_types.append('_integer')
    return instruction


stack_depth_exec_instr = stackdepther('_exec')
stack_depth_integer_instr = stackdepther('_integer')
stack_depth_float_instr = stackdepther('_float')
stack_depth_code_instr = stackdepther('_code')
stack_depth_boolean_instr = stackdepther('_boolean')
stack_depth_string_instr = stackdepther('_string')
stack_depth_char_instr = stackdepther('_char')
# <instr_open>
# <instr_name>exec_stack_depth
# <instr_desc>Pushes the depth of the `exec` stack to the `integer` stack.
# <instr_close>
# <instr_open>
# <instr_name>integer_stack_depth
# <instr_desc>Pushes the depth of the `integer` stack to the `integer` stack.
# <instr_close>
# <instr_open>
# <instr_name>float_stack_depth
# <instr_desc>Pushes the depth of the `float` stack to the `integer` stack.
# <instr_close>
# <instr_open>
# <instr_name>code_stack_depth
# <instr_desc>Pushes the depth of the `code` stack to the `integer` stack.
# <instr_close>
# <instr_open>
# <instr_name>boolean_stack_depth
# <instr_desc>Pushes the depth of the `boolean` stack to the `integer` stack.
# <instr_close>
# <instr_open>
# <instr_name>string_stack_depth
# <instr_desc>Pushes the depth of the `string` stack to the `integer` stack.
# <instr_close>
# <instr_open>
# <instr_name>char_stack_depth
# <instr_desc>Pushes the depth of the `char` stack to the `integer` stack.
# <instr_close>


def yanker(pysh_type):
    '''
    Returns an instruction that yanks an item from deep in the specified stack,
    using the top integer to indicate how deep.
    '''
    def yank(state):
        a = pysh_type == '_integer' and len(state[pysh_type]) > 1
        b = pysh_type != '_integer' and len(
            state[pysh_type]) > 0 and len(state['_integer']) > 0
        if a or b:
            raw_index = state['_integer'].ref(0)
            state['_integer'].pop()
            actual_index = int(
                max(0, min(raw_index, len(state[pysh_type]) - 1)))
            item = state[pysh_type].ref(actual_index)
            del state[pysh_type][-actual_index - 1]
            state[pysh_type].push(item)
    instruction = instr.PyshInstruction(pysh_type + '_yank',
                                        yank,
                                        stack_types=[pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 0
    if not pysh_type == '_integer':
        instruction.stack_types.append('_integer')
    return instruction


yank_exec_instr = yanker('_exec')
yank_integer_instr = yanker('_integer')
yank_float_instr = yanker('_float')
yank_code_instr = yanker('_code')
yank_boolean_instr = yanker('_boolean')
yank_string_instr = yanker('_string')
yank_char_instr = yanker('_char')
# <instr_open>
# <instr_name>exec_yank
# <instr_desc>Yanks an item from deep in the `exec` stack, using the top `integer` to indicate how deep.
# <instr_close>
# <instr_open>
# <instr_name>integer_yank
# <instr_desc>Yanks an item from deep in the `integer` stack, using the top `integer` to indicate how deep.
# <instr_close>
# <instr_open>
# <instr_name>float_yank
# <instr_desc>Yanks an item from deep in the `float` stack, using the top `integer` to indicate how deep.
# <instr_close>
# <instr_open>
# <instr_name>code_yank
# <instr_desc>Yanks an item from deep in the `code` stack, using the top `integer` to indicate how deep.
# <instr_close>
# <instr_open>
# <instr_name>boolean_yank
# <instr_desc>Yanks an item from deep in the `boolean` stack, using the top `integer` to indicate how deep.
# <instr_close>
# <instr_open>
# <instr_name>string_yank
# <instr_desc>Yanks an item from deep in the `string` stack, using the top `integer` to indicate how deep.
# <instr_close>
# <instr_open>
# <instr_name>char_yank
# <instr_desc>Yanks an item from deep in the `char` stack, using the top `integer` to indicate how deep.
# <instr_close>


def yankduper(pysh_type):
    '''
    Returns an instruction that yanks a copy of an item from deep in the specified stack,
   using the top integer to indicate how deep.
    '''
    def yankdup(state):
        a = pysh_type == '_integer' and len(state[pysh_type]) > 1
        b = pysh_type != '_integer' and len(
            state[pysh_type]) > 0 and len(state['_integer']) > 0
        if a or b:
            raw_index = state['_integer'].ref(0)
            state['_integer'].pop()
            actual_index = int(
                max(0, min(raw_index, len(state[pysh_type]) - 1)))
            item = state[pysh_type].ref(actual_index)
            state[pysh_type].push(item)
    instruction = instr.PyshInstruction(pysh_type + '_yankdup',
                                        yankdup,
                                        stack_types=[pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 0
    if not pysh_type == '_integer':
        instruction.stack_types.append('_integer')
    return instruction


yank_dup_exec_instr = yankduper('_exec')
yank_dup_integer_instr = yankduper('_integer')
yank_dup_float_instr = yankduper('_float')
yank_dup_code_instr = yankduper('_code')
yank_dup_boolean_instr = yankduper('_boolean')
yank_dup_string_instr = yankduper('_string')
yank_dup_char_instr = yankduper('_char')
# <instr_open>
# <instr_name>exec_yankdup
# <instr_desc>Yanks a copy of an item from deep in the `exec` stack, using the top `integer` to indicate how deep.
# <instr_close>
# <instr_open>
# <instr_name>integer_yankdup
# <instr_desc>Yanks a copy of an item from deep in the `integer` stack, using the top `integer` to indicate how deep.
# <instr_close>
# <instr_open>
# <instr_name>float_yankdup
# <instr_desc>Yanks a copy of an item from deep in the `float` stack, using the top `integer` to indicate how deep.
# <instr_close>
# <instr_open>
# <instr_name>code_yankdup
# <instr_desc>Yanks a copy of an item from deep in the `code` stack, using the top `integer` to indicate how deep.
# <instr_close>
# <instr_open>
# <instr_name>boolean_yankdup
# <instr_desc>Yanks a copy of an item from deep in the `boolean` stack, using the top `integer` to indicate how deep.
# <instr_close>
# <instr_open>
# <instr_name>string_yankdup
# <instr_desc>Yanks a copy of an item from deep in the `string` stack, using the top `integer` to indicate how deep.
# <instr_close>
# <instr_open>
# <instr_name>char_yankdup
# <instr_desc>Yanks a copy of an item from deep in the `char` stack, using the top `integer` to indicate how deep.
# <instr_close>


def shover(pysh_type):
    '''
    Returns an instruction that shoves an item deep in the specified stack, using the top
    integer to indicate how deep.
    '''
    def shove(state):
        a = pysh_type == '_integer' and len(state[pysh_type]) > 1
        b = pysh_type != '_integer' and len(
            state[pysh_type]) > 0 and len(state['_integer']) > 0
        if a or b:
            raw_index = state['_integer'].ref(0)
            state['_integer'].pop()
            item = state[pysh_type].ref(0)
            state[pysh_type].pop()
            actual_index = int(max(0, min(raw_index, len(state[pysh_type]))))
            state[pysh_type].insert(actual_index, item)
    instruction = instr.PyshInstruction(pysh_type + '_shove',
                                        shove,
                                        stack_types=[pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 1
    if not pysh_type == '_integer':
        instruction.stack_types.append('_integer')
    return instruction


shove_exec_instr = shover('_exec')
shove_integer_instr = shover('_integer')
shove_float_instr = shover('_float')
shove_code_instr = shover('_code')
shove_boolean_instr = shover('_boolean')
shove_string_instr = shover('_string')
shove_char_instr = shover('_char')
# <instr_open>
# <instr_name>exec_shove
# <instr_desc>Shoves an item deep in the `exec` stack, using the top `integer` to indicate how deep.
# <instr_close>
# <instr_open>
# <instr_name>integer_shove
# <instr_desc>Shoves an item deep in the `integer` stack, using the top `integer` to indicate how deep.
# <instr_close>
# <instr_open>
# <instr_name>float_shove
# <instr_desc>Shoves an item deep in the `float` stack, using the top `integer` to indicate how deep.
# <instr_close>
# <instr_open>
# <instr_name>code_shove
# <instr_desc>Shoves an item deep in the `code` stack, using the top `integer` to indicate how deep.
# <instr_close>
# <instr_open>
# <instr_name>boolean_shove
# <instr_desc>Shoves an item deep in the `boolean` stack, using the top `integer` to indicate how deep.
# <instr_close>
# <instr_open>
# <instr_name>string_shove
# <instr_desc>Shoves an item deep in the `string` stack, using the top `integer` to indicate how deep.
# <instr_close>
# <instr_open>
# <instr_name>char_shove
# <instr_desc>Shoves an item deep in the `char` stack, using the top `integer` to indicate how deep.
# <instr_close>


def emptyer(pysh_type):
    '''
    Returns an instruction that takes a state and tells whether that stack is empty.
    '''
    def empty(state):
        state['_boolean'].push(len(state[pysh_type]) == 0)
    instruction = instr.PyshInstruction(pysh_type + '_empty',
                                        empty,
                                        stack_types=[pysh_type])
    if not pysh_type == '_boolean':
        instruction.stack_types.append('_boolean')
    return instruction


empty_exec_instr = emptyer('_exec')
empty_integer_instr = emptyer('_integer')
empty_float_instr = emptyer('_float')
empty_code_instr = emptyer('_code')
empty_boolean_instr = emptyer('_boolean')
empty_string_instr = emptyer('_string')
empty_char_instr = emptyer('_char')
# <instr_open>
# <instr_name>exec_empty
# <instr_desc>Pushes True if the `exec` stack is empty. Pushes False otherwise.
# <instr_close>
# <instr_open>
# <instr_name>integer_empty
# <instr_desc>Pushes True if the `integer` stack is empty. Pushes False otherwise.
# <instr_close>
# <instr_open>
# <instr_name>float_empty
# <instr_desc>Pushes True if the `float` stack is empty. Pushes False otherwise.
# <instr_close>
# <instr_open>
# <instr_name>code_empty
# <instr_desc>Pushes True if the `code` stack is empty. Pushes False otherwise.
# <instr_close>
# <instr_open>
# <instr_name>boolean_empty
# <instr_desc>Pushes True if the `boolean` stack is empty. Pushes False otherwise.
# <instr_close>
# <instr_open>
# <instr_name>string_empty
# <instr_desc>Pushes True if the `string` stack is empty. Pushes False otherwise.
# <instr_close>
# <instr_open>
# <instr_name>char_empty
# <instr_desc>Pushes True if the `char` stack is empty. Pushes False otherwise.
# <instr_close>
