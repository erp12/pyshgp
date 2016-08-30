# _*_ coding: utf_8 _*_
"""
Created on 5/50/2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import math
import random

from .. import plush_gene as pl
from .. import pysh_random

#############
# Utilities #
#############

def gaussian_noise_factor():
	"""
	Returns gaussian noise of mean 0, std dev 1.
	"""
	return math.sqrt(-2.0 * math.log(random.random())) * math.cos(2.0 * math.pi * random.random()) 

def perturb_with_gaussian_noise(sd, n):
	"Returns n perturbed with std dev sd."
	return n + (sd * gaussian_noise_factor())


#############################
# Crossover and Alternation #
#############################

def alternation(parent_1, parent_2, evo_params):
	"""
	Uniformly alternates between the two parent.
	parent_1 and parent_2 are plush genomes.
	"""
	resulting_genome = []

	# Random pick which parent to start from
	use_parent_1 = random.choice([True, False])

	loop_times = len(parent_1)
	if not use_parent_1:
		loop_times = len(parent_2)

	i = 0
	while (i < loop_times) and (len(resulting_genome) < evo_params["max_points"]):
		if random.random() < evo_params["alternation_rate"]:
			# Switch which parent we are pulling genes from
			i += round(evo_params["alignment_deviation"] * gaussian_noise_factor())
			i = int(max(0, i))
			use_parent_1 = not use_parent_1
		else:
			# Pull gene from parent
			if use_parent_1:
				resulting_genome.append(parent_1[i])
			else:
				resulting_genome.append(parent_2[i])
			i = int(i+1)

		# Change loop stop condition
		loop_times = len(parent_1)
		if not use_parent_1:
			loop_times = len(parent_2)

	return resulting_genome


#############
# Mutations #
#############

def string_tweak(s, evo_params):
	new_s = ""
	for c in s:
		if random.random() < evo_params['uniform_mutation_string_char_change_rate']:
			new_s += random.choice(['\t', '\n'] + list(map(chr, range(32, 127))))
		else:
			new_s += c
	return new_s

def instruction_mutator(evo_params):
	return pysh_random.random_plush_instruction(evo_params)

def constant_mutator(token, evo_params):
	new_token = pl.Plush_Gene()

	const = token.instruction
	if type(const) == float:
		new_token.instruction = perturb_with_gaussian_noise(evo_params["uniform_mutation_float_gaussian_standard_deviation"], const)
	elif type(const) == int:
		new_token.instruction = round(perturb_with_gaussian_noise(evo_params["uniform_mutation_float_gaussian_standard_deviation"], const))
	elif type(const) == str:
		new_token.instruction = string_tweak(const, evo_params)
	elif type(const) == bool:
		random.choice([True, False])
	else:
		new_token = instruction_mutator(evo_params)
	return new_token

def token_mutator(token, evo_params):
	new_token = token
	if random.random() < evo_params["uniform_mutation_rate"]:
		if random.random() < evo_params["uniform_mutation_constant_tweak_rate"]:
			new_token = constant_mutator(token, evo_params)
		else:
			new_token = instruction_mutator(evo_params)
	return new_token


def uniform_mutation(genome, evo_params):
	"""
	Uniformly mutates individual. For each token in program, there is
	uniform-mutation-rate probability of being mutated. If a token is to be
	mutated, it has a uniform-mutation-constant-tweak-rate probability of being
	mutated using a constant mutator (which varies depending on the type of the
	token), and otherwise is replaced with a random instruction.
	"""
	new_genome = list(map(lambda gene: token_mutator(gene, evo_params), genome))
	return new_genome




