# -*- coding: utf-8 -*-
"""
Created on Sun Jun 6 2016

@author: Eddie
"""
import random

import pysh_globals as g
import pysh_utils as u
import pysh_instruction
import pysh_plush_translation


class Plush_Instruction:
	'''
	Object representing a plush instruction.
	'''
	def __init__(self, instruction = None, closes = None, silent = None):
		self.instruction = instruction
		self.closes = closes
		self.silent = silent



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

def random_plush_instruction(atom_generators):
	'''
	Returns a random Plush_Instruction object given the atom_generators 
	and the required epigenetic-markers.
	'''
	markers = g.pysh_argmap['epigenetic_markers']
	markers.append('_instruction')

	new_plush_instruction = Plush_Instruction()
	for m in markers:
		if m == '_instruction':
			element = random.choice(atom_generators)
			if type(element).__name__ == pysh_instruction.Pysh_Instruction.__name__:
				new_plush_instruction.instruction = element # It's an instruction!
			elif callable(element): # It's a function
				fn_element = element() 
				if callable(fn_element): # It's another function!
					new_plush_instruction.instruction = fn_element()
				else:
					new_plush_instruction.instruction = fn_element 
			else:
				raise Exception("Encountered strange _instruction epigenetic marker.")
		elif m == '_close':
			random_closes(g.pysh_argmap['close_parens_probabilities'])
		elif m == '_silent':
			if random.random() > g.pysh_argmap['silent_instruction_probability']:
				new_plush_instruction.silent = True
			else:
				new_plush_instruction.silent = False
		else:
			raise Exception("Unknown epigenetic marker type.")

def random_plush_genome_with_size(genome_size, atom_generators):
	'''
	Returns a random Plush genome (aka list of Plush_Instruction objects)
	containing the given number of points.
	'''
	genome = []
	for i in range(genome_size):
		genome.append(random_plush_instruction(atom_generators))
	return genome

def random_plush_genome(max_genome_size, atom_generators):
	'''
	Returns a random Plush genome with size limited by max_genome_size.
	'''
	genome_size = random.randint(1, max_genome_size)
	return random_plush_genome_with_size(genome_size, atom_generators)


#################################
# random push code generator


def random_push_code(max_points, atom_generators = g.pysh_argmap['atom_generators']):
	'''
	Returns a random Push expression with size limited by max_points.
	'''
	max_genome_size = max(int(max_points /  2), 1)
	return pysh_plush_translation.translate_plush_genome_to_push_program(random_plush_genome(max_genome_size, atom_generators))
	

