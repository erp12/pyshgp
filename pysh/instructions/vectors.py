# -*- coding: utf-8 -*-
"""
Created on December 5, 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from . import registered_instructions
from .. import pysh_globals as g


vector_types = ['_integer', '_float', '_boolean', '_string']


##                         ##
#  Instructions for Vectors # 
##                         ##

def concater(pysh_type):
    '''
    Returns a function that takes a state and concats two vectors on the type stack.
    '''
    def concat(state):
        if len(state.stacks[pysh_type])>1:
            first_vec = state.stacks[pysh_type].stack_ref(0)
            second_vec = state.stacks[pysh_type].stack_ref(1)
            if g.max_vector_length < len(first_vec) + len(second_vec):
                return state
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].pop_item()
            state.stacks[pysh_type].push_item(second_vec+first_vec)
    instruction = instr.Pysh_Instruction(pysh_type[1:] + '_concat',
                                         concat,
                                         stack_types = [pysh_type])
    return instruction
#<instr_open>
#<instr_name>_vector_integer_concat
#<instr_desc>Concats the top two ``integer vectors`` and pushes the resulting ``integer vector``.
#<instr_close>
#<instr_open>
#<instr_name>_vector_float_concat
#<instr_desc>Concats the top two ``float vectors`` and pushes the resulting ``float vector``.
#<instr_close>
#<instr_open>
#<instr_name>_vector_string_concat
#<instr_desc>Concats the top two ``string vectors`` and pushes the resulting ``string vector``.
#<instr_close>
#<instr_open>
#<instr_name>_vector_boolean_concat
#<instr_desc>Concats the top two ``boolean vectors`` and pushes the resulting ``boolean vector``.
#<instr_close>
#<instr_open>


def appender(vec_type, lit_type):
    '''
    Returns a function that takes a state and appends an item onto the type stack.
    '''
    def append(state):
        if len(state.stacks[vec_type])>0 and len(state.stacks[lit_type])>0:
            result = state.stacks[vec_type].stack_ref(0)+[state.stacks[lit_type].stack_ref(0)]
            if g.max_vector_length < len(result):
                return state
            state.stacks[vec_type].pop_item()
            state.stacks[lit_type].pop_item()
            state.stacks[vec_type].push_item(result)
    instruction = instr.Pysh_Instruction(vec_type[1:] + '_append',
                                         append,
                                         stack_types = [vec_type, lit_type])
    return instruction
#<instr_open>
#<instr_name>_vector_integer_append
#<instr_desc>Appends the top ``integer`` onto the top ``integer vector`` and pushes the resulting ``integer vector``.
#<instr_close>
#<instr_open>
#<instr_name>_vector_float_append
#<instr_desc>Appends the top ``float`` onto the top ``float vector`` and pushes the resulting ``float vector``.
#<instr_close>
#<instr_open>
#<instr_name>_vector_string_append
#<instr_desc>Appends the top ``string`` onto the top ``string vector`` and pushes the resulting ``string vector``.
#<instr_close>
#<instr_open>
#<instr_name>_vector_boolean_append
#<instr_desc>Appends the top ``boolean`` onto the top ``boolean vector`` and pushes the resulting ``boolean vector``.
#<instr_close>
#<instr_open>


def taker(vec_type):
    '''
    Returns a function that takes a state and appends an item onto the type stack.
    '''
    def take(state):
        if len(state.stacks[vec_type])>0 and len(state.stacks['_integer'])>0:
            result = state.stacks[vec_type].stack_ref(0)[:state.stacks[lit_type].stack_ref(0)]
            state.stacks[vec_type].pop_item()
            state.stacks['_integer'].pop_item()
            state.stacks[vec_type].push_item(result)
    instruction = instr.Pysh_Instruction(vec_type[1:] + '_take',
                                         take,
                                         stack_types = [vec_type, '_integer'])
    return instruction
#<instr_open>
#<instr_name>_vector_integer_take
#<instr_desc>Takes the first ``n`` items from the top ``integer vector`` and pushes the resulting ``integer vector``. ``n`` comes from the top item on the ``integer`` stack.
#<instr_close>
#<instr_open>
#<instr_name>_vector_float_take
#<instr_desc>Takes the first ``n`` items from the top ``float vector`` and pushes the resulting ``float vector``. ``n`` comes from the top item on the ``integer`` stack.
#<instr_close>
#<instr_open>
#<instr_name>_vector_string_take
#<instr_desc>Takes the first ``n`` items from the top ``string vector`` and pushes the resulting ``string vector``. ``n`` comes from the top item on the ``integer`` stack.
#<instr_close>
#<instr_open>
#<instr_name>_vector_boolean_take
#<instr_desc>Takes the first ``n`` items from the top ``boolean vector`` and pushes the resulting ``boolean vector``. ``n`` comes from the top item on the ``integer`` stack.
#<instr_close>
#<instr_open>


def subvecer(vec_type):
    '''
    Returns a function that takes a state and takes the subvec of the top item
    on the type stack.
    '''
    def subvec(state):
        if len(state.stacks[vec_type])>0 and len(state.stacks['_integer'])>1:
            result = state.stacks[vec_type].stack_ref(0)
            i = state.stacks['_integer'].stack_ref(1)
            j = state.stacks['_integer'].stack_ref(0)
            result = result[i:j]
            state.stacks[vec_type].pop_item()
            state.stacks['_integer'].pop_item()
            state.stacks['_integer'].pop_item()
            state.stacks[vec_type].push_item(result)
    instruction = instr.Pysh_Instruction(vec_type[1:] + '_subvec',
                                         subvec,
                                         stack_types = [vec_type, '_integer'])
    return instruction
#<instr_open>
#<instr_name>_vector_integer_subvec
#<instr_desc>Pushes a subvector of the top ``integer vector`` from index ``i`` to ``j``. ``i`` and ``j`` come from the top items on the ``integer`` stack.
#<instr_close>
#<instr_open>
#<instr_name>_vector_float_subvec
#<instr_desc>Pushes a subvector of the top ``float vector`` from index ``i`` to ``j``. ``i`` and ``j`` come from the top items on the ``integer`` stack.
#<instr_close>
#<instr_open>
#<instr_name>_vector_string_subvec
#<instr_desc>Pushes a subvector of the top ``string vector`` from index ``i`` to ``j``. ``i`` and ``j`` come from the top items on the ``integer`` stack.
#<instr_close>
#<instr_open>
#<instr_name>_vector_boolean_subvec
#<instr_desc>Pushes a subvector of the top ``boolean vector`` from index ``i`` to ``j``. ``i`` and ``j`` come from the top items on the ``integer`` stack.
#<instr_close>
#<instr_open>


def firster(vec_type, lit_type):
    '''
    Returns a function that takes a state and gets the first item from the type stack.
    '''
    def first(state):
        if len(state.stacks[vec_type]) > 0 and len(state.stacks[vec_type][0]) > 0:
            result = state.stacks[vec_type].stack_ref(0)[0]
            state.stacks[vec_type].pop_item()
            state.stacks[lit_type].push_item(result)
    instruction = instr.Pysh_Instruction(vec_type[1:] + '_first',
                                         first,
                                         stack_types = [vec_type, lit_type])
    return instruction
#<instr_open>
#<instr_name>_vector_integer_first
#<instr_desc>Pushes the first item of the top ``integer vector`` to the ``integer`` stack.
#<instr_close>
#<instr_open>
#<instr_name>_vector_float_first
#<instr_desc>Pushes the first item of the top ``float vector`` to the ``float`` stack.
#<instr_close>
#<instr_open>
#<instr_name>_vector_string_first
#<instr_desc>Pushes the first item of the top ``string vector`` to the ``string`` stack.
#<instr_close>
#<instr_open>
#<instr_name>_vector_boolean_first
#<instr_desc>Pushes the first item of the top ``boolean vector`` to the ``boolean`` stack.
#<instr_close>
#<instr_open>


def laster(vec_type, lit_type):
    '''
    Returns a function that takes a state and gets the first item from the type stack.
    '''
    def last(state):
        if len(state.stacks[vec_type]) > 0 and len(state.stacks[vec_type][0]) > 0:
            result = state.stacks[vec_type].stack_ref(0)[-1]
            state.stacks[vec_type].pop_item()
            state.stacks[lit_type].push_item(result)
    instruction = instr.Pysh_Instruction(vec_type[1:] + '_last',
                                         first,
                                         stack_types = [vec_type, lit_type])
    return instruction
#<instr_open>
#<instr_name>_vector_integer_last
#<instr_desc>Pushes the last item of the top ``integer vector`` to the ``integer`` stack.
#<instr_close>
#<instr_open>
#<instr_name>_vector_float_last
#<instr_desc>Pushes the last item of the top ``float vector`` to the ``float`` stack.
#<instr_close>
#<instr_open>
#<instr_name>_vector_string_last
#<instr_desc>Pushes the last item of the top ``string vector`` to the ``string`` stack.
#<instr_close>
#<instr_open>
#<instr_name>_vector_boolean_last
#<instr_desc>Pushes the last item of the top ``boolean vector`` to the ``boolean`` stack.
#<instr_close>
#<instr_open>


def nther(vec_type, lit_type):
    '''
    Returns a function that takes a state and gets the first item from the type stack.
    '''
    def nth(state):
        if len(state.stacks[vec_type]) > 0 and len(state.stacks[vec_type][0]) > 0 and len(state.stacks['_integer']):
            i = state.stacks['_integer'] % len(state.stacks[vec_type].stack_ref(0))
            result = state.stacks[vec_type].stack_ref(0)[i]
            state.stacks[vec_type].pop_item()
            state.stacks['_integer'].pop_item()
            state.stacks[lit_type].push_item(result)
    instruction = instr.Pysh_Instruction(vec_type[1:] + '_nth',
                                         first,
                                         stack_types = [vec_type, lit_type, '_integer'])
    return instruction
#<instr_open>
#<instr_name>_vector_integer_nth
#<instr_desc>Pushes the nth item of the top ``integer vector`` to the ``integer`` stack where n is given by the top ``integer``.
#<instr_close>
#<instr_open>
#<instr_name>_vector_float_nth
#<instr_desc>Pushes the nth item of the top ``float vector`` to the ``float`` stack where n is given by the top ``integer``.
#<instr_close>
#<instr_open>
#<instr_name>_vector_string_nth
#<instr_desc>Pushes the nth item of the top ``string vector`` to the ``string`` stack where n is given by the top ``integer``.
#<instr_close>
#<instr_open>
#<instr_name>_vector_boolean_nth
#<instr_desc>Pushes the nth item of the top ``boolean vector`` to the ``boolean`` stack where n is given by the top ``integer``.
#<instr_close>
#<instr_open>


def rester(vec_type):
    '''
    Returns a function that takes a state and takes the rest of the top item
    on the type stack.
    '''
    def rest(state):
        if len(state.stacks[vec_type]) > 0:
            result = state.stacks[vec_type].stack_ref(0)[1:]
            state.stacks[vec_type].pop_item()
            state.stacks[vec_type].push_item(result)
    instruction = instr.Pysh_Instruction(vec_type[1:] + '_rest',
                                         rest,
                                         stack_types = [vec_type])
    return instruction
#<instr_open>
#<instr_name>_vector_integer_rest
#<instr_desc>Pushes the top ``integer vector`` without its first element.
#<instr_close>
#<instr_open>
#<instr_name>_vector_float_rest
#<instr_desc>Pushes the top ``float vector`` without its first element.
#<instr_close>
#<instr_open>
#<instr_name>_vector_string_rest
#<instr_desc>Pushes the top ``string vector`` without its first element.
#<instr_close>
#<instr_open>
#<instr_name>_vector_boolean_rest
#<instr_desc>Pushes the top ``boolean vector`` without its first element.
#<instr_close>
#<instr_open>

def butlaster(vec_type):
    '''
    Returns a function that takes a state and takes the butlast of the top item
    on the type stack.
    '''
    def butlast(state):
        if len(state.stacks[vec_type]) > 0:
            result = state.stacks[vec_type].stack_ref(0)[:-1]
            state.stacks[vec_type].pop_item()
            state.stacks[vec_type].push_item(result)
    instruction = instr.Pysh_Instruction(vec_type[1:] + '_butlast',
                                         butlast,
                                         stack_types = [vec_type])
    return instruction
#<instr_open>
#<instr_name>_vector_integer_butlast
#<instr_desc>Pushes the top ``integer vector`` without its last element.
#<instr_close>
#<instr_open>
#<instr_name>_vector_float_butlast
#<instr_desc>Pushes the top ``float vector`` without its last element.
#<instr_close>
#<instr_open>
#<instr_name>_vector_string_butlast
#<instr_desc>Pushes the top ``string vector`` without its last element.
#<instr_close>
#<instr_open>
#<instr_name>_vector_boolean_butlast
#<instr_desc>Pushes the top ``boolean vector`` without its last element.
#<instr_close>
#<instr_open>


def lengther(vec_type):
    '''
    Returns a function that takes a state and takes the length of the top item
    on the type stack.
    '''
    def length(state):
        if len(state.stacks[vec_type]) > 0:
            result = len(state.stacks[vec_type].stack_ref(0))
            state.stacks[vec_type].pop_item()
            state.stacks['_integer'].push_item(result)
    instruction = instr.Pysh_Instruction(vec_type[1:] + '_butlast',
                                         length,
                                         stack_types = [vec_type, '_integer'])
    return instruction
#<instr_open>
#<instr_name>_vector_integer_length
#<instr_desc>Pushes the length of the top ``integer vector`` to the ``integer`` stack.
#<instr_close>
#<instr_open>
#<instr_name>_vector_float_length
#<instr_desc>Pushes the length of the top ``float vector`` to the ``integer`` stack.
#<instr_close>
#<instr_open>
#<instr_name>_vector_string_length
#<instr_desc>Pushes the length of the top ``string vector`` to the ``integer`` stack.
#<instr_close>
#<instr_open>
#<instr_name>_vector_boolean_length
#<instr_desc>Pushes the length of the top ``boolean vector`` to the ``integer`` stack.
#<instr_close>
#<instr_open>


def reverser(vec_type):
    '''
    Returns a function that takes a state and takes the reverse of the top item
    on the type stack.
    '''
    def rev(state):
        if len(state.stacks[vec_type]) > 0:
            result = state.stacks[vec_type].stack_ref(0)[::-1]
            state.stacks[vec_type].pop_item()
            state.stacks[vec_type].push_item(result)
    instruction = instr.Pysh_Instruction(vec_type[1:] + '_reverse',
                                         rev,
                                         stack_types = [vec_type])
    return instruction
#<instr_open>
#<instr_name>_vector_integer_reverse
#<instr_desc>Pushes the top ``integer vector`` reversed.
#<instr_close>
#<instr_open>
#<instr_name>_vector_float_reverse
#<instr_desc>Pushes the top ``float vector`` reversed.
#<instr_close>
#<instr_open>
#<instr_name>_vector_string_reverse
#<instr_desc>Pushes the top ``string vector`` reversed.
#<instr_close>
#<instr_open>
#<instr_name>_vector_boolean_reverse
#<instr_desc>Pushes the top ``boolean vector`` reversed.
#<instr_close>
#<instr_open>


def pushaller(vec_type, lit_type):
    '''
    Returns a function that takes a state and pushes every item from the first
    vector onto the appropriate stack.
    '''
    def pushall(state):
        if len(state.stacks[vec_type]) > 0:
            l = state.stacks[vec_type].stack_ref(0)
            state.stacks[vec_type].pop_item()
            for el in l[::-1]:
                state.stacks[lit_type].push_item(el)
    instruction = instr.Pysh_Instruction(vec_type[1:] + '_pushall',
                                         rev,
                                         stack_types = [vec_type, lit_type])
    return instruction
#<instr_open>
#<instr_name>_vector_integer_pushall
#<instr_desc>Pushes all the elements of the top ``integer vector`` to the ``integer`` stack.
#<instr_close>
#<instr_open>
#<instr_name>_vector_float_pushall
#<instr_desc>Pushes all the elements of the top ``float vector`` to the ``float`` stack.
#<instr_close>
#<instr_open>
#<instr_name>_vector_string_pushall
#<instr_desc>Pushes all the elements of the top ``string vector`` to the ``string`` stack.
#<instr_close>
#<instr_open>
#<instr_name>_vector_boolean_pushall
#<instr_desc>Pushes all the elements of the top ``boolean vector`` to the ``boolean`` stack.
#<instr_close>
#<instr_open>


def emptyvectorer(vec_type):
    '''
    Returns a function that takes a state and pushes every item from the first
    vector onto the appropriate stack.
    '''
    def emptyvector(state):
        if len(state.stacks[vec_type]) > 0:
            l = state.stacks[vec_type].stack_ref(0)
            state.stacks[vec_type].pop_item()
            if len(l) == 0:
                state.stacks['_boolean'].push_item(True)
            else:
                state.stacks['_boolean'].push_item(False)
    instruction = instr.Pysh_Instruction(vec_type[1:] + '_emptyvector',
                                         emptyvector,
                                         stack_types = [vec_type, 'boolean'])
    return instruction
#<instr_open>
#<instr_name>_vector_integer_emptyvector
#<instr_desc>Pushes ``True`` if top ``integer vector`` is empty.
#<instr_close>
#<instr_open>
#<instr_name>_vector_float_emptyvector
#<instr_desc>Pushes ``True`` if top ``float vector`` is empty.
#<instr_close>
#<instr_open>
#<instr_name>_vector_string_emptyvector
#<instr_desc>Pushes ``True`` if top ``string vector`` is empty.
#<instr_close>
#<instr_open>
#<instr_name>_vector_boolean_emptyvector
#<instr_desc>Pushes ``True`` if top ``boolean vector`` is empty.
#<instr_close>
#<instr_open>


##                                ##
# Register All Vector Instructions #
##                                ##

for t in vector_types:
    # stack instructions for vectors
    registered_instructions.register_instruction(popper('_vector'+t))
    registered_instructions.register_instruction(duper('_vector'+t))
    registered_instructions.register_instruction(swapper('_vector'+t))
    registered_instructions.register_instruction(rotter('_vector'+t))
    registered_instructions.register_instruction(flusher('_vector'+t))
    registered_instructions.register_instruction(eqer('_vector'+t))
    registered_instructions.register_instruction(stackdepther('_vector'+t))
    registered_instructions.register_instruction(yanker('_vector'+t))
    registered_instructions.register_instruction(yankduper('_vector'+t))
    registered_instructions.register_instruction(shover('_vector'+t))
    registered_instructions.register_instruction(emptyer('_vector'+t))
    # common instructions for vectors
    registered_instructions.register_instruction(concater('_vector'+t))
    registered_instructions.register_instruction(appender('_vector'+t, t))
    registered_instructions.register_instruction(taker('_vector'+t))
    registered_instructions.register_instruction(subvecer('_vector'+t))
    registered_instructions.register_instruction(firster('_vector'+t, t))
    registered_instructions.register_instruction(laster('_vector'+t, t))
    registered_instructions.register_instruction(nther('_vector'+t, t))
    registered_instructions.register_instruction(rester('_vector'+t))
    registered_instructions.register_instruction(butlaster('_vector'+t))
    registered_instructions.register_instruction(lengther('_vector'+t))
    registered_instructions.register_instruction(reverser('_vector'+t))
    registered_instructions.register_instruction(pushaller('_vector'+t, t))
    registered_instructions.register_instruction(emptyvectorer('_vector'+t))



