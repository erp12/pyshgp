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

def gen_random_test_case():
    i = random.randint(4, 31)
    j = random.randint(0, i-1)
    return [[random.choice(list(range(i))) for _ in list(range(i))], j]

test_cases = [gen_random_test_case() for _ in list(range(20))]

def error_func(program):
    errors = []
    for t in test_cases:
        interpreter = pysh_interpreter.Pysh_Interpreter()
        
        interpreter.state.stacks["_input"].push_item(t[0])
        interpreter.run_push(program)
        prog_output = interpreter.state.stacks['_integer'].stack_ref(0)
        target_output = t[0][t[1]]

        if prog_output == '_no_stack_item' or prog_output == '_stack_out_of_bounds_item':
            errors.append(1000)
        elif prog_output == target_output:
            errors.append(0)
        else:
            errors.append(1)
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
    "max_genome_initial_size" : 20,
    "alternation_rate" : 0.01,
    "alignment_deviation" : 10,
    "uniform_mutation_rate" : 0.01,
    "final_report_simplifications" : 5000

}

if __name__ == "__main__":
    gp.evolution(error_func, params)