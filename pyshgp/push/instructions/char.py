# -*- coding: utf-8 -*-
"""
Created on 9/29/2016

@author: Eddie
"""
from ... import utils as u

from .. import instruction as instr


def char_all_from_string(state):
    if len(state['_string']) > 0:
        char_list = state['_string'].ref(0)[::-1]
        state['_string'].pop()
        for c in char_list:
            new_char = u.Character(c)
            state['_char'].push(new_char)
char_all_from_string_instruction = instr.PyshInstruction('_char_all_from_string',
                                                          char_all_from_string,
                                                          stack_types = ['_string', '_char'])
# <instr_open>
# <instr_name>char_all_from_string
# <instr_desc>Pushes every charecter of the top `string` to the `char` stack.
# <instr_close>


def char_from_integer(state):
    if len(state['_integer']) > 0:
        new_char = chr(state['_integer'].ref(0) % 128)
        new_char = u.Character(new_char)
        state['_integer'].pop()
        state['_char'].push(new_char)
char_from_integer_instruction = instr.PyshInstruction('_char_from_integer',
                                                       char_from_integer,
                                                       stack_types = ['_integer', '_char'])
# <instr_open>
# <instr_name>char_from_integer
# <instr_desc>Push the top `integer` converted to a `char`.
# <instr_close>


def char_from_float(state):
    if len(state['_float']) > 0:
        new_char = chr(int(state['_float'].ref(0)) % 128)
        new_char = u.Character(new_char)
        state['_float'].pop()
        state['_char'].push(new_char)
char_from_float_instruction = instr.PyshInstruction('_char_from_float',
                                                     char_from_float,
                                                     stack_types = ['_float', '_char'])
# <instr_open>
# <instr_name>char_from_float
# <instr_desc>Push the top `float` converted to a `char`.
# <instr_close>


def char_is_letter(state):
    if len(state['_char']) > 0:
        top_char = state['_char'].ref(0).char
        new_bool = top_char.isalpha()
        state['_char'].pop()
        state['_boolean'].push(new_bool)
char_is_letter_instruction = instr.PyshInstruction('_char_is_letter',
                                                     char_is_letter,
                                                     stack_types = ['_boolean', '_char'])
# <instr_open>
# <instr_name>char_is_letter
# <instr_desc>Pushes True if top `char` is a letter. Pushes False otherwise.
# <instr_close>


def char_is_digit(state):
    if len(state['_char']) > 0:
        top_char = state['_char'].ref(0).char
        new_bool = top_char.isdigit()
        state['_char'].pop()
        state['_boolean'].push(new_bool)
char_is_digit_instruction = instr.PyshInstruction('_char_is_digit',
                                                  char_is_digit,
                                                  stack_types = ['_boolean', '_char'])
# <instr_open>
# <instr_name>char_is_digit
# <instr_desc>Pushes True if top `char` is a digit. Pushes False otherwise.
# <instr_close>


def char_is_white_space(state):
    if len(state['_char']) > 0:
        top_char = state['_char'].ref(0).char
        new_bool = top_char.isspace()
        state['_char'].pop()
        state['_boolean'].push(new_bool)
char_is_white_space_instruction = instr.PyshInstruction('_char_is_white_space',
                                                        char_is_white_space,
                                                        stack_types = ['_boolean', '_char'])
# <instr_open>
# <instr_name>char_is_white_space
# <instr_desc>Pushes True if top `char` is a whitespace character. Pushes False otherwise.
# <instr_close>
