# -*- coding: utf-8 -*-
"""
Created on July 23, 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

'''
Plush genomes are linear representations of Push programs.
Plush genomes are python lists of plush genes.
Plush genes are python tuples.
'''


def make_plush_gene(instruction, is_literal = False, closes = None, silent = None):
	'''Creates a plush gene tuple from an instruction ojbect.

	Args:
		instruction: An instance of the instruction class.
		is_literal (bool): Denotes if the gene is holding a literal or an instruction.
		closes (int): The close epigenetic marker. Denotes how many close parens to place after instruction in program.
		silent (bool): If true, do not include instruction in translated program.
	'''
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