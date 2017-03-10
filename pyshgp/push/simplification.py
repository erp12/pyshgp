# _*_ coding: utf_8 _*_
"""
The :mod:`simplification` module defines method of automatically simplifying
Push genomes and Push programs. 

.. todo::
    Genome simplification is very simplistic in its current state. This should
    be overhauled at some point to match the recent developments in
    simplification found in Clojush.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import random
import copy

from .. import utils as u

from . import plush as pl

def auto_simplify(individual, error_function, steps):
	'''Simplifies the genome (and program) of the individual based on error_function.

	At each step, 1 or 2 random gene are silenced from the individual's genome.
	The genome is translated into a program which is then run through the 
	error_funciton. If the errors of the program are equal or lower, the gene(s)
	remain silenced. Otherwise they are un-silenced. 

	.. todo::
	    Add bool to toggle printing.

	:param Individual individual: Individual to simplify (The genome, program, 
		and error vector are needed.)
	:param function error_function: Error function.
	:param int steps: Number of simplification iterations.
	:returns: A new individual with a simplified program that performs the same.

	'''
	print("Autosimplifying program of size:", u.count_points(individual.get_program()))

	for step in range(steps):
		old_genome = individual.get_genome()
		initial_error_vector = individual.get_errors()
		# Pick the index of the gene you want to silence
		genes_to_silence = [random.randint(0,len(individual.get_genome())-1)]
		# Possibly silence another gene
		if random.random() < 0.5 :
			genes_to_silence.append(random.randint(0,len(individual.get_genome())-1))

		# Silence the gene(s)
		new_genome = copy.copy(individual.get_genome())
		for i in genes_to_silence:
			if not pl.plush_gene_is_silent(new_genome[i]):
				new_genome[i] = pl.make_plush_gene(new_genome[i][0], new_genome[i][1], new_genome[i][2], True)

		# Make sure the program still performs the same
		individual.set_genome(new_genome)
		new_error = error_function(individual.get_program())

		# reset genes if no improvment was made
		if not new_error <= initial_error_vector:
			individual.set_genome(old_genome)

	print("Finished simplifying program. New size:", u.count_points(individual.get_program()))
	print(individual.get_program())
	return individual