# _*_ coding: utf_8 _*_
"""
Created on 5/50/2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

#import uuid

from .. import pysh_plush_translation as tran

class Individual:
	'''
	Holds all information about an individual in a GP run.
	'''
	
	def __init__(self, genome, evo_params):
		self.genome = genome
		#self.uuid = uuid.uuid4()
		self.max_points = evo_params["max_points"]
		self.errors = []
		self.total_error = None
		self.atom_generators = evo_params["atom_generators"]
		self.program = tran.translate_plush_genome_to_push_program(genome, self.max_points, self.atom_generators)


	def get_genome(self):
		return self.genome

	def set_genome(self, genome):
		self.genome = genome
		self.program = tran.translate_plush_genome_to_push_program(self.genome, self.max_points, self.atom_generators)

	def get_program(self):
		return self.program

	def get_errors(self):
		return self.errors

	def set_errors(self, errors):
		self.errors = errors
		self.total_error = sum(errors)

	def get_total_error(self):
		return self.total_error

	def __repr__(self):
		return "Pysh_Individual"

	# def __eq__(self, other):
	# 	return str(self.genome) == str(other.get_genome())


