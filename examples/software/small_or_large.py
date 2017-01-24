# _*_ coding: utf_8 _*_
"""
Created on 1/12/2017

@author: Eddie
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import random

import pyshgp.utils as u
import pyshgp.gp.gp as gp
import pyshgp.push.interpreter as interp
import pyshgp.push.instructions.registered_instructions as ri
import pyshgp.push.instruction as instr

def generate_cases(num_base_cases, num_rand_cases):
    base_cases = np.asarray([-10000, 0, 980, 1020, 19180, 2020, 10000] + list(range(995, 1005)))
    more_cases = np.asarray(list(range(-10000, 10000)))
    all_cases = np.concatenate((np.random.choice(base_cases, num_base_cases), np.random.choice(more_cases, num_rand_cases)))
    print(all_cases)
    return all_cases.tolist()

train_cases = generate_cases(27, 73)
#test_cases = generate_cases(0, 1000)

def error_func(program):
    errors = []
    for t in train_cases:
        interpreter = interp.PushInterpreter([t])
        interpreter.run_push(program)
        
        result = interpreter.state.stacks["_output"].ref(0)
        target = ''
        if t < 1000:
        	target = 'small'
        elif t > 2000:
        	target = 'large'

        errors.append(u.levenshtein_distance(result, target))
    return errors

params = {
    "atom_generators" : list(u.merge_sets(ri.get_instructions_by_pysh_type('_integer'),
                                          ri.get_instructions_by_pysh_type('_boolean'),
                                          ri.get_instructions_by_pysh_type('_exec'),
                                          ri.get_instructions_by_pysh_type('_string'),
                                          ri.get_instructions_by_pysh_type('_print'),
                                          [# Random function
                                           lambda: random.randint(-10000, 10000),
                                           # Input instruction
                                           instr.PyshInputInstruction(0)])),
    "max_points" : 800,
    "max_genome_size_in_initial_program" : 100,
    "evalpush_limit" : 300,
    "population_size" : 1000,
    "max_generations" : 300,
    "genetic_operator_probabilities" : {"alternation" : 0.2,
                                        "uniform_mutation" : 0.2,
                                        "alternation & uniform_mutation" : 0.5,
                                        "uniform_close_mutation" : 0.1},
    "alternation_rate" : 0.01,
    "alignment_deviation" : 5,
    "uniform_mutation_rate" : 0.01,
    "final_report_simplifications" : 5000,
    "error_threshold" : 1.0E-3
}

if __name__ == "__main__":
    gp.evolution(error_func, params)