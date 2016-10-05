from __future__ import absolute_import, division, print_function, unicode_literals

from .. import pysh_state
from .. import instruction as instr
from .. import utils as u

from . import registered_instructions


def string_from_integer(state):
    if len(state.stacks['_integer']) > 0:
        top_int = state.stacks['_integer'].stack_ref(0)
        state.stacks['_integer'].pop_item()
        state.stacks['_string'].push_item(str(top_int))
    return state
string_from_integer_intruction = instr.Pysh_Instruction('string_from_integer',
                                                                    string_from_integer,
                                                                    stack_types = ['_string', '_integer'])
registered_instructions.register_instruction(string_from_integer_intruction)
#<instr_open>
#<instr_name>string_from_integer
#<instr_desc>Casts the top integer to a string and pushes the result onto the string stack.
#<instr_close>


def string_from_float(state):
    if len(state.stacks['_float']) > 0:
        top_float = state.stacks['_float'].stack_ref(0)
        state.stacks['_float'].pop_item()
        state.stacks['_string'].push_item(str(top_float))
    return state
string_from_float_intruction = instr.Pysh_Instruction('string_from_float',
                                                                    string_from_float,
                                                                    stack_types = ['_string', '_float'])
registered_instructions.register_instruction(string_from_float_intruction)
#<instr_open>
#<instr_name>string_from_float
#<instr_desc>Casts the top float to a string and pushes the result onto the string stack.
#<instr_close>


def string_from_boolean(state):
    if len(state.stacks['_boolean']) > 0:
        top_float = state.stacks['_boolean'].stack_ref(0)
        state.stacks['_boolean'].pop_item()
        state.stacks['_string'].push_item(str(top_float))
    return state
string_from_boolean_intruction = instr.Pysh_Instruction('string_from_boolean',
                                                                    string_from_boolean,
                                                                    stack_types = ['_string', '_boolean'])
registered_instructions.register_instruction(string_from_boolean_intruction)
#<instr_open>
#<instr_name>string_from_boolean
#<instr_desc>Casts the top boolean to a string and pushes the result onto the string stack.
#<instr_close>


def string_concat(state):
    if len(state.stacks['_string']) > 1:
        s1 = state.stacks['_string'].stack_ref(0)
        s2 = state.stacks['_string'].stack_ref(0)
        state.stacks['_string'].pop_item()
        state.stacks['_string'].pop_item()
        state.stacks['_string'].push_item(s1 + s2)
    return state
string_concat_instruction = instr.Pysh_Instruction('string_concat',
                                                               string_concat,
                                                               stack_types = ['_string'])
registered_instructions.register_instruction(string_concat_instruction)
#<instr_open>
#<instr_name>string_concat
#<instr_desc>Pops top 2 strings, and pushes result of concatenating those strings to the string stack.
#<instr_close>


def string_head(state):
    if len(state.stacks['_string']) > 0 and len(state.stacks['_integer']) > 0:
        s = state.stacks['_string'].stack_ref(0)
        i = state.stacks['_integer'].stack_ref(0)
        state.stacks['_string'].pop_item()
        state.stacks['_integer'].pop_item()
        state.stacks['_string'].push_item(s[:i])
    return state
string_head_instruction = instr.Pysh_Instruction('string_head',
                                                             string_head,
                                                             stack_types = ['_string', '_integer'])
registered_instructions.register_instruction(string_head_instruction)
#<instr_open>
#<instr_name>string_head
#<instr_desc>Pushed a string of the first i chars in s. i is top integer. s is top string.
#<instr_close>


def string_tail(state):
    if len(state.stacks['_string']) > 0 and len(state.stacks['_integer']) > 0:
        s = state.stacks['_string'].stack_ref(0)
        i = state.stacks['_integer'].stack_ref(0)
        state.stacks['_string'].pop_item()
        state.stacks['_integer'].pop_item()
        state.stacks['_string'].push_item(s[-i:])
    return state
string_tail_instruction = instr.Pysh_Instruction('string_tail',
                                                             string_tail,
                                                             stack_types = ['_string', '_integer'])
registered_instructions.register_instruction(string_tail_instruction)
#<instr_open>
#<instr_name>string_tail
#<instr_desc>Pushed a string of the last i chars in s. i is top integer. s is top string.
#<instr_close>

def string_split_at_index(state):
    if len(state.stacks['_string']) > 0 and len(state.stacks['_integer']) > 0:
        s = state.stacks['_string'].stack_ref(0)
        i = state.stacks['_integer'].stack_ref(0)
        s_head = s[:i]
        s_tail = s[i:]
        state.stacks['_string'].pop_item()
        state.stacks['_string'].push_item(s_head)
        state.stacks['_string'].push_item(s_tail)
    return state
string_split_at_index_instruction = instr.Pysh_Instruction('string_split_at_index',
                                                                      string_split_at_index,
                                                                      stack_types = ['_string', '_integer'])
#<instr_open>
#<instr_name>string_split_at_index
#<instr_desc>Pushes 2 strings from top string being split at index given by top integer.
#<instr_close>


def string_split_at_str(state):
    if len(state.stacks['_string']) > 1:
        split_on = state.stacks['_string'].stack_ref(1)
        split_this = state.stacks['_string'].stack_ref(0)
        if split_on == "":
            new_strings = split_this
        else:
            new_strings = split_this.split(split_on)
        state.stacks['_string'].pop_item()
        state.stacks['_string'].pop_item()
        for s in new_strings:
            state.stacks['_string'].push_item(s)
    return state
string_split_at_str_instruction = instr.Pysh_Instruction('string_split_at_str',
                                                                    string_split_at_str,
                                                                    stack_types = ['_string'])
registered_instructions.register_instruction(string_split_at_str_instruction)
#<instr_open>
#<instr_name>string_split_at_str
#<instr_desc>Pushes 2 strings from top string being split on second string.
#<instr_close>


def string_split_at_space(state):
    if len(state.stacks['_string']) > 0:
        split_this = state.stacks['_string'].stack_ref(0)
        new_strings = split_this.split()
        state.stacks['_string'].pop_item()
        for s in new_strings:
            state.stacks['_string'].push_item(s)
    return state
string_split_at_space_instruction = instr.Pysh_Instruction('string_split_at_space',
                                                                        string_split_at_space,
                                                                        stack_types = ['_string'])
registered_instructions.register_instruction(string_split_at_space_instruction)
#<instr_open>
#<instr_name>string_split_at_space
#<instr_desc>Pushes all strings resulting from spliting top string on space characters.
#<instr_close>


def string_length(state):
    if len(state.stacks['_string']) > 0:
        new_int = len(state.stacks['_string'].stack_ref(0))
        new_int = u.keep_number_reasonable(new_int)
        state.stacks['_string'].pop_item()
        state.stacks['_integer'].push_item(new_int)
    return state
string_length_instruction = instr.Pysh_Instruction('string_length',
                                                                string_length,
                                                                stack_types = ['_string', '_integer'])
registered_instructions.register_instruction(string_length_instruction)
#<instr_open>
#<instr_name>string_length
#<instr_desc>Pushes integer equal to length of top string.
#<instr_close>


def string_reverse(state):
    if len(state.stacks['_string']) > 0:
        s = state.stacks['_string'].stack_ref(0)
        s = s[::-1]
        state.stacks['_string'].pop_item()
        state.stacks['_string'].push_item(s)
    return state
string_reverse_instruction = instr.Pysh_Instruction('string_reverse',
                                                                string_reverse,
                                                                stack_types = ['_string'])
registered_instructions.register_instruction(string_reverse_instruction)
#<instr_open>
#<instr_name>string_reverse
#<instr_desc>Pushes top string reversed.
#<instr_close>


def string_char_at(state):
    if len(state.stacks['_string']) > 0 and len(state.stacks['_integer']) > 0:
        s = state.stacks['_string'].stack_ref(0)
        if len(s) == 0:
            c = ''
        else:
            i = state.stacks['_integer'].stack_ref(0) % len(s)
            c = s[i]
        state.stacks['_string'].pop_item()
        state.stacks['_integer'].pop_item()
        state.stacks['_string'].push_item(c)
    return state
string_char_at_instruction = instr.Pysh_Instruction('string_char_at',
                                                                string_char_at,
                                                                stack_types = ['_string', '_integer'])
registered_instructions.register_instruction(string_char_at_instruction)
#<instr_open>
#<instr_name>string_char_at
#<instr_desc>Pushes string of character in top string at index given by top integer.
#<instr_close>


def string_emptystring(state):
    if len(state.stacks['_string']) > 0:
        s = state.stacks['_string'].stack_ref(0)
        state.stacks['_string'].pop_item()
        if s == "":
            state.stacks['_boolean'].push_item(True)
        else:
            state.stacks['_boolean'].push_item(False)
    return state
string_emptystring_instruction = instr.Pysh_Instruction('string_emptystring',
                                                                    string_emptystring,
                                                                    stack_types = ['_string', '_boolean'])
registered_instructions.register_instruction(string_emptystring_instruction)    
#<instr_open>
#<instr_name>string_emptystring
#<instr_desc>Pushes True if top string is an emptry string. Pushes False otherwise.
#<instr_close>


def string_contains(state): 
    '''
    True if top string is a substring of second string; false otherwise
    '''
    if len(state.stacks['_string']) > 1:
        s1 = state.stacks['_string'].stack_ref(0)
        s2 = state.stacks['_string'].stack_ref(1)
        new_bool = s1 in s2
        state.stacks['_string'].pop_item()
        state.stacks['_string'].pop_item()
        state.stacks['_boolean'].push_item(new_bool)
    return state
string_contains_instruction = instr.Pysh_Instruction('string_contains',
                                                     string_contains,
                                                     stack_types = ['_string', '_boolean'])
registered_instructions.register_instruction(string_contains_instruction)
#<instr_open>
#<instr_name>string_contains
#<instr_desc>Pushes True is second string is a substring of top string. Pushes False otherwise.
#<instr_close>


def string_replace(state):
    '''
    In third string on stack, replaces all occurences of second string with first string
    '''
    if len(state.stacks['_string']) > 2:
        replace_this = state.stacks['_string'].stack_ref(1)
        with_this = state.stacks['_string'].stack_ref(0)
        in_this = state.stacks['_string'].stack_ref(2)
        new_string = in_this.replace(replace_this, with_this)
        state.stacks['_string'].pop_item()
        state.stacks['_string'].pop_item()
        state.stacks['_string'].pop_item()
        state.stacks['_string'].push_item(new_string)
    return state
string_replace_instruction = instr.Pysh_Instruction('string_replace',
                                                    string_replace,
                                                    stack_types = ['_string'])
registered_instructions.register_instruction(string_replace_instruction)
#<instr_open>
#<instr_name>string_replace
#<instr_desc>Replaces all instances of second string with the top string in the third string. Pushes the result.
#<instr_close>

## STRING CHAR INSTRUCTIONS ##

def string_from_char(state):
    if len(state.stacks['_char']) > 0:
        new_string = str(state.stacks['_char'].stack_ref(0))
        state.stacks['_char'].pop_item()
        state.stacks['_string'].push_item(new_string)
string_from_char_instruction = instr.Pysh_Instruction('string_from_char',
                                                      string_from_char,
                                                      stack_types = ['_string', '_char'])
registered_instructions.register_instruction(string_from_char_instruction)
#<instr_open>
#<instr_name>string_from_char
#<instr_desc>Pushed the top `char` to the `string` stack.
#<instr_close>


def string_append_char(state):
    if len(state.stacks['_char']) > 0 and len(state.stacks['_string']) > 0:
        new_string =  state.stacks['_string'].stack_ref(0) + state.stacks['_char'].stack_ref(0)
        state.stacks['_char'].pop_item()
        state.stacks['_string'].pop_item()
        state.stacks['_string'].push_item(new_string)
string_append_char_instruction = instr.Pysh_Instruction('string_append_char',
                                                        string_append_char,
                                                        stack_types = ['_string', '_char'])
registered_instructions.register_instruction(string_append_char_instruction)
#<instr_open>
#<instr_name>string_append_char
#<instr_desc>Appends the top `char` to the top `string` and pushes result to the `string` stack.
#<instr_close>


def string_first(state):
    if len(state.stacks['_string']) > 0 and len(state.stacks['_string'].stack_ref(0)) > 0:
        new_char = state.stacks['_string'].stack_ref(0)[0]
        state.stacks['_string'].pop_item()
        state.stacks['_char'].push_item(new_char)
string_first_instruction = instr.Pysh_Instruction('string_first',
                                                  string_first,
                                                  stack_types = ['_string', '_char'])
registered_instructions.register_instruction(string_first_instruction)
#<instr_open>
#<instr_name>string_first
#<instr_desc>Pushes the first `char` of the top `string`.
#<instr_close>      


def string_last(state):
    if len(state.stacks['_string']) > 0 and len(state.stacks['_string'].stack_ref(0)) > 0:
        new_char = state.stacks['_string'].stack_ref(0)[-1]
        state.stacks['_string'].pop_item()
        state.stacks['_char'].push_item(new_char)
string_last_instruction = instr.Pysh_Instruction('string_last',
                                                  string_last,
                                                  stack_types = ['_string', '_char'])
registered_instructions.register_instruction(string_last_instruction)
#<instr_open>
#<instr_name>string_first
#<instr_desc>Pushes the last `char` of the top `string`.
#<instr_close> 



def string_nth(state):
    if len(state.stacks['_string']) > 0 and len(state.stacks['_integer']) > 0 and len(state.stacks['_string'].stack_ref(0)) > 0:
        top_str = state.stacks['_string'].stack_ref(0)
        index = state.stacks['_integer'].stack_ref(0) % len(top_str)
        new_char = top_str[index]
        state.stacks['_string'].pop_item()
        state.stacks['_integer'].pop_item()
        state.stacks['_char'].push_item(new_char)
string_nth_instruction = instr.Pysh_Instruction('string_nth',
                                                 string_nth,
                                                 stack_types = ['_string', '_char', '_integer'])
registered_instructions.register_instruction(string_nth_instruction)
#<instr_open>
#<instr_name>string_nth
#<instr_desc>Pushes the nth `char` of the top `string`. n is the top `integer` mod the length of the top `string`.
#<instr_close> 


## string_containschar
## string_indexofchar
## string_occurrencesofchar

def string_replace_char(state):
    if len(state.stacks['_string']) > 0 and len(state.stacks['_char']) > 1:
        top_str = state.stacks['_string'].stack_ref(0)
        new_str = top_str.replace(state.stacks['_char'].stack_ref(1), state.stacks['_char'].stack_ref(0))
        state.stacks['_char'].pop_item()
        state.stacks['_char'].pop_item()
        state.stacks['_string'].push_item(new_str)
string_replace_char_instruction = instr.Pysh_Instruction('string_replace_char',
                                                         string_replace_char,
                                                         stack_types = ['_string', '_char'])
registered_instructions.register_instruction(string_replace_char_instruction)
#<instr_open>
#<instr_name>string_replace_char
#<instr_desc>Pushes the top `string` with all occurences of second `char` replaced with the top `char`.
#<instr_close> 


def string_replace_first_char(state):
    if len(state.stacks['_string']) > 0 and len(state.stacks['_char']) > 1:
        top_str = state.stacks['_string'].stack_ref(0)
        new_str = top_str.replace(state.stacks['_char'].stack_ref(1), state.stacks['_char'].stack_ref(0), 1)
        state.stacks['_char'].pop_item()
        state.stacks['_char'].pop_item()
        state.stacks['_string'].push_item(new_str)
string_replace_first_char_instruction = instr.Pysh_Instruction('string_replace_first_char',
                                                               string_replace_first_char,
                                                               stack_types = ['_string', '_char'])
registered_instructions.register_instruction(string_replace_first_char_instruction)
#<instr_open>
#<instr_name>string_replace_first_char_instruction
#<instr_desc>Pushes the top `string` with the first occurence of second `char` replaced with the top `char`.
#<instr_close> 

## string_removechar
## string_setchar
## exec_string_iterate


