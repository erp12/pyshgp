# -*- coding: utf-8 -*-
"""
Created on December 5, 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from ... import utils as u
from ... import constants as c

from .. import instruction as instr

from . import common
from . import registered_instructions as ri

vector_types = ['_integer', '_float', '_boolean', '_string']

##                         ##
#  Instructions for Vectors # 
##                         ##

def newer(vec_type):
    '''
    Returns a function that takes a state and concats two vectors on the type
    stack.
    '''
    t = None
    if vec_type == '_vector_integer':
        t = int
    elif vec_type == '_vector_float':
        t = float
    elif vec_type == '_vector_boolean':
        t = bool
    elif vec_type == '_vector_string':
        t = str

    def new(state):
        if len(state[vec_type])>1:
            state[vec_type].push_item(u.PushVector([], t))
    instruction = instr.PyshInstruction(vec_type + '_new',
                                        new,
                                        stack_types = [vec_type])
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


def concater(vec_type):
    '''
    Returns a function that takes a state and concats two vectors on the type stack.
    '''
    def concat(state):
        if len(state[vec_type])>1:
            first_vec = state[vec_type].ref(0)
            second_vec = state[vec_type].ref(1)
            if c.max_vector_length < len(first_vec) + len(second_vec):
                return state
            state[vec_type].pop_item()
            state[vec_type].pop_item()
            state[vec_type].push_item(u.PushVector(second_vec + first_vec, second_vec.typ))
    instruction = instr.PyshInstruction(vec_type + '_concat',
                                        concat,
                                        stack_types = [vec_type])
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
        if len(state[vec_type])>0 and len(state[lit_type])>0:
            v = state[vec_type].ref(0)
            result = v + [state[lit_type].ref(0)]
            if c.max_vector_length < len(result):
                return state
            state[vec_type].pop_item()
            state[lit_type].pop_item()
            state[vec_type].push_item(u.PushVector(result, v.typ))
    instruction = instr.PyshInstruction(vec_type + '_append',
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
        if len(state[vec_type]) > 0 and len(state['_integer']) > 0:
            v = state[vec_type].ref(0)
            result = v[:state['_integer'].ref(0)]
            state[vec_type].pop_item()
            state['_integer'].pop_item()
            state[vec_type].push_item(u.PushVector(result, v.typ))
    instruction = instr.PyshInstruction(vec_type + '_take',
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
        if len(state[vec_type])>0 and len(state['_integer'])>1:
            result = state[vec_type].ref(0)
            t = result.typ
            i = state['_integer'].ref(1)
            j = state['_integer'].ref(0)
            result = result[i:j]
            state[vec_type].pop_item()
            state['_integer'].pop_item()
            state['_integer'].pop_item()
            state[vec_type].push_item(u.PushVector(result, t))
    instruction = instr.PyshInstruction(vec_type + '_subvec',
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
        if len(state[vec_type]) > 0 and len(state[vec_type].ref(0)) > 0:
            result = state[vec_type].ref(0)[0]
            state[vec_type].pop_item()
            state[lit_type].push_item(result)
    instruction = instr.PyshInstruction(vec_type + '_first',
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
        if len(state[vec_type]) > 0 and len(state[vec_type].ref(0)) > 0:
            result = state[vec_type].ref(0)[-1]
            state[vec_type].pop_item()
            state[lit_type].push_item(result)
    instruction = instr.PyshInstruction(vec_type + '_last',
                                        last,
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
        if len(state[vec_type]) > 0 and len(state[vec_type].ref(0)) > 0 and len(state['_integer']):
            i = state['_integer'].ref(0) % len(state[vec_type].ref(0))
            result = state[vec_type].ref(0)[i]
            state[vec_type].pop_item()
            state['_integer'].pop_item()
            state[lit_type].push_item(result)
    instruction = instr.PyshInstruction(vec_type + '_nth',
                                         nth,
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
        if len(state[vec_type]) > 0:
            v = state[vec_type].ref(0)
            t = v.typ
            result = v[1:]
            state[vec_type].pop_item()
            state[vec_type].push_item(u.PushVector(result, t)) 
    instruction = instr.PyshInstruction(vec_type + '_rest',
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
        if len(state[vec_type]) > 0:
            v = state[vec_type].ref(0)
            t = v.typ
            result = v[:-1]
            state[vec_type].pop_item()
            state[vec_type].push_item(u.PushVector(result, t))
    instruction = instr.PyshInstruction(vec_type + '_butlast',
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
        if len(state[vec_type]) > 0:
            result = len(state[vec_type].ref(0))
            state[vec_type].pop_item()
            state['_integer'].push_item(result)
    instruction = instr.PyshInstruction(vec_type + '_length',
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
        if len(state[vec_type]) > 0:
            v =  state[vec_type].ref(0)
            t = v.typ
            result = v[::-1]
            state[vec_type].pop_item()
            state[vec_type].push_item(u.PushVector(result, t))
    instruction = instr.PyshInstruction(vec_type + '_reverse',
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
        if len(state[vec_type]) > 0:
            l = state[vec_type].ref(0)
            state[vec_type].pop_item()
            for el in l[::-1]:
                state[lit_type].push_item(el)
    instruction = instr.PyshInstruction(vec_type + '_pushall',
                                         pushall,
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
        if len(state[vec_type]) > 0:
            l = state[vec_type].ref(0)
            state[vec_type].pop_item()
            if len(l) == 0:
                state['_boolean'].push_item(True)
            else:
                state['_boolean'].push_item(False)
    instruction = instr.PyshInstruction(vec_type + '_emptyvector',
                                         emptyvector,
                                         stack_types = [vec_type, '_boolean'])
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


def containser(vec_type, lit_type):
    '''
    Returns a function that takes a state and tells whether the top lit_type item
    is in the top type vector.
    '''
    def contains(state):
        if len(state[vec_type]) > 0 and len(state[lit_type]) > 0:
            b = state[lit_type].ref(0) in state[vec_type].ref(0)
            state[vec_type].pop_item()
            state[lit_type].pop_item()
            state['_boolean'].push_item(b)
    instruction = instr.PyshInstruction(vec_type + '_contains',
                                         contains,
                                         stack_types = [vec_type, lit_type, '_boolean'])
    return instruction
#<instr_open>
#<instr_name>_vector_integer_contains
#<instr_desc>Pushes ``True`` if top ``integer`` is in the top ``integer vector``. Pushes ``False`` otherwise.
#<instr_close>
#<instr_open>
#<instr_name>_vector_float_contains
#<instr_desc>Pushes ``True`` if top ``integer`` is in the top ``integer vector``. Pushes ``False`` otherwise.
#<instr_close>
#<instr_open>
#<instr_name>_vector_string_contains
#<instr_desc>Pushes ``True`` if top ``integer`` is in the top ``integer vector``. Pushes ``False`` otherwise.
#<instr_close>
#<instr_open>
#<instr_name>_vector_boolean_contains
#<instr_desc>Pushes ``True`` if top ``integer`` is in the top ``integer vector``. Pushes ``False`` otherwise.
#<instr_close>
#<instr_open>


def indexofer(vec_type, lit_type):
    '''
    Returns a function that takes a state and finds the index of the top lit-type
    item in the top type vector.
    '''
    def indexof(state):
        if len(state[vec_type]) > 0 and len(state[lit_type]) > 0:
            b = state[lit_type].ref(0) in state[vec_type].ref(0)
            i = None
            if not b:
                i = -1
            else:
                i = state[vec_type].ref(0).index(state[lit_type].ref(0))
            state[vec_type].pop_item()
            state[lit_type].pop_item()
            state['_integer'].push_item(i)
    instruction = instr.PyshInstruction(vec_type + '_indexof',
                                         indexof,
                                         stack_types = [vec_type, lit_type, '_integer'])
    return instruction
#<instr_open>
#<instr_name>_vector_integer_indexof
#<instr_desc>Pushes the index of the top ``integer`` in the top ``integer vector``. Pushes ``-1`` if top ``integer`` is not in the top ``integer vector``.
#<instr_close>
#<instr_open>
#<instr_name>_vector_float_indexof
#<instr_desc>Pushes the index of the top ``float`` in the top ``float vector``. Pushes ``-1`` if top ``float`` is not in the top ``float vector``.
#<instr_close>
#<instr_open>
#<instr_name>_vector_string_indexof
#<instr_desc>Pushes the index of the top ``string`` in the top ``string vector``. Pushes ``-1`` if top ``string`` is not in the top ``string vector``.
#<instr_close>
#<instr_open>
#<instr_name>_vector_boolean_indexof
#<instr_desc>Pushes the index of the top ``boolean`` n the top ``boolean vector``. Pushes ``-1`` if top ``boolean`` is not in the top ``boolean vector``.
#<instr_close>
#<instr_open>


def occurrencesofer(vec_type, lit_type):
    '''
    Returns a function that takes a state and counts the occurrences of the top lit_type
    item in the top type vector.
    '''
    def occurrencesof(state):
        if len(state[vec_type]) > 0 and len(state[lit_type]) > 0:
            l = [x for x in state[vec_type].ref(0) if x == state[lit_type].ref(0)]
            state[vec_type].pop_item()
            state[lit_type].pop_item()
            state['_integer'].push_item(len(l))
    instruction = instr.PyshInstruction(vec_type + '_occurrencesof',
                                         occurrencesof,
                                         stack_types = [vec_type, lit_type, '_integer'])
    return instruction
#<instr_open>
#<instr_name>_vector_integer_occurrencesof
#<instr_desc>Pushes the number of occurrences of the top ``integer`` in the top ``integer vector``.
#<instr_close>
#<instr_open>
#<instr_name>_vector_float_occurrencesof
#<instr_desc>Pushes the number of occurrences of the top ``float`` in the top ``float vector``.
#<instr_close>
#<instr_open>
#<instr_name>_vector_string_occurrencesof
#<instr_desc>Pushes the number of occurrences of the top ``string`` in the top ``string vector``.
#<instr_close>
#<instr_open>
#<instr_name>_vector_boolean_occurrencesof
#<instr_desc>Pushes the number of occurrences of the top ``boolean`` in the top ``boolean vector``.
#<instr_close>
#<instr_open>


def seter(vec_type, lit_type):
    '''
    Returns a function that takes a state and replaces, in the top type vector,
    item at index (from integer stack) with the first lit_type item.
    '''
    def _set(state):
        if len(state[vec_type])>0 and len(state[lit_type])>0 and len(state['_integer'])>0:
            v = state[vec_type].ref(0)
            t = v.typ
            item = None
            if lit_type == '_integer':
                if len(state['_integer'])<2:
                    return
                item = state['_integer'].ref(1)
            else:
                item = state[lit_type].ref(0)

            index = 0
            result = v[:]
            if len(v) > 0:
                index = state['_integer'].ref(0) % len(v)
                result[index] = item
                
            state[vec_type].pop_item()
            state[lit_type].pop_item()
            state['_integer'].pop_item()
            state[vec_type].push_item(u.PushVector(result, t))
    instruction = instr.PyshInstruction(vec_type + '_set',
                                         _set,
                                         stack_types = [vec_type, lit_type])
    if not lit_type == '_integer':
        instruction.stack_types.append('_integer')
    return instruction
#<instr_open>
#<instr_name>_vector_integer_set
#<instr_desc>Pushes the top ``integer vector`` with its ``i``th element set to the second ``integer``. ``i`` is the top integer.
#<instr_close>
#<instr_open>
#<instr_name>_vector_float_set
#<instr_desc>Pushes the top ``float vector`` with its ``i``th element set to the second ``float``. ``i`` is the top integer.
#<instr_close>
#<instr_open>
#<instr_name>_vector_string_set
#<instr_desc>Pushes the top ``string vector`` with its ``i``th element set to the second ``string``. ``i`` is the top integer.
#<instr_close>
#<instr_open>
#<instr_name>_vector_boolean_set
#<instr_desc>Pushes the top ``boolean vector`` with its ``i``th element set to the second ``boolean``. ``i`` is the top integer.
#<instr_close>
#<instr_open>


def replaceer(vec_type, lit_type):
    '''
    Returns a function that takes a state and replaces all occurrences of the second lit-type item
    with the first lit-type item in the top type vector.
    '''
    def _replace(state):
        if len(state[vec_type])>0 and len(state[lit_type])>1:
            v = state[vec_type].ref(0)
            t = v.typ
            replace_this = state[lit_type].ref(1)
            with_this = state[lit_type].ref(0)
            result = [with_this if x == replace_this else x for x in v]

            state[vec_type].pop_item()
            state[lit_type].pop_item()
            state[lit_type].pop_item()
            state[vec_type].push_item(u.PushVector(result, t))

    instruction = instr.PyshInstruction(vec_type + '_replace',
                                         _replace,
                                         stack_types = [vec_type, lit_type])
    return instruction
#<instr_open>
#<instr_name>_vector_integer_replace
#<instr_desc>Pushes the top ``integer vector`` with all occurrences of the second ``integer`` replaced with the top ``integer``.
#<instr_open>
#<instr_name>_vector_float_replace
#<instr_desc>Pushes the top ``float vector`` with all occurrences of the second ``float`` replaced with the top ``float``.
#<instr_close>
#<instr_open>
#<instr_name>_vector_string_replace
#<instr_desc>Pushes the top ``string vector`` with all occurrences of the second ``string`` replaced with the top ``string``.
#<instr_close>
#<instr_open>
#<instr_name>_vector_boolean_replace
#<instr_desc>Pushes the top ``boolean vector`` with all occurrences of the second ``boolean`` replaced with the top ``boolean``.
#<instr_close>
#<instr_open>


def replacefirster(vec_type, lit_type):
    '''
    Returns a function that takes a state and replaces the first occurrence of the second lit-type item
    with the first lit-type item in the top type vector.
    '''
    def replacefirst(state):
        if len(state[vec_type]) > 0 and len(state[lit_type])>1:
            v = state[vec_type].ref(0)
            t = v.typ
            replace_this = state[lit_type].ref(1)
            with_this = state[lit_type].ref(0)
            
            result = []
            found  = False
            for el in v:
                if (not found) and el == replace_this:
                    result.append(with_this)
                else:
                    result.append(el)

            state[vec_type].pop_item()
            state[lit_type].pop_item()
            state[lit_type].pop_item()
            state[vec_type].push_item(u.PushVector(result, t))

    instruction = instr.PyshInstruction(vec_type + '_replacefirst',
                                         replacefirst,
                                         stack_types = [vec_type, lit_type])
    return instruction
#<instr_open>
#<instr_name>_vector_integer_replacefirst
#<instr_desc>Pushes the top ``integer vector`` with the first occurrence of the second ``integer`` replaced with the top ``integer``.
#<instr_open>
#<instr_name>_vector_float_replacefirst
#<instr_desc>Pushes the top ``float vector`` with the first occurrence of the second ``float`` replaced with the top ``float``.
#<instr_close>
#<instr_open>
#<instr_name>_vector_string_replacefirst
#<instr_desc>Pushes the top ``string vector`` with the first occurrence of the second ``string`` replaced with the top ``string``.
#<instr_close>
#<instr_open>
#<instr_name>_vector_boolean_replacefirst
#<instr_desc>Pushes the top ``boolean vector`` with the first occurrence of the second ``boolean`` replaced with the top ``boolean``.
#<instr_close>
#<instr_open>


def removeer(vec_type, lit_type):
    '''
    Returns a function that takes a state and removes all occurrences of the first lit-type item
    in the top type vector.
    '''
    def _remove(state):
        if len(state[vec_type])>0 and len(state[lit_type])>0:
            v = state[vec_type].ref(0)
            t = v.typ
            remove_this = state[lit_type].ref(0)
            result = [x for x in v if not x == remove_this]

            state[vec_type].pop_item()
            state[lit_type].pop_item()
            state[vec_type].push_item(u.PushVector(result, t))

    instruction = instr.PyshInstruction(vec_type + '_remove',
                                         _remove,
                                         stack_types = [vec_type, lit_type])
    return instruction
#<instr_open>
#<instr_name>_vector_integer_remove
#<instr_desc>Pushes the top ``integer vector`` with all occurrences of the top ``integer`` removed.
#<instr_open>
#<instr_name>_vector_float_remove
#<instr_desc>Pushes the top ``float vector`` with all occurrences of the top ``float`` removed.
#<instr_close>
#<instr_open>
#<instr_name>_vector_string_remove
#<instr_desc>Pushes the top ``string vector`` with all occurrences of the top ``string`` removed.
#<instr_close>
#<instr_open>
#<instr_name>_vector_boolean_remove
#<instr_desc>Pushes the top ``boolean vector`` with all occurrences of the top ``boolean`` removed.
#<instr_close>


def iterateer(vec_type, lit_type):
    '''
    Returns a function that takes a state and iterates over the type vector using
    code on the exec stack. If the vector isn't empty, expands to:
        ((first vector) (top-item :exec state) (rest vector) exec_do*vector_type (top-item :exec state) rest_of_program)
    '''
    instr_name = '_exec_do*' + vec_type[1:]
    def _iter(state):
        if len(state[vec_type]) > 0 and len(state['_exec']) > 0:
            v = state[vec_type].ref(0)
            e = state['_exec'].ref(0)
            
            if len(v) == 0:
                state[vec_type].pop_item()
                state['_exec'].pop_item()
            elif len(v) == 1: #If the rest of the vector is empty, we're done iterating.
                state[vec_type].pop_item()
                state[lit_type].push_item(v[0])
            else:
                state[vec_type].pop_item()
                state['_exec'].push_item(instr.JustInTimeInstruction(instr_name))
                state['_exec'].push_item(u.PushVector(v[1:], v.typ))
                state['_exec'].push_item(e)
                state[lit_type].push_item(v[0])

    instruction = instr.PyshInstruction(instr_name,
                                         _iter,
                                         stack_types = [vec_type, lit_type])
    return instruction
#<instr_open>
#<instr_name>_exec_do*vector_integer
#<instr_desc>Iterates over the top ``integer vector`` using code on the top of the ``exec stack``.
#<instr_open>
#<instr_name>_exec_do*vector_float
#<instr_desc>Iterates over the top ``float vector`` using code on the top of the ``exec stack``.
#<instr_close>
#<instr_open>
#<instr_name>_exec_do*vector_string
#<instr_desc>Iterates over the top ``string vector`` using code on the top of the ``exec stack``.
#<instr_close>
#<instr_open>
#<instr_name>_exec_do*vector_boolean
#<instr_desc>Iterates over the top ``boolean vector`` using code on the top of the ``exec stack``.
#<instr_close>


##                                ##
# Register All Vector Instructions #
##                                ##

for t in vector_types:
    # stack instructions for vectors
    ri.register_instruction(common.popper('_vector'+t))
    ri.register_instruction(common.duper('_vector'+t))
    ri.register_instruction(common.swapper('_vector'+t))
    ri.register_instruction(common.rotter('_vector'+t))
    ri.register_instruction(common.flusher('_vector'+t))
    ri.register_instruction(common.eqer('_vector'+t))
    ri.register_instruction(common.stackdepther('_vector'+t))
    ri.register_instruction(common.yanker('_vector'+t))
    ri.register_instruction(common.yankduper('_vector'+t))
    ri.register_instruction(common.shover('_vector'+t))
    ri.register_instruction(common.emptyer('_vector'+t))
    # common instructions for vectors
    ri.register_instruction(concater('_vector'+t))
    ri.register_instruction(appender('_vector'+t, t))
    ri.register_instruction(taker('_vector'+t))
    ri.register_instruction(subvecer('_vector'+t))
    ri.register_instruction(firster('_vector'+t, t))
    ri.register_instruction(laster('_vector'+t, t))
    ri.register_instruction(nther('_vector'+t, t))
    ri.register_instruction(rester('_vector'+t))
    ri.register_instruction(butlaster('_vector'+t))
    ri.register_instruction(lengther('_vector'+t))
    ri.register_instruction(reverser('_vector'+t))
    ri.register_instruction(pushaller('_vector'+t, t))
    ri.register_instruction(emptyvectorer('_vector'+t))
    ri.register_instruction(containser('_vector'+t, t))
    ri.register_instruction(indexofer('_vector'+t, t))
    ri.register_instruction(occurrencesofer('_vector'+t, t))
    ri.register_instruction(seter('_vector'+t, t))
    ri.register_instruction(replaceer('_vector'+t, t))
    ri.register_instruction(replacefirster('_vector'+t, t))
    ri.register_instruction(removeer('_vector'+t, t))
    ri.register_instruction(iterateer('_vector'+t, t))
