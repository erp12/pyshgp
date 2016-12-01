# _*_ coding: utf_8 _*_
"""
Created on 11/30/2016

@author: Eddie
"""

import random

from pysh import pysh_interpreter
from pysh import instruction as instr
from pysh import utils as u
from pysh.gp import gp
from pysh.instructions import boolean, code, common, numbers, string
from pysh.instructions import registered_instructions as ri


test_cases = [(False, False, False),
              (False, False, True),
              (False, True, False),
              (False, True, True),
              (True, False, False),
              (True, False, True),
              (True, True, False),
              (True, True, True)]

def full_adder(c, a, b):
    xor_1 = not a == b
    s = not xor_1 == c

    and_1 = a and b
    and_2 = xor_1 and c
    c_out = and_1 or and_2
    return (s, c_out)

def error_func(program):
    errors = []
    for t in test_cases:
        interpreter = pysh_interpreter.Pysh_Interpreter()
        
        interpreter.state.stacks["_input"].push_item(t[0])
        interpreter.state.stacks["_input"].push_item(t[1])
        interpreter.state.stacks["_input"].push_item(t[2])

        interpreter.run_push(program)
        prog_output = interpreter.state.stacks['_boolean'][-2:]
        target_output = full_adder(t[0], t[1], t[2])

        e = 0
        if len(prog_output) < 2 or '_no_stack_item' in prog_output or '_stack_out_of_bounds_item' in prog_output:
            e += 1000
        else:
            if not prog_output[0] == target_output[0]: # Is the sum the same
                e += 1
            if not prog_output[1] == target_output[1]: # Is the carry out the same
                e += 1
        errors.append(e)
    return errors

params = {
    "atom_generators" : u.merge_dicts(ri.get_instructions_by_pysh_type("_boolean"),
                                      ri.get_instructions_by_pysh_type("_exec"),
                                      {"Input0" : instr.Pysh_Input_Instruction(0),
                                       "Input1" : instr.Pysh_Input_Instruction(1),
                                       "Input2" : instr.Pysh_Input_Instruction(2)}),
    "genetic_operator_probabilities" : {"alternation" : 0.2,
                                        "uniform_mutation" : 0.2,
                                        "alternation & uniform_mutation" : 0.5,
                                        "uniform_close_mutation" : 0.1},
    "alternation_rate" : 0.1,
    "alignment_deviation" : 10,
    "uniform_mutation_rate" : 0.1,
    "final_report_simplifications" : 5000

}

if __name__ == "__main__":
    gp.evolution(error_func, params)