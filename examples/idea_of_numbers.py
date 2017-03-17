# _*_ coding: utf_8 _*_
"""
Created on 3/17/2017

@author: Tozier
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import random

import pyshgp.utils as u
import pyshgp.gp.gp as gp
import pyshgp.push.interpreter as interp
import pyshgp.push.instructions.registered_instructions as ri
import pyshgp.push.instruction as instr

'''
This problem evolves a program (using the full Push instruction set) to fit the symbolic regression problem `9x^2-11x + 1964`. But it is given no numeric constants at all to work with, and has to "MacGuyver" a mechanism to build large-enough constants to fit the training cases.
'''

def target_function(x):
    return 9 * x**2 - 11 * x + 1964

def error_func(program):
    errors = []

    for x in range(20):
        # Create the push interpreter and run program
        interpreter = interp.PushInterpreter(inputs=[x])
        interpreter.run_push(program)
        # Get output
        top_int = interpreter.state.stacks["_integer"].ref(0)

        if type(top_int) == int:
            # compare to target output
            target_int = target_function(x)
            # calculate error
            errors.append(abs(top_int - target_int))
        else:
            errors.append(100000000)

    return errors

problem_params = {
    "atom_generators" : list(u.merge_sets(ri.registered_instructions,
                                          [instr.PyshInputInstruction(0)])),
    "epigenetic_markers" : [],
    "selection_method" : "epsilon_lexicase",
    "genetic_operator_probabilities" : {"alternation" : 0.5,
                                        "uniform_mutation" : 0.5},
    "alternation_rate" : 0.1,
    "uniform_mutation_rate" : 0.1
}


if __name__ == "__main__":
    gp.evolution(error_func, problem_params)
