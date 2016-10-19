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

credit_data = pd.read_csv("data/credit.csv")
train_inds = np.random.rand(len(credit_data)) < 0.8
training_set = credit_data[train_inds]
testing_set = credit_data[~train_inds]


def random_character_str():
	return random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")

def credit_error_func(program):
	errors = []

	for index, row in training_set.iterrows():
		# Create the push interpreter
		interpreter = interp.Pysh_Interpreter()
		interpreter.reset_pysh_state()
		
		# Push input number		
		interpreter.state.stacks["_input"].push_item(row['V1'])
		interpreter.state.stacks["_input"].push_item(row['V2'])
		interpreter.state.stacks["_input"].push_item(row['V3'])
		interpreter.state.stacks["_input"].push_item(row['V4'])
		interpreter.state.stacks["_input"].push_item(row['V5'])
		interpreter.state.stacks["_input"].push_item(row['V6'])
		interpreter.state.stacks["_input"].push_item(row['V7'])
		interpreter.state.stacks["_input"].push_item(row['V8'])
		interpreter.state.stacks["_input"].push_item(row['V9'])
		interpreter.state.stacks["_input"].push_item(row['V10'])
		interpreter.state.stacks["_input"].push_item(row['V11'])
		interpreter.state.stacks["_input"].push_item(row['V12'])
		interpreter.state.stacks["_input"].push_item(row['V13'])
		interpreter.state.stacks["_input"].push_item(row['V14'])
		interpreter.state.stacks["_input"].push_item(row['V15'])

		# Initialize output classes
		interpreter.state.stacks["_output"].push_item(0)
		interpreter.state.stacks["_output"].push_item(0)

		# Run program
		interpreter.run_push(program)

		# Get output
		class_votes = interpreter.state.stacks['_output'][1:]

		if row['V16'] == class_votes.index(max(class_votes))+1:
			errors.append(0)
		else:
			errors.append(1)

	return errors

credit_params = {
	"error_threshold" : 10,
	"population_size" : 1000,
	"atom_generators" : u.merge_dicts(ri.registered_instructions,
					                  {"f1" : lambda: random.randint(0, 100),
									   "f2" : lambda: random.random(),
									   "f3" : lambda: random_character_str(),
									   # Inpput instructions
									   "Input_1" : instr.Pysh_Input_Instruction(0),
									   "Input_2" : instr.Pysh_Input_Instruction(1),
									   "Input_3" : instr.Pysh_Input_Instruction(2),
									   "Input_4" : instr.Pysh_Input_Instruction(3),
									   "Input_5" : instr.Pysh_Input_Instruction(4),
									   "Input_6" : instr.Pysh_Input_Instruction(5),
									   "Input_7" : instr.Pysh_Input_Instruction(6),
									   "Input_8" : instr.Pysh_Input_Instruction(7),
									   "Input_9" : instr.Pysh_Input_Instruction(8),
									   "Input_10" : instr.Pysh_Input_Instruction(9),
									   "Input_11" : instr.Pysh_Input_Instruction(10),
									   "Input_12" : instr.Pysh_Input_Instruction(11),
									   "Input_13" : instr.Pysh_Input_Instruction(12),
									   "Input_14" : instr.Pysh_Input_Instruction(13),
									   "Input_15" : instr.Pysh_Input_Instruction(14),
									   # Class label voting instsructions.
									   "Vote_1_float"   : instr.Pysh_Class_Instruction(1, '_float'),
									   "Vote_1_integer" : instr.Pysh_Class_Instruction(1, '_integer'),
									   "Vote_2_float"   : instr.Pysh_Class_Instruction(2, '_float'),
									   "Vote_2_integer" : instr.Pysh_Class_Instruction(2, '_integer'),
									  }),	
    "selection_method" : "lexicase",
	"uniform_mutation_constant_tweak_rate" : 0.1,
	"uniform_mutation_float_gaussian_standard_deviation" : 0.1
}

if __name__ == "__main__":
	gp.evolution(credit_error_func, credit_params)