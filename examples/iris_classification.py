# _*_ coding: utf_8 _*_
"""
Created on 9/19/2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import random
import numpy  as np
import pandas as pd

import pyshgp.utils as u
import pyshgp.gp.gp as gp
import pyshgp.push.interpreter as interp
import pyshgp.push.instructions.registered_instructions as ri
import pyshgp.push.instruction as instr

# Get the absolute path to the data file
script_dir = os.path.dirname(__file__)
rel_path = "data/iris.csv"
abs_file_path = os.path.join(script_dir, rel_path)

# Load the data file and split into training and testing.
iris_data = pd.read_csv(abs_file_path)
train_inds = np.random.rand(len(iris_data)) < 0.8
training_set = iris_data[train_inds]
testing_set = iris_data[~train_inds]

def iris_error_func(program, print_trace = False):
	errors = []

	for index, row in training_set.iterrows():
		# Create the push interpreter
		interpreter = interp.PyshInterpreter([float(x) for x in row.drop('Species').tolist()])
    
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
	"error_threshold" : 2, # Single decision tree tends to have an error of 6
	"atom_generators" : list(u.merge_sets(ri.get_instructions_by_pysh_type('_float'),
					      ri.get_instructions_by_pysh_type('_exec'),
					      [lambda: random.randint(0, 100),
					       lambda: random.random(),
					       # Input Instructions.
					       instr.PyshInputInstruction(0),
					       instr.PyshInputInstruction(1),
					       instr.PyshInputInstruction(2),
					       instr.PyshInputInstruction(3),
					       # Class label voting instsructions.
					       instr.PyshClassVoteInstruction(1, '_float'),
					       instr.PyshClassVoteInstruction(2, '_float'),
					       instr.PyshClassVoteInstruction(3, '_float')])),
	"genetic_operator_probabilities" : {"alternation" : 0.3,
                                        "uniform_mutation" : 0.3,
                                        "alternation & uniform_mutation" : 0.3,
                                        "uniform_close_mutation" : 0.1},
    "selection_method" : "epsilon_lexicase",
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

