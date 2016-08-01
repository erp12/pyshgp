# _*_ coding: utf_8 _*_
"""
Created on 5/21/2016

@author: Eddie
"""
import copy
import random

from ..gp import gp
from .. import pysh_interpreter
from ..instructions import *
from ..instructions import registered_instructions 

'''
This problem evolves a program to determine if a number is odd or not.
'''

def odd_error_func(program):
	errors = []

	for i in range(9):
		prog = copy.deepcopy(program)
		# Create the push interpreter
		interpreter = pysh_interpreter.Pysh_Interpreter()
		interpreter.reset_pysh_state()
		
		# Push input number		
		interpreter.state.stacks["_integer"].push_item(i)
		interpreter.state.stacks["_input"].push_item(i)
		# Run program
		interpreter.run_push(prog)
		# Get output
		prog_output = interpreter.state.stacks["_boolean"].stack_ref(0)
		#compare to target output
		target_output = bool(i % 2)

		if prog_output == target_output:
			errors.append(0)
		else:
			errors.append(1)

	return errors

odd_params = {
	"atom_generators" : registered_instructions.registered_instructions +	# Use all possible instructions,
                        [lambda: random.randint(0, 100),					# and some integers
                         lambda: random.random(),							# and some floats
                         "_in1"]											# and an input instruction that pushes the input to the _integer stack.
}

def test_odd_solution():
	#prog_lst = ["_in1", "_integer_add"]
	prog_lst = ['_exec_stack_depth', '_in1', '_float_dup', '_float_sub', '_string_empty', '_exec_yankdup', '_float_stack_depth', '_foat_from_boolean', '_string_stack_depth', '_integer_gte', '_in1', '_float_dup', '_float_sub', '_string_empty', '_exec_yankdup', '_float_stack_depth', '_foat_from_boolean', '_string_stack_depth', '_integer_gte', '_code_shove', '_foat_from_boolean', '_string_stack_depth', '_float_lt', 3, '_boolean_xor', '_boolean_xor', '_integer_yank', '_integer_gte']
	prog = gp.load_program_from_list(prog_lst)
	errors = odd_error_func(prog)
	print "Errors:", errors


if __name__ == "__main__":
	gp.evolution(odd_error_func, odd_params)
	#test_odd_solution()

