# -*- coding: utf-8 -*-
"""
Created on July 23, 2016

@author: Eddie
"""

import pysh_instruction

class Plush_Gene:
	'''
	Object representing a plush instruction that can be found in a linear
	plush genome.
	'''
	def __init__(self, instruction = None, closes = None, silent = None):
		self.instruction = instruction
		self.closes = closes
		self.silent = silent

	def __repr__(self):
		if type(self.instruction).__name__ == pysh_instruction.Pysh_Instruction.__name__:
			s = "PLUSH_" + self.instruction.name 
			if self.silent:
				s += "_SILENT"
			return s
		else:
			return "LITERAL_" + type(self.instruction).__name__ + "_" + str(self.instruction)