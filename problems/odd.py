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
		
		# Push in input number		
		interpreter.state.stacks["_integer"].push_item(i)
		interpreter.state.stacks["_input"].push_item(i)

		# Run program
		interpreter.run_push(prog)
		# Get output
		prog_output = interpreter.state.stacks["_boolean"].stack_ref(0)
		#compare to target output
		target_output = bool(i % 2)
		
		#print prog_output, target_output

		if prog_output == target_output:
			errors.append(0)
		else:
			errors.append(1)

	return errors

def test_odd_solution():
	#prog_lst = [2, '_integer_mod', 1, '_integer_eq']
	prog = gp.load_program_from_list(prog_lst)
	errors = odd_error_func(prog)
	print "Errors:", errors

odd_params = {
	"atom_generators" : registered_instructions.registered_instructions + 
                        [lambda: random.randint(0, 100),
                         lambda: random.random(),
                         "_in1"]
}

if __name__ == "__main__":
	gp.evolution(odd_error_func, odd_params)
	#test_odd_solution()

