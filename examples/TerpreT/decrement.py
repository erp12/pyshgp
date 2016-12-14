# _*_ coding: utf_8 _*_
"""
Created on 11/30/2016

@author: Eddie
"""
import random
import numpy as np

import pysh.utils as u
import pysh.gp.gp as gp
import pysh.push.interpreter as interp
import pysh.push.instructions.registered_instructions as ri
import pysh.push.instruction as instr

def gen_random_test_case():
    i = random.randint(4, 31)
    return [random.choice(list(range(i))) for _ in list(range(i))]

test_cases = [u.PushVector(gen_random_test_case(), int) for _ in list(range(20))]

for t in test_cases:
    print(t, [x - 1 for x in t])

def error_func(program):
    errors = []
    for t in test_cases:
        interpreter = interp.PyshInterpreter()
        
        interpreter.state.stacks["_input"].push_item(t)
        interpreter.run_push(program)
        prog_output = interpreter.state.stacks['_integer'][:]
        target_output = [x - 1 for x in t]

        if isinstance(prog_output, u.UnevaluatableStackResponse):
            errors.append(2000)
        elif not len(prog_output) == len(target_output):
            errors.append(1000)
        else:
            # errors.append(u.levenshtein_distance(prog_output, target_output))
            rmse = np.linalg.norm(np.array(prog_output) - np.array(target_output)) / np.sqrt(len(prog_output))
            errors.append(rmse)
    return errors

params = {
    "atom_generators" : list(u.merge_sets(ri.get_instructions_by_pysh_type("_integer"),
                                          ri.get_instructions_by_pysh_type("_vector"),
                                          [instr.PyshInputInstruction(0)])),
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