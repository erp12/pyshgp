# -*- coding: utf-8 -*-
"""
Created on 9/29/2016

@author: Eddie
"""
from .. import pysh_state
from .. import instruction as instr
from .. import pysh_globals as g
from .. import utils as u

from . import registered_instructions

def char_all_from_string(state):
    if len(state.stacks['_string']) > 0:
        char_list = state.stacks['_string'].stack_ref(0)[::-1]
        state.stacks['_string'].pop_item()
        for c in char_list:
            new_char = g.Character(c)
            state.stacks['_char'].push_item(new_char)
char_all_from_string_instruction = instr.Pysh_Instruction('char_all_from_string',
                                                          char_all_from_string,
                                                          stack_types = ['_string', '_char'])
registered_instructions.register_instruction(char_all_from_string_instruction)
#<instr_open>
#<instr_name>char_all_from_string
#<instr_desc>Pushes every charecter of the top `string` to the `char` stack.
#<instr_close>  


def char_from_integer(state):
    if len(state.stacks['_integer']) > 0:
        new_char = chr(state.stacks['_integer'].stack_ref(0))
        new_char = g.Character(new_char)
        state.stacks['_integer'].pop_item()
        state.stacks['_char'].push_item(new_char)
char_from_integer_instruction = instr.Pysh_Instruction('char_from_integer',
                                                       char_from_integer,
                                                       stack_types = ['_integer', '_char'])
registered_instructions.register_instruction(char_from_integer_instruction)
#<instr_open>
#<instr_name>char_from_integer
#<instr_desc>Push the top `integer` converted to a `char`.
#<instr_close>  


def char_from_float(state):
    if len(state.stacks['_float']) > 0:
        new_char = chr(int(state.stacks['_float'].stack_ref(0)) % 128)
        new_char = g.Character(new_char)
        state.stacks['_float'].pop_item()
        state.stacks['_char'].push_item(new_char)
char_from_float_instruction = instr.Pysh_Instruction('char_from_float',
                                                     char_from_float,
                                                     stack_types = ['_float', '_char'])
registered_instructions.register_instruction(char_from_float_instruction)
#<instr_open>
#<instr_name>char_from_float
#<instr_desc>Push the top `float` converted to a `char`.
#<instr_close>  


def char_is_letter(state):
    if len(state.stacks['_char']) > 0:
        top_char = state.stacks['_char'].stack_ref(0).char
        new_bool = top_char.isalpha()
        state.stacks['_char'].pop_item()
        state.stacks['_boolean'].push_item(new_bool)
char_is_letter_instruction = instr.Pysh_Instruction('char_is_letter',
                                                     char_is_letter,
                                                     stack_types = ['_boolean', '_char'])
registered_instructions.register_instruction(char_is_letter_instruction)
#<instr_open>
#<instr_name>char_is_letter
#<instr_desc>Pushes True if top `char` is a letter. Pushes False otherwise.
#<instr_close>


def char_is_digit(state):
    if len(state.stacks['_char']) > 0:
        top_char = state.stacks['_char'].stack_ref(0).char
        new_bool = top_char.isdigit()
        state.stacks['_char'].pop_item()
        state.stacks['_boolean'].push_item(new_bool)
char_is_digit_instruction = instr.Pysh_Instruction('char_is_digit',
                                                     char_is_digit,
                                                     stack_types = ['_boolean', '_char'])
registered_instructions.register_instruction(char_is_digit_instruction)
#<instr_open>
#<instr_name>char_is_digit
#<instr_desc>Pushes True if top `char` is a digit. Pushes False otherwise.
#<instr_close>


def char_is_white_space(state):
    if len(state.stacks['_char']) > 0:
        top_char = state.stacks['_char'].stack_ref(0).char
        new_bool = top_char.isspace()
        state.stacks['_char'].pop_item()
        state.stacks['_boolean'].push_item(new_bool)
char_is_white_space_instruction = instr.Pysh_Instruction('char_is_white_space',
                                                         char_is_white_space,
                                                         stack_types = ['_boolean', '_char'])
registered_instructions.register_instruction(char_is_white_space_instruction)
#<instr_open>
#<instr_name>char_is_white_space
#<instr_desc>Pushes True if top `char` is a whitespace character. Pushes False otherwise.
#<instr_close>
