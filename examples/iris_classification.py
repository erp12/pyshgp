# _*_ coding: utf_8 _*_
"""
Created on 9/19/2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import random
import numpy  as np
import pandas as pd

from pysh.gp import gp
import pysh.utils as u
import pysh.instruction as instr
import pysh.pysh_interpreter as interp
from pysh.instructions import registered_instructions as ri

iris_data = pd.read_csv("data/iris.csv")
train_inds = np.random.rand(len(iris_data)) < 0.8
training_set = iris_data[train_inds]
testing_set = iris_data[~train_inds]

def iris_error_func(program, print_trace = False):
	errors = []

	for index, row in training_set.iterrows():
		# Create the push interpreter
		interpreter = interp.Pysh_Interpreter()
		interpreter.reset_pysh_state()
		
		# Push input number		
		interpreter.state.stacks["_input"].push_item(float(row['Sepal_Length']))
		interpreter.state.stacks["_input"].push_item(float(row['Sepal_Width']))
		interpreter.state.stacks["_input"].push_item(float(row['Petal_Length']))
		interpreter.state.stacks["_input"].push_item(float(row['Petal_Width']))

		# Initialize output classes
		interpreter.state.stacks["_output"].push_item(0)
		interpreter.state.stacks["_output"].push_item(0)
		interpreter.state.stacks["_output"].push_item(0)

		# Run program
		interpreter.run_push(program, print_trace)
		# Get output
		class_votes = interpreter.state.stacks['_output'][1:]

		if row['Species'] == class_votes.index(max(class_votes))+1:
			errors.append(0)
		else:
			errors.append(1)

	return errors

iris_params = {
	"error_threshold" : 6, # Single decision tree tends to have an error of 6
	"population_size" : 1000,
	"atom_generators" : u.merge_dicts(ri.get_instructions_by_pysh_type('_float'),
									  ri.get_instructions_by_pysh_type('_exec'),
					                  {"f1" : lambda: random.randint(0, 100),
									   "f2" : lambda: random.random(),
									   # Input Instructions.
									   "Sepal_Length" : instr.Pysh_Input_Instruction(0),
									   "Sepal_Width" : instr.Pysh_Input_Instruction(1),
									   "Petal_Length" : instr.Pysh_Input_Instruction(2),
									   "Petal_Width" : instr.Pysh_Input_Instruction(3),
									   # Class label voting instsructions.
									   "Vote_1_float" : instr.Pysh_Class_Instruction(1, '_float'),
									   "Vote_2_float" : instr.Pysh_Class_Instruction(2, '_float'),
									   "Vote_3_float" : instr.Pysh_Class_Instruction(3, '_float'),
									  }),
	"genetic_operator_probabilities" : {"alternation" : 0.3,
                                        "uniform_mutation" : 0.3,
                                        "alternation & uniform_mutation" : 0.3,
                                        "uniform_close_mutation" : 0.1},
    "selection_method" : "lexicase",
	"uniform_mutation_constant_tweak_rate" : 0.1,
	"uniform_mutation_float_gaussian_standard_deviation" : 0.1
}

def test_iris_solution():
	prog_lst = ["_integer_stack_depth", "_integer_inc"]
	prog = gp.load_program_from_list(prog_lst)
	errors = iris_error_func(prog, True)
	print("Errors:", errors)
	print(ri.registered_instructions.keys())


if __name__ == "__main__":
	gp.evolution(iris_error_func, iris_params)
	#test_iris_solution()

