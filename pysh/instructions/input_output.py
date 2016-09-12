# -*- coding: utf-8 -*-
"""
Created on July 24, 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from .. import pysh_state
from .. import instruction as instr
from .. import utils as u



def handle_input_instruction(instruction, state):
	'''
	Allows Push to handle inN instructions, e.g. in2, using things from the input
	stack. We can tell whether a particular inN instruction is valid if N-1
	values are on the input stack.
	'''
	input_depth = int(instruction.name.split("input")[1]) - 1
	input_value = state.stacks['_input'].stack_ref(input_depth)
	pysh_type = u.recognize_pysh_type(input_value)

	if pysh_type == '_instruction':
		state.stacks['_exec'].push_item(input_value)
	elif pysh_type == '_list':
		state.stacks['_exec'].push_item(input_value)
	else:
		state.stacks[pysh_type].push_item(input_value)