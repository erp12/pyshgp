# _*_ coding: utf_8 _*_
"""
Created on 12/1/2016

@author: Eddie
"""

import random
import collections

from pysh import pysh_interpreter
from pysh import instruction as instr
from pysh import utils as u
from pysh import pysh_globals as g
from pysh.gp import gp
from pysh.instructions import boolean, code, common, numbers, string
from pysh.instructions import registered_instructions as ri


test_cases = [g.PushVector([False, False, False, False], bool),
              g.PushVector([False, False, False, True], bool),
              g.PushVector([False, False, True, False], bool),
              g.PushVector([False, False, True, True], bool),
              g.PushVector([False, True, False, False], bool),
              g.PushVector([False, True, False, True], bool),
              g.PushVector([False, True, True, False], bool),
              g.PushVector([False, True, True, True], bool),
              g.PushVector([True, False, False, False], bool),
              g.PushVector([True, False, False, True], bool),
              g.PushVector([True, False, True, False], bool),
              g.PushVector([True, False, True, True], bool),
              g.PushVector([True, True, False, False], bool),
              g.PushVector([True, True, False, True], bool),
              g.PushVector([True, True, True, False], bool),
              g.PushVector([True, True, True, True], bool),
              g.PushVector([False, False, False, False, True, False, True, True], bool),
              g.PushVector([False, False, False, True, True, True, False, True], bool),
              g.PushVector([False, False, True, False, True, True, True, False], bool),
              g.PushVector([False, False, True, True, True, True, False, True], bool),
              g.PushVector([False, True, False, False, True, False, True, True], bool),
              g.PushVector([False, True, True, False, True, True, True, True], bool),
              g.PushVector([False, False, False, False, False, False, False, False], bool),
              g.PushVector([False, True, True, True, False, True, False, True], bool)]

def binary_decrement(bitstr):
    bits = list(bitstr[::-1])
    for i, bit in enumerate(bits):
        if bit:
            bits[i] = False
            break
        else:
            bits[i] = True
    return bits[::-1]

for t in test_cases:
    print(t, binary_decrement(t))
print()

def error_func(program):
    errors = []
    for t in test_cases:
        interpreter = pysh_interpreter.Pysh_Interpreter()
        
        interpreter.state.stacks["_input"].push_item(t)
        interpreter.run_push(program)
        prog_output = interpreter.state.stacks['_boolean'][:]
        target_output = binary_decrement(t)

        if prog_output == '_no_stack_item' or prog_output == '_stack_out_of_bounds_item':
            errors.append(1000)
        else:
            errors.append(u.levenshtein_distance(prog_output, target_output))
    return errors

params = {
    "atom_generators" : u.merge_dicts(ri.registered_instructions,
                                      {"Input0" : instr.Pysh_Input_Instruction(0)}),
    "genetic_operator_probabilities" : {"alternation" : 0.2,
                                        "uniform_mutation" : 0.2,
                                        "alternation & uniform_mutation" : 0.5,
                                        "uniform_close_mutation" : 0.1},
    "max_points" : 3200,
    "max_genome_size_in_initial_program" : 400,
    "evalpush_limit" : 1600,
    "population_size" : 1000,
    "max_generations" : 300,
    "alternation_rate" : 0.01,
    "alignment_deviation" : 10,
    "uniform_mutation_rate" : 0.01,
    "final_report_simplifications" : 5000

}

if __name__ == "__main__":
    gp.evolution(error_func, params)