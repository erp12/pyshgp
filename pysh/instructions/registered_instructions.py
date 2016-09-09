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
registered_instructions = []


def register_instruction(instruction):
	'''
	Registers an instruction, excluding duplicates.
	'''   
	if len([x for x in registered_instructions if x.name == instruction.name]) > 0:
		warnings.warn('Duplicate instructions registered: ' + instruction.name + '. Duplicate ignored.')
	else:
		registered_instructions.append(instruction)


def get_instruction_by_name(name):
	if name[0] == "_":
		name = name[1:]
	instr = [x for x in registered_instructions if x.name == name]
	if len(instr) == 0:
		raise Exception("No registered instruction with name: " + name)
	else:
		return instr[0]