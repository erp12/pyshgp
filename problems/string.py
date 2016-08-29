import math
import random
import collections

from ..gp import gp
from .. import pysh_interpreter
from ..instructions import *
from ..instructions import registered_instructions as ri

'''
Take the input string, remove the last 2 characters, and then concat this result with itself.
The fitness will be the number of non-matching characters in the resulting string. For example,
desired result of "abcde" would be "abcabc", and a string of "abcabcrrr" would have an error of 3, for
3 too many characters, and the string "aaaaaa" would have error of 4, since it gets 2 of the characters right.
'''

def string_difference(s1, s2):
	'''
	Returns the difference in the strings, based on character position.
	'''
	char_lvl_diff = 0
	for c1, c2 in zip(s1, s2):
		char_lvl_diff += int(not c1 == c2)
	return char_lvl_diff + abs(len(s1) - len(s2))

def string_char_counts_difference(s1, s2):
	'''
	'''
	result = len(s1) + len(s2)
	s1_letters = collections.Counter(s1)
	for c in s2:
		if c in s1_letters:
			result -= 2
			s1_letters[c] -= 1
			if s1_letters[c] == 0:
				s1_letters.pop(c, None)
	return result


def random_str():
	s = ""
	for i in range(random.randint(1, 10)):
		s += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
	return s

def string_error_func(program):
	inputs = ["abcde", "", "E", "Hi", "Tom", "leprechaun", "zoomzoomzoom", 
				"qwertyuiopasd", "GallopTrotCanter", "Quinona", "_abc"]
	errors = []

	for inpt in inputs:
		# Create the push interpreter
		interpreter = pysh_interpreter.Pysh_Interpreter()
		interpreter.reset_pysh_state()
		
		# Push input number		
		interpreter.state.stacks["_string"].push_item(inpt)
		interpreter.state.stacks["_input"].push_item(inpt)
		# Run program
		interpreter.run_push(program)
		# Get output
		prog_output = interpreter.state.stacks["_string"].stack_ref(0)

		if type(prog_output == str):
			#compare to target output
			target_output = inpt[:-2] + inpt[:-2]
			errors.append(string_difference(prog_output, target_output) + string_char_counts_difference(prog_output, target_output))
		else:
			errors.append(1000)
	return errors

string_params = {
	"atom_generators" : ["_in1",
						 ri.get_instruction_by_name("string_length"),
						 ri.get_instruction_by_name("string_head"),
						 ri.get_instruction_by_name("string_concat"),
						 ri.get_instruction_by_name("string_stack_depth"),
						 ri.get_instruction_by_name("string_swap"),
						 ri.get_instruction_by_name("string_dup"),
						 ri.get_instruction_by_name("integer_add"),
						 ri.get_instruction_by_name("integer_sub"),
						 ri.get_instruction_by_name("integer_dup"),
						 ri.get_instruction_by_name("integer_swap"),
						 ri.get_instruction_by_name("integer_stack_depth"),
						 lambda: random.randint(0, 10),
						 lambda: random_str()],
	"population_size" : 500,
	"max_generations" : 200,
	"epigenetic_markers" : [],
    "genetic_operator_probabilities" : {"alternation" : 0.5,
										"uniform_mutation" : 0.5},
	"uniform_mutation_constant_tweak_rate" : 0.8
}

if __name__ == "__main__":
	gp.evolution(string_error_func, string_params)
