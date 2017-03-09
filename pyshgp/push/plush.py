# -*- coding: utf-8 -*-

"""
The :mod:`plush` module defines functions that create tuples that represent 
genes in a Plush genome.

Plush genomes are linear representations of Push programs.
Plush genomes are python lists of plush genes.
Plush genes are python tuples.

.. todo::
    Consider change plush gene back to a class, opposed to immutable tuples. 
"""


from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

def make_plush_gene(instruction, is_literal = False, closes = None, silent = None):
	"""Creates a plush gene tuple from an instruction ojbect.

	:param PushInstruction instruction: An instance of the instruction class.
	:param bool is_literal: Denotes if the gene is holding a literal or an instruction.
	:param int closes: The close epigenetic marker. Denotes how many close parens to place after instruction in program.
	:param bool silent: If true, do not include instruction in translated program.
	:returns: Tuple containing all gene information.
	"""
	return (instruction, is_literal, closes, silent)

def plush_gene_to_string(gene):
	"""Returns a single string representing the gene.

	:param tuple gene: Plush gene to print.
	:returns: String of gene.
	"""
	if not gene[1]:
		s = "PLUSH_" + gene[0] 
		if gene[3]:
			s += "_SILENT"
		return s
	else:
		return "LITERAL_" + type(gene[0]) + "_" + gene[0]

def plush_gene_get_instruction(gene):
	"""Returns a gene's instruction.

	:param tuple gene: The gene.
	:returns: Instruction
	"""
	return gene[0]

def plush_gene_is_literal(gene):
	"""Return if a gene is a literal or not.

	:param tuple gene: The gene.
	:returns: Boolean where ``true`` if gene is a literal.
	"""
	return gene[1]

def plush_gene_get_closes(gene):
	"""Returns a gene's number of close markers.

	:param tuple gene: The gene.
	:returns: Integer denoting number of close markers on the gene.
	"""
	return gene[2]

def plush_gene_is_silent(gene):
	"""Returns if a gene is silent or not.

	:param tuple gene: The gene.
	:returns: Boolean where ``true`` if gene is silent.
	"""
	return gene[3]