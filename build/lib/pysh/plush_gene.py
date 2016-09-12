# -*- coding: utf-8 -*-
"""
Created on July 23, 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

from . import instruction

# class Plush_Gene:
# 	'''
# 	Object representing a plush instruction that can be found in a linear
# 	plush genome.
# 	'''
# 	def __init__(self, instruction = None, is_literal = False, closes = None, silent = None):
# 		self.instruction = instruction
# 		self.closes = closes
# 		self.silent = silent
# 		self.is_literal = is_literal

# 	def __repr__(self):
# 		if not self.is_literal:
# 			s = "PLUSH_" + self.instruction 
# 			if self.silent:
# 				s += "_SILENT"
# 			return s
# 		else:
# 			return "LITERAL_" + type(self.instruction).__name__ + "_" + str(self.instruction)



def make_plush_gene(instruction, is_literal = False, closes = None, silent = None):
	return (instruction, is_literal, closes, silent)

def plush_gene_print(gene):
	if not gene[1]:
		s = "PLUSH_" + gene[0] 
		if gene[3]:
			s += "_SILENT"
		return s
	else:
		return "LITERAL_" + type(gene[0]) + "_" + gene[0]

def plush_gene_get_instruction(gene):
	return gene[0]

def plush_gene_is_literal(gene):
	return gene[1]

def plush_gene_get_closes(gene):
	return gene[2]

def plush_gene_is_silent(gene):
	return gene[3]