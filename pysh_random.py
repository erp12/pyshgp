# -*- coding: utf-8 -*-
"""
Created on Sun Jun 6 2016

@author: Eddie
"""
import random

import pysh_utils as u
import pysh_globals as g
import pysh_instruction
import pysh_plush_translation
import plush_instruction as pl



#################################
# random plush genome generator


def random_closes(close_parens_probabilities):
	'''
	Returns a random number of closes based on close_parens_probabilities, which
	defaults to [0.772 0.206 0.021 0.001]. This is roughly equivalent to each selection
	coming from  a binomial distribution with n=4 and p=1/16.
		(see http://www.wolframalpha.com/input/?i=binomial+distribution+4+0.0625)
	This results in the following probabilities:
		p(0) = 0.772
		p(1) = 0.206
		p(2) = 0.021
		p(3) = 0.001
	'''
	prob = random.random()
	probabilities = u.reductions(lambda i, j: i + j, close_parens_probabilities) + [1.0]
	parens = 0

	while prob > probabilities[1]:
		parens += 1
		del probabilities[0]
	return parens

def random_plush_instruction(evo_params):
	'''
	Returns a random Plush_Instruction object given the atom_generators 
	and the required epigenetic-markers.
	'''
	markers = evo_params["epigenetic_markers"]
	markers.append('_instruction')

	new_plush_gene = pl.Plush_Gene()
	for m in markers:
		if m == '_instruction':
			element = random.choice(evo_params["atom_generators"])
			if type(element).__name__ == pysh_instruction.Pysh_Instruction.__name__:
				new_plush_gene.instruction = element # It's an instruction!
			elif callable(element): # It's a function
				fn_element = element() 
				if callable(fn_element): # It's another function!
					new_plush_gene.instruction = fn_element()
				else:
					new_plush_gene.instruction = fn_element 
			elif type(element) == str and element.startswith("_in") and not element.startswith("_int"):
			     # Its an input instruction!
			     new_plush_gene.instruction = pysh_instruction.Pysh_Input_Instruction(element)
			else:
				raise Exception("Encountered strange _instruction epigenetic marker: " + element)
		elif m == '_close':
			new_plush_gene.closes = random_closes(evo_params['close_parens_probabilities'])
		elif m == '_silent':
			if random.random() > evo_params['silent_instruction_probability']:
				new_plush_gene.silent = True
			else:
				new_plush_gene.silent = False
		else:
			raise Exception("Unknown epigenetic marker type.")
	return new_plush_gene

def random_plush_genome_with_size(genome_size, evo_params):
	'''
	Returns a random Plush genome (aka list of Plush_Instruction objects)
	containing the given number of points.
	'''
	genome = []
	for i in range(genome_size):
		genome.append(random_plush_instruction(evo_params))
	return genome

def random_plush_genome(evo_params):
	'''
	Returns a random Plush genome with size limited by max_genome_size.
	'''
	genome_size = random.randint(1, evo_params["max_genome_initial_size"])
	return random_plush_genome_with_size(genome_size, evo_params)


#################################
# random push code generator


def random_push_code(max_points, evo_params):
	'''
	Returns a random Push expression with size limited by max_points.
	'''
	max_genome_size = max(int(max_points /  2), 1)
	return pysh_plush_translation.translate_plush_genome_to_push_program(random_plush_genome(max_genome_size, evo_params))
	