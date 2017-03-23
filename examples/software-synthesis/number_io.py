# _*_ coding: utf_8 _*_
"""
Created on 1/12/2017

@author: Eddie
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import random

import pyshgp.utils as u
import pyshgp.gp.gp as gp
import pyshgp.push.interpreter as interp
import pyshgp.push.instructions.registered_instructions as ri
import pyshgp.push.instruction as instr

def generate_cases(num):
    cases = []
    for _ in list(range(num)):
        f = (random.random() * 200) - 100
        i = random.randint(0, 201) - 100
        cases.append([[f, i], round(f + i, 4)])
    return cases

train_cases = generate_cases(30)
test_cases = generate_cases(200)

def error_func(program):
    errors = []
    for t in train_cases:
        interpreter = interp.PushInterpreter(t[0])
        interpreter.run_push(program)
        str_result = interpreter.state.stacks["_output"].ref(0)

        try:
            errors.append(abs(t[1] - float(str_result)))
        except ValueError:
            errors.append(1000)
        errors.append(u.levenshtein_distance(str_result, str(t[1])))
    return errors

params = {
    "atom_generators" : list(u.merge_sets(ri.get_instructions_by_pysh_type('_float'),
                                          ri.get_instructions_by_pysh_type('_integer'),
                                          ri.get_instructions_by_pysh_type('_print'),
                                          [# Random runctions
                                           lambda: (random.random() * 200) - 100,
                                           lambda: random.randint(0, 201) - 100,
                                           # Input instruction
                                           instr.PyshInputInstruction(0),
                                           instr.PyshInputInstruction(1)])),
    "max_points" : 800,
    "max_genome_size_in_initial_program" : 100,
    "evalpush_limit" : 200,
    "population_size" : 1000,
    "max_generations" : 200,
    "genetic_operator_probabilities" : {"alternation" : 0.3,
                                        "uniform_mutation" : 0.2,
                                        "alternation & uniform_mutation" : 0.5},
    "alternation_rate" : 0.01,
    "alignment_deviation" : 5,
    "uniform_mutation_rate" : 0.01,
    "final_report_simplifications" : 5000,
    "error_threshold" : 1.0E-3
}

if __name__ == "__main__":

    gp.evolution(error_func, params)