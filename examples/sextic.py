# _*_ coding: utf_8 _*_
"""
Created on 7/29/2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import random

import pyshgp.gp.gp as gp
import pyshgp.push.interpreter as interp
import pyshgp.push.instructions.registered_instructions as ri
import pyshgp.push.instruction as instr

'''
This problem is symbolic regression.
'''

def target_function(x):
	return x**6 + -2*(x**4) + x**2

def error_func(program):
	errors = []

	for x in np.arange(-2.0, 2.0, 0.1):
		x = float(x)
		# Create the push interpreter
		interpreter = interp.PyshInterpreter([x])
		interpreter.run_push(program)
		# Get output
		top_float = interpreter.state.stacks["_float"].stack_ref(0)

		if type(top_float) == float:
			# compare to target output
			target_float = target_function(x)
			# calculate error
			errors.append((top_float - target_float)**2)
		else:
			errors.append(1000)

	return errors

problem_params = {
	"error_threshold" : 0.01,
	"population_size" : 2000,
	"atom_generators" : [ri.get_instruction("_float_div"),
						 ri.get_instruction("_float_mult"),
						 ri.get_instruction("_float_sub"),
						 ri.get_instruction("_float_add"),
						 ri.get_instruction("_float_rot"),
						 ri.get_instruction("_float_swap"),
						 ri.get_instruction("_float_dup"),
						 ri.get_instruction("_float_pop"),
                         lambda: float(random.randint(0, 21) - 10),
                         instr.PyshInputInstruction(0)],
    "epigenetic_markers" : [],
    "selection_method" : "epsilon_lexicase",
    "genetic_operator_probabilities" : {"alternation" : 0.5,
										"uniform_mutation" : 0.5},
	"uniform_mutation_constant_tweak_rate" : 0.1,
	"uniform_mutation_float_gaussian_standard_deviation" : 0.1
}


if __name__ == "__main__":
	gp.evolution(error_func, problem_params)

