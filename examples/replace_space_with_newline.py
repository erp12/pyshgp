# _*_ coding: utf_8 _*_
"""
Created on 9/15/2016

@author: Eddie
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import math
import random
import collections

from pysh import pysh_interpreter
from pysh import utils as u
from pysh import instruction as instr
from pysh.gp import gp
from pysh.instructions import boolean, code, common, numbers, string
from pysh.instructions import registered_instructions as ri

'''
Given a string input, print the string, replacing spaces with newlines.
The input string will not have tabs or newlines, but may have multiple spaces
in a row. It will have maximum length of 20 characters. Also, the program
should return the integer count of the non-whitespace characters.
'''

def random_str(str_length):
	s = ""
	for i in range(str_length):
		if random.random() < 0.2:
			s += " "
		else:
			s += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
	return s


def make_RSWN_data_domains():
	dd_1 = {"inputs" : ["", "A", "*", " ", "s", "B ", "  ", " D", "ef", "!!", " F ", "T L", "4ps", "q  ", "   ", "  e", "hi ", "  $  ", "      9",
						"i !i !i !i !i", "88888888888888888888", "                    ", "ssssssssssssssssssss", "1 1 1 1 1 1 1 1 1 1 ",
						" v v v v v v v v v v", "Ha Ha Ha Ha Ha Ha Ha", "x y!x y!x y!x y!x y!", "G5G5G5G5G5G5G5G5G5G5", ">_=]>_=]>_=]>_=]>_=]",
						"^_^ ^_^ ^_^ ^_^ ^_^ "],
			"train_test_split" : [30, 0]}
	dd_2 = {"inputs" : lambda: random_str(random.randint(2, 19)),
			"train_test_split" : [70, 1000]}
	return (dd_1, dd_2)

def RSWN_test_cases(inputs):
	'''
	Takes a sequence of inputs and gives IO test cases of the form [input output].
	[inpt_str [target_str, taget_int]]
	'''
	return list(map(lambda inpt: [inpt, [str.replace(inpt, " ", "\n"), len(list(filter(lambda x: not x == " ", inpt)))]], inputs))

def make_RSWN_error_func_from_cases(train_cases, test_cases):
	def actual_RSWN_func(program, data_cases = "train", print_outputs = False, debug = False):
		errors = []

		cases = train_cases
		if data_cases == "test":
			cases = test_cases

		interpreter = pysh_interpreter.Pysh_Interpreter()

		for io_pair in cases:
			interpreter.reset_pysh_state()
			interpreter.state.stacks["_input"].push_item(io_pair[0])
			interpreter.state.stacks["_output"].push_item("")
			interpreter.run_push(program, debug)
			str_result = interpreter.state.stacks["_string"].stack_ref(0)
			int_result = interpreter.state.stacks["_integer"].stack_ref(0)

			s_er = u.levenshtein_distance(io_pair[1][0], str_result)
			i_er = 1000
			if type(int_result) == int or type(int_result) == float:
				i_er = abs(int_result - io_pair[1][1])
			errors += [s_er, i_er]

		return errors
	return actual_RSWN_func

def get_RSWN_train_and_test():
	'''
	Returns the train and test cases.
	'''
	data_domains = make_RSWN_data_domains()
	io_pairs = list(map(RSWN_test_cases, u.test_and_train_data_from_domains(data_domains)))
	return io_pairs

RSWN_params = {
	"atom_generators" : u.merge_dicts({# Constants
									   "_space"              : lambda: " ",
									   "_newline"            : lambda: "\n",
									   # ERCs
									   "_char_ERC"           : lambda: random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789\n\t"),
									   "_string_ERC"         : lambda: random_str(random.randint(0, 21)),
									   # Input instruction
									   "_input1" 	           : instr.Pysh_Input_Instruction("_input1")},
									   # Standard stack instructions
									   ri.get_instructions_by_pysh_type("_integer"),
									   ri.get_instructions_by_pysh_type("_boolean"),
									   ri.get_instructions_by_pysh_type("_string"),
									   ri.get_instructions_by_pysh_type("_char"),
									   ri.get_instructions_by_pysh_type("_exec"),
									   ri.get_instructions_by_pysh_type("_print")
									   ),
	"max_points" : 3200,
	"max_genome_size_in_initial_program" : 400,
	"evalpush_limit" : 1600,
	"population_size" : 1000,
	"max_generations" : 300,
    "genetic_operator_probabilities" : {"alternation" : 0.2,
										"uniform_mutation" : 0.2,
										"alternation & uniform_mutation" : 0.5,
										"uniform_close_mutation" : 0.1},
	"alternation-rate" : 0.01,
	"alignment-deviation" : 10,
	"uniform-mutation-rate" : 0.01,
	"final-report-simplifications" : 5000
}

def test_RSWN_solution(err_func):
	#print(registered_instructions.registered_instructions)
	prog_lst = [" ", '_input1', "\n", '_string_replacechar', '_print_string', ' ', '_input1', '_string_removechar', '_char_allfromstring', '_char_stackdepth']
	prog = gp.load_program_from_list(prog_lst)
	errors = err_func(prog, debug = True)
	print("Errors:", errors)


if __name__ == "__main__":
	train_and_test = get_RSWN_train_and_test()
	#print(train_and_test)
	gp.evolution(make_RSWN_error_func_from_cases(train_and_test[0], train_and_test[1]), RSWN_params)

	#test_RSWN_solution(make_RSWN_error_func_from_cases(train_and_test[0], train_and_test[1]))

