# _*_ coding: utf_8 _*_
"""
Created on 11/30/2016

@author: Eddie
"""

import random
import collections
import numpy as np

from pysh import pysh_interpreter
from pysh import instruction as instr
from pysh import utils as u
from pysh import pysh_globals as g
from pysh.gp import gp
from pysh.instructions import boolean, code, common, numbers, string
from pysh.instructions import registered_instructions as ri

def gen_random_test_case():
    i = random.randint(4, 31)
    return [random.choice(list(range(i))) for _ in list(range(i))]

test_cases = [g.PushVector(gen_random_test_case(), int) for _ in list(range(20))]

for t in test_cases:
    print(t, [x - 1 for x in t])

def error_func(program):
    errors = []
    for t in test_cases:
        interpreter = pysh_interpreter.Pysh_Interpreter()
        
        interpreter.state.stacks["_input"].push_item(t)
        interpreter.run_push(program)
        prog_output = interpreter.state.stacks['_integer'][:]
        target_output = [x - 1 for x in t]

        if prog_output == '_no_stack_item' or prog_output == '_stack_out_of_bounds_item':
            errors.append(2000)
        elif not len(prog_output) == len(target_output):
            errors.append(1000)
        else:
            # errors.append(u.levenshtein_distance(prog_output, target_output))
            rmse = np.linalg.norm(np.array(prog_output) - np.array(target_output)) / np.sqrt(len(prog_output))
            errors.append(rmse)
    return errors

params = {
    "atom_generators" : u.merge_dicts(ri.get_instructions_by_pysh_type("_integer"),
                                      ri.get_instructions_by_pysh_type("_vector"),
                                      {"Input0" : instr.Pysh_Input_Instruction(0)}),
    "genetic_operator_probabilities" : {"alternation" : 0.2,
                                        "uniform_mutation" : 0.2,
                                        "alternation & uniform_mutation" : 0.5,
                                        "uniform_close_mutation" : 0.1},
    "selection_method" : "epsilon_lexicase",
    "max_genome_initial_size" : 20,
    "alternation_rate" : 0.01,
    "alignment_deviation" : 10,
    "uniform_mutation_rate" : 0.01,
    "final_report_simplifications" : 5000

}

if __name__ == "__main__":
    gp.evolution(error_func, params)