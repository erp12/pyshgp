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

		# Run program
		interpreter.run_push(program)
		# Get output
		top_float = interpreter.state.stacks["_float"].stack_ref(0)

		if type(top_float) == float:
			errors.append(abs(row['V15'] - top_float))
		else:
			errors.append(1000)

	return errors

credit_params = {
	"error_threshold" : 10,
	"population_size" : 1000,
	"atom_generators" : u.merge_dicts(ri.registered_instructions,
					                  {"f1" : lambda: random.randint(0, 100),
									   "f2" : lambda: random.random(),
									   "_input1" : instr.Pysh_Input_Instruction("_input1"),
									   "_input2" : instr.Pysh_Input_Instruction("_input2"),
									   "_input3" : instr.Pysh_Input_Instruction("_input3"),
									   "_input4" : instr.Pysh_Input_Instruction("_input4"),
									   "_input5" : instr.Pysh_Input_Instruction("_input5"),
									   "_input6" : instr.Pysh_Input_Instruction("_input6"),
									   "_input7" : instr.Pysh_Input_Instruction("_input7"),
									   "_input8" : instr.Pysh_Input_Instruction("_input8"),
									   "_input9" : instr.Pysh_Input_Instruction("_input9"),
									   "_input10" : instr.Pysh_Input_Instruction("_input10"),
									   "_input11" : instr.Pysh_Input_Instruction("_input11"),
									   "_input12" : instr.Pysh_Input_Instruction("_input12"),
									   "_input13" : instr.Pysh_Input_Instruction("_input13"),
									   "_input14" : instr.Pysh_Input_Instruction("_input14"),
									   "_input15" : instr.Pysh_Input_Instruction("_input15"),
									  }),	
    "selection_method" : "lexicase",
	"uniform_mutation_constant_tweak_rate" : 0.1,
	"uniform_mutation_float_gaussian_standard_deviation" : 0.1
}

if __name__ == "__main__":
	gp.evolution(credit_error_func, credit_params)