# _*_ coding: utf_8 _*_
"""
Created on 7/29/2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import math
import numpy as np
import random

from pysh.gp import gp
from pysh import pysh_interpreter
from pysh import instruction
from pysh.instructions import boolean, code, common, numbers, string
from pysh.instructions import registered_instructions as ri

'''
This problem evolves a program to determine if a number is odd or not.
'''

def target_function(x):
	return x**6 + -2*(x**4) + x**2

def error_func(program):
	errors = []

	for x in np.arange(-2.0, 2.0, 0.1):
		x = float(x)
		# Create the push interpreter
		interpreter = pysh_interpreter.Pysh_Interpreter()
		interpreter.reset_pysh_state()
		
		# Push input number		
		interpreter.state.stacks["_float"].push_item(x)
		interpreter.state.stacks["_input"].push_item(x)
		# Run program
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
	"atom_generators" : {"float_div"    : ri.get_instruction_by_name("float_div"),
						 "float_mult"   : ri.get_instruction_by_name("float_mult"),
						 "float_sub"    : ri.get_instruction_by_name("float_sub"),
						 "float_add"    : ri.get_instruction_by_name("float_add"),
						 "float_rot"    : ri.get_instruction_by_name("float_rot"),
						 "float_swap"   : ri.get_instruction_by_name("float_swap"),
						 "float_dup"    : ri.get_instruction_by_name("float_dup"),
						 "float_pop"    : ri.get_instruction_by_name("float_pop"),
                         "f1"           : lambda: float(random.randint(0, 21) - 10),
                         "_input1"      : instruction.Pysh_Input_Instruction("_input1")},
    "epigenetic_markers" : [],
    "selection_method" : "epsilon_lexicase",
    "genetic_operator_probabilities" : {"alternation" : 0.5,
										"uniform_mutation" : 0.5},
	"uniform_mutation_constant_tweak_rate" : 0.1,
	"uniform_mutation_float_gaussian_standard_deviation" : 0.1
}


if __name__ == "__main__":
	gp.evolution(error_func, problem_params)

