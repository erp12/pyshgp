# _*_ coding: utf_8 _*_
"""
Created on 11/30/2016

@author: Eddie
"""

import random
import collections

from pysh import pysh_interpreter
from pysh import instruction as instr
from pysh import utils as u
from pysh.gp import gp
from pysh.instructions import boolean, code, common, numbers, string
from pysh.instructions import registered_instructions as ri


test_cases = ['0000',
              '0001',
              '0010',
              '0011',
              '0100',
              '0101',
              '0110',
              '0111',
              '1000',
              '1001',
              '1010',
              '1011',
              '1100',
              '1101',
              '1110',
              '1111',
              '00001011',
              '00011101',
              '00101110',
              '00111101',
              '01001011',
              '01010111',
              '01101111',
              '01110101']

def invert_bitstring(bitstr):
    inverted_bitstr = ""
    for bit in bitstr:
        if bit == '0':
            inverted_bitstr += '1'
        elif bit == '1':
            inverted_bitstr += '0'
        else:
            break

    return inverted_bitstr

def string_difference(s1, s2):
    '''
    Returns the difference in the strings, based on character position.
    '''
    char_lvl_diff = 0
    for c1, c2 in zip(s1, s2):
        char_lvl_diff += int(not c1 == c2)
    return char_lvl_diff + abs(len(s1) - len(s2))

def string_char_counts_difference(s1, s2):
    '''
    '''
    result = len(s1) + len(s2)
    s1_letters = collections.Counter(s1)
    for c in s2:
        if c in s1_letters:
            result -= 2
            s1_letters[c] -= 1
            if s1_letters[c] == 0:
                s1_letters.pop(c, None)
    return result

for t in test_cases:
    print(t, invert_bitstring(t), string_difference(invert_bitstring(t), t), string_char_counts_difference(invert_bitstring(t), t))

def error_func(program):
    errors = []
    for t in test_cases:
        interpreter = pysh_interpreter.Pysh_Interpreter()
        
        interpreter.state.stacks["_input"].push_item(t)
        interpreter.state.stacks["_input"].push_item('0')
        interpreter.state.stacks["_input"].push_item('1')
        interpreter.run_push(program)
        prog_output = interpreter.state.stacks['_string'].stack_ref(0)
        target_output = invert_bitstring(t)

        if prog_output == '_no_stack_item' or prog_output == '_stack_out_of_bounds_item':
            errors.append(1000)
        else:
            #errors.append(u.levenshtein_distance(prog_output, target_output))
            errors.append(string_difference(target_output, t) + string_char_counts_difference(target_output, t))
    return errors

params = {
    "atom_generators" : u.merge_dicts(ri.registered_instructions,
                                      {"Input0" : instr.Pysh_Input_Instruction(0),
                                       "Input1" : instr.Pysh_Input_Instruction(1),
                                       "Input2" : instr.Pysh_Input_Instruction(2)}),
    "genetic_operator_probabilities" : {"alternation" : 0.2,
                                        "uniform_mutation" : 0.2,
                                        "alternation & uniform_mutation" : 0.5,
                                        "uniform_close_mutation" : 0.1},
    "alternation_rate" : 0.01,
    "alignment_deviation" : 10,
    "uniform_mutation_rate" : 0.01,
    "final_report_simplifications" : 5000

}

if __name__ == "__main__":
    gp.evolution(error_func, params)