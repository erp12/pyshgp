# -*- coding: utf-8 -*-
"""
Created on July 23, 2016

@author: Eddie
"""
from .. instruction import Instruction


def popper(pysh_type):
    '''
    Returns an instruction that takes a state and pops the appropriate
    stack of the state.
    '''
    def pop(state):
        if len(state[pysh_type]) > 0:
            state[pysh_type].pop()
    instruction = Instruction(pysh_type + '_pop',
                              pop,
                              stack_types=[pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 1
    return instruction


I_pop_exec = popper('_exec')
I_pop_integer = popper('_integer')
I_pop_float = popper('_float')
I_pop_code = popper('_code')
I_pop_boolean = popper('_boolean')
I_pop_string = popper('_string')
I_pop_char = popper('_char')
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
    instruction = Instruction(pysh_type + '_dup',
                              dup,
                              stack_types=[pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 1
    return instruction


I_dup_exec = duper('_exec')
I_dup_integer = duper('_integer')
I_dup_float = duper('_float')
I_dup_code = duper('_code')
I_dup_boolean = duper('_boolean')
I_dup_string = duper('_string')
I_dup_char = duper('_char')
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
    instruction = Instruction(pysh_type + '_swap',
                              swap,
                              stack_types=[pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 2
    return instruction


I_swap_exec = swapper('_exec')
I_swap_integer = swapper('_integer')
I_swap_float = swapper('_float')
I_swap_code = swapper('_code')
I_swap_boolean = swapper('_boolean')
I_swap_string = swapper('_string')
I_swap_char = swapper('_char')
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
    instruction = Instruction(pysh_type + '_rot',
                              rot,
                              stack_types=[pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 3
    return instruction


I_rot_exec = rotter('_exec')
I_rot_integer = rotter('_integer')
I_rot_float = rotter('_float')
I_rot_code = rotter('_code')
I_rot_boolean = rotter('_boolean')
I_rot_string = rotter('_string')
I_rot_char = rotter('_char')
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
    instruction = Instruction(pysh_type + '_flush',
                              flush,
                              stack_types=[pysh_type])
    return instruction


I_flush_exec = flusher('_exec')
I_flush_integer = flusher('_integer')
I_flush_float = flusher('_float')
I_flush_code = flusher('_code')
I_flush_boolean = flusher('_boolean')
I_flush_string = flusher('_string')
I_flush_char = flusher('_char')
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
    instruction = Instruction(pysh_type + '_eq',
                              eq,
                              stack_types=[pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 0
    if not pysh_type == '_boolean':
        instruction.stack_types.append('_boolean')
    return instruction


I_eq_exec = eqer('_exec')
I_eq_integer = eqer('_integer')
I_eq_float = eqer('_float')
I_eq_code = eqer('_code')
I_eq_boolean = eqer('_boolean')
I_eq_string = eqer('_string')
I_eq_char = eqer('_char')
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
    instruction = Instruction(pysh_type + '_stack_depth',
                              stackdepth,
                              stack_types=[pysh_type])
    if not pysh_type == '_integer':
        instruction.stack_types.append('_integer')
    return instruction


I_stack_depth_exec = stackdepther('_exec')
I_stack_depth_integer = stackdepther('_integer')
I_stack_depth_float = stackdepther('_float')
I_stack_depth_code = stackdepther('_code')
I_stack_depth_boolean = stackdepther('_boolean')
I_stack_depth_string = stackdepther('_string')
I_stack_depth_char = stackdepther('_char')
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
    instruction = Instruction(pysh_type + '_yank',
                              yank,
                              stack_types=[pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 0
    if not pysh_type == '_integer':
        instruction.stack_types.append('_integer')
    return instruction


I_yank_exec = yanker('_exec')
I_yank_integer = yanker('_integer')
I_yank_float = yanker('_float')
I_yank_code = yanker('_code')
I_yank_boolean = yanker('_boolean')
I_yank_string = yanker('_string')
I_yank_char = yanker('_char')
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
    instruction = Instruction(pysh_type + '_yankdup',
                              yankdup,
                              stack_types=[pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 0
    if not pysh_type == '_integer':
        instruction.stack_types.append('_integer')
    return instruction


I_yank_dup_exec = yankduper('_exec')
I_yank_dup_integer = yankduper('_integer')
I_yank_dup_float = yankduper('_float')
I_yank_dup_code = yankduper('_code')
I_yank_dup_boolean = yankduper('_boolean')
I_yank_dup_string = yankduper('_string')
I_yank_dup_char = yankduper('_char')
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
    instruction = Instruction(pysh_type + '_shove',
                              shove,
                              stack_types=[pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 1
    if not pysh_type == '_integer':
        instruction.stack_types.append('_integer')
    return instruction


I_shove_exec = shover('_exec')
I_shove_integer = shover('_integer')
I_shove_float = shover('_float')
I_shove_code = shover('_code')
I_shove_boolean = shover('_boolean')
I_shove_string = shover('_string')
I_shove_char = shover('_char')
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
    instruction = Instruction(pysh_type + '_empty',
                              empty,
                              stack_types=[pysh_type])
    if not pysh_type == '_boolean':
        instruction.stack_types.append('_boolean')
    return instruction


I_empty_exec = emptyer('_exec')
I_empty_integer = emptyer('_integer')
I_empty_float = emptyer('_float')
I_empty_code = emptyer('_code')
I_empty_boolean = emptyer('_boolean')
I_empty_string = emptyer('_string')
I_empty_char = emptyer('_char')
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
