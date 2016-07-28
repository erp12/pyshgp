# -*- coding: utf-8 -*-
"""
Created on Sun Jun  17, 2016

@author: Eddie
"""

from .. import pysh_state
from .. import pysh_instruction

import registered_instructions


def exec_do_range(state):
	'''
	Differs from code.do*range only in the source of the code and the recursive call.
	'''
	if len(state.stacks['_exec']) > 0 and len(state.stacks['_integer']) > 1:
		to_do = state.stacks['_exec'].stack_ref(0)
		current_index = state.stacks['_integer'].stack_ref(1)
		destination_index = state.stacks['_integer'].stack_ref(0)
		state.stacks['_integer'].pop_item()
		state.stacks['_integer'].pop_item()
		state.stacks['_exec'].pop_item()

		increment = 0
		if current_index < destination_index:
			increment = 1
		elif current_index > destination_index:
			increment = 0

		if not increment == 0:
			state.stacks['_exec'].push_item([(current_index + increment), 
											  destination_index, 
											  registered_instructions.get_instruction_by_name('_exec_do*range'), 
											  to_do])

		state.stacks['_integer'].push_item(current_index)
		state.stacks['_exec'].push_item(to_do)
	return state

exec_do_range_intruction = pysh_instruction.Pysh_Instruction('exec_do*range',
												  			 exec_do_range,
												  			 stack_types = ['_exec', '_integer'],
												  			 parentheses = 1)
registered_instructions.register_instruction(exec_do_range_intruction)



def exec_do_count(state):
	'''
	differs from code.do*count only in the source of the code and the recursive call
	'''
	if not (len(state.stacks['_integer']) == 0 or state.stacks['_integer'] < 1 or len(state.stacks['_exec']) == 0):
		to_push = [0, 
				   state.stacks['_integer'].stack_ref(0) - 1, 
				   registered_instructions.get_instruction_by_name('_exec_do*range'),
				   state.stacks['_exec'].stack_ref(0)]
		state.stacks['_exec'].pop_item()
		state.stacks['_integer'].pop_item()
		state.stacks['_exec'].push_item(to_push)
	return state

exec_do_count_intruction = pysh_instruction.Pysh_Instruction('exec_do*count',
												  			 exec_do_count,
												  			 stack_types = ['_exec', '_integer'],
												  			 parentheses = 1)
registered_instructions.register_instruction(exec_do_count_intruction)