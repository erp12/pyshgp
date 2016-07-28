# _*_ coding: utf_8 _*_
"""
Created on 5/22/2016

@author: Eddie
"""
import copy
import random

import pysh_utils as u

def auto_simplify(individual, error_function, steps):
	print "Autosimplifying program of size:", u.count_points(individual.get_program())

	for step in range(steps):
		old_genome = individual.get_genome()
		initial_error_vector = individual.get_errors()
		# Pick the index of the gene you want to silence
		genes_to_silence = [random.randint(0,len(individual.get_genome())-1)]
		# Possibly silence another gene
		if random.random() < 0.5 :
			genes_to_silence.append(random.randint(0,len(individual.get_genome())-1))

		# Silence the gene(s)
		new_genome = copy.deepcopy(individual.get_genome())
		for i in genes_to_silence:
			if not new_genome[i].silent:
				new_genome[i].silent = True

		# Make sure the program still performs the same
		individual.set_genome(new_genome)
		new_error = error_function(individual.get_program())

		# reset genes if no improvment was made
		if not new_error == initial_error_vector:
			individual.set_genome(old_genome)

	print "Finished simplifying program. New size:", u.count_points(individual.get_program())
	print individual.get_program()