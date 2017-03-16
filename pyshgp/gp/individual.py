# _*_ coding: utf_8 _*_
"""
The :mod:`individual` module defines the ``Individual`` class which represents
an individual in the evolution run.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

from ..push import translation as tran

class Individual:
	"""Holds all information about an individual. 
	"""

	#: List of plush genes (tuples) that create the genome.
	genome = None
	#: Max size the program can after after translated into genome.
	max_points = None
	#: List of errors on each test case.
	errors = None
	#: Sum of errors.
	total_error = None
	#: Atom generators being used in the current GP run.
	atom_generators = None
	#: List of Instruction objects and literals that can be executed by the push interpreter.
	program = None
	
	def __init__(self, genome, evo_params):
		self.genome = genome
		self.max_points = evo_params["max_points"]
		self.errors = []
		self.total_error = None
		self.atom_generators = evo_params["atom_generators"]
		self.program = tran.translate_plush_genome_to_push_program(genome, self.max_points)

	# Getters and Setters

	def get_genome(self):
		"""
		:returns: The individual's genome.
		"""
		return self.genome

	def set_genome(self, genome):
		"""Sets individual's genome, and translates it into it's Push program.

		:param list genome: List of Plush gene tuples.
		"""
		self.genome = genome
		self.program = tran.translate_plush_genome_to_push_program(self.genome, self.max_points)

	def get_program(self):
		"""
		:returns: The individual's program.
		"""
		return self.program

	def get_errors(self):
		"""
		:returns: The program's error vector.
		"""
		return self.errors

	def set_errors(self, errors):
		"""Sets the individual's error vector and total error.

		:param list error: List of errors.
		"""
		self.errors = errors
		self.total_error = sum(errors)

	def get_total_error(self):
		"""
		:returns: The inidividual's total error.
		"""
		return self.total_error

	def __repr__(self):
		return "PyshIndividual<"+str(self.total_error)+">"

	# def __eq__(self, other):
	# 	return str(self.genome) == str(other.get_genome())


