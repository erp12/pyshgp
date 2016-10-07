# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 18:24:31 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals


import warnings

'''
List of all registered push instructions.
'''
registered_instructions = {}

def register_instruction(instruction):
	'''
	Registers an instruction, excluding duplicates.
	'''   
	if instruction.name in registered_instructions:
		warnings.warn('Duplicate instructions registered: ' + instruction.name + '. Duplicate ignored.')
	else:
		registered_instructions[instruction.name] = instruction


def get_instruction_by_name(name):
	if name[0] == "_":
		name = name[1:]
	if name in registered_instructions:
		return registered_instructions[name]
	else:
		raise Exception("No registered instruction with name: " + name)


def get_instructions_by_pysh_type(pysh_type):
	return {k:v for (k,v) in registered_instructions.items() if pysh_type in v.stack_types}


class instruction_looker_upper():
	def __init__(self, instruction_name):
		self.instruction_name = instruction_name

	def __call__(self):
		return get_instruction_by_name(self.instruction_name)

	def __repr__(self):
		return self.instruction_name[1:] + "_LOOKUP"