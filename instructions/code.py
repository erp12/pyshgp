# -*- coding: utf-8 -*-
"""
Created on Sun Jun  17, 2016

@author: Eddie
"""

from .. import pysh_state
from .. import pysh_instruction
from .. import pysh_utils as u

import registered_instructions


exec_noop_instruction = pysh_instruction.Pysh_Instruction('exec_noop',
														   lambda state: state,
														   stack_types = ['_exec'])
registered_instructions.register_instruction(exec_noop_instruction)

code_noop_instruction = pysh_instruction.Pysh_Instruction('code_noop',
															lambda state: state,
															stack_types = ['_code'])
registered_instructions.register_instruction(code_noop_instruction)


def code_append(state):
	if len(state.stacks['_code']) > 1:
		new_item = u.ensure_list(state.stacks['_code'].stack_ref(0)) + u.ensure_list(state.stacks['_code'].stack_ref(1))
		state.stacks['_code'].pop_item()
		state.stacks['_code'].pop_item()
		state.stacks['_code'].push_item(new_item)
	return state
code_append_instruction = pysh_instruction.Pysh_Instruction('code_append',
	                                                        code_append,
	                                                        stack_types = ['_code'])
registered_instructions.register_instruction(code_append_instruction)


def code_atom(state):
	if len(state.stacks['_code']) > 0:
		top_code = state.stacks['_code'].stack_ref(0)
		state.stacks['_code'].pop_item()
		state.stacks['_boolean'].push_item(not (type(top_code) == list))
	return state
code_atom_instruction = pysh_instruction.Pysh_Instruction('code_atom',
														  code_atom,
														  stack_types = ['_code', '_boolean'])
registered_instructions.register_instruction(code_atom_instruction)


def code_car(state):
	if len(state.stacks['_code']) > 0 and len(u.ensure_list(state.stacks['_code'].stack_ref(0))) > 0:
		top_code = u.ensure_list(state.stacks['_code'].stack_ref(0))[0]
		state.stacks['_code'].pop_item()
		state.stacks['_code'].push_item(top_code)
	return state
code_car_instruction = pysh_instruction.Pysh_Instruction('code_car',
														 code_car,
														 stack_types = ['_code'])
registered_instructions.register_instruction(code_car_instruction)


def code_cdr(state):
	if len(state.stacks['_code']) > 0:
		top_code = u.ensure_list(state.stacks['_code'].stack_ref(0))[1:]
		state.stacks['_code'].pop_item()
		state.stacks['_code'].push_item(top_code)
	return state		
code_cdr_instruction = pysh_instruction.Pysh_Instruction('code_cdr',
														 code_cdr,
														 stack_types = ['_code'])
registered_instructions.register_instruction(code_cdr_instruction)


def code_cons(state):
	if len(state.stacks['_code']) > 1:
		new_item = [state.stacks['_code'].stack_ref(1)] + u.ensure_list(state.stacks['_code'].stack_ref(0))
		state.stacks['_code'].pop_item()
		state.stacks['_code'].push_item(new_item)
	return state
code_cons_instruction = pysh_instruction.Pysh_Instruction('code_cons',
														  code_cons,
														  stack_types = ['_code'])
registered_instructions.register_instruction(code_cons_instruction)


def code_do(state):
	if len(state.stacks['_code']) > 0:
		top_code = state.stacks['_code'].stack_ref(0)
		state.stacks['_exec'].push_item('_code_pop')
		state.stacks['_exec'].push_item(top_code)
	return state
code_do_instruction = pysh_instruction.Pysh_Instruction('code_do',
														code_do,
														stack_types = ['_code', '_exec'])
registered_instructions.register_instruction(code_do_instruction)



def code_do_star(state):
	if len(state.stacks['_code']) > 0:
		top_code = state.stacks['_code'].stack_ref(0)
		state.stacks['_exec'].push_item(top_code)
	return state
code_do_star_instruction = pysh_instruction.Pysh_Instruction('code_do*',
															 code_do_star,
															 stack_types = ['_code', '_exec'])
registered_instructions.register_instruction(code_do_star_instruction)


def code_do_range(state):
	if len(state.stacks['_code']) > 0 and len(state.stacks['_code']) > 1:
		to_do = state.stacks['_code'].stack_ref(0)
		current_index = state.stacks['_integer'].stack_ref(1)
		destination_index = state.stacks['_integer'].stack_ref(0)
		state.stacks['_integer'].pop_item()
		state.stacks['_integer'].pop_item()
		state.stacks['_code'].pop_item()

		increment = 0
		if current_index < destination_index:
			increment = 1
		elif current_index > destination_index:
			increment = -1

		if not increment == 0:
			state.stacks['_exec'].push_item([(current_index + increment), 
											  destination_index, 
											  '_code_quote', 
											  to_do,
											  '_code_do_range'])
		state.stacks['_integer'].push_item(current_index)
		state.stacks['_exec'].push_item(to_do)
	return state
code_do_range_intruction = pysh_instruction.Pysh_Instruction('code_do*range',
												  			 code_do_range,
												  			 stack_types = ['_exec', '_integer', '_code'])
registered_instructions.register_instruction(code_do_range_intruction)


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
			increment = -1

		if not increment == 0:
			state.stacks['_exec'].push_item([(current_index + increment), 
											  destination_index, 
											  '_exec_do*range', 
											  to_do])

		state.stacks['_integer'].push_item(current_index)
		state.stacks['_exec'].push_item(to_do)
	return state

exec_do_range_intruction = pysh_instruction.Pysh_Instruction('exec_do*range',
												  			 exec_do_range,
												  			 stack_types = ['_exec', '_integer'],
												  			 parentheses = 1)
registered_instructions.register_instruction(exec_do_range_intruction)


def code_do_count(state):
	if not (len(state.stacks['_integer']) == 0 or state.stacks['_integer'].stack_ref(0) < 1 or len(state.stacks['_code']) == 0):
		to_push = [0, 
				   state.stacks['_integer'].stack_ref(0) - 1, 
				   '_code_quote',
				   state.stacks['_code'].stack_ref(0),
				   'code_do*range']
		state.stacks['_code'].pop_item()
		state.stacks['_integer'].pop_item()
		state.stacks['_exec'].push_item(to_push)
	return state

code_do_count_intruction = pysh_instruction.Pysh_Instruction('code_do*count',
												  			 code_do_count,
												  			 stack_types = ['_exec', '_integer', '_code'])
registered_instructions.register_instruction(code_do_count_intruction)


def exec_do_count(state):
	'''
	differs from code.do*count only in the source of the code and the recursive call
	'''
	if not (len(state.stacks['_integer']) == 0 or state.stacks['_integer'].stack_ref(0) < 1 or len(state.stacks['_exec']) == 0):
		to_push = [0, 
				   state.stacks['_integer'].stack_ref(0) - 1, 
				   '_exec_do*range',
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


def code_do_times(state):
	if not (len(state.stacks['_integer']) == 0 or state.stacks['_integer'].stack_ref(0) < 1 or len(state.stacks['_code']) == 0):
		to_push = [0,
		           state.stacks['_integer'].stack_ref(0) - 1,
		           '_code_quote',
		           ['_integer_pop'] + u.ensure_list(state.stacks['_exec'].stack_ref(0)),
		           '_code_do*range']
		state.stacks['_code'].pop_item()
		state.stacks['_integer'].pop_item()
		state.stacks['_exec'].push_item(to_push)
code_do_times_intruction = pysh_instruction.Pysh_Instruction('code_do*times',
												  			 code_do_times,
												  			 stack_types = ['_code', '_integer'])
registered_instructions.register_instruction(code_do_times_intruction)


def exec_do_times(state):
	'''
	differs from code.do*times only in the source of the code and the recursive call
	'''
	if not (len(state.stacks['_integer']) == 0 or state.stacks['_integer'].stack_ref(0) < 1 or len(state.stacks['_exec']) == 0):
		to_push = [0, 
				   state.stacks['_integer'].stack_ref(0) - 1, 
				   '_exec_do*range',
				   ['_integer_pop'] + u.ensure_list(state.stacks['_exec'].stack_ref(0))]
		state.stacks['_exec'].pop_item()
		state.stacks['_integer'].pop_item()
		state.stacks['_exec'].push_item(to_push)
	return state

exec_do_times_intruction = pysh_instruction.Pysh_Instruction('exec_do*times',
												  			 exec_do_times,
												  			 stack_types = ['_exec', '_integer'],
												  			 parentheses = 1)
registered_instructions.register_instruction(exec_do_times_intruction)


def exec_while(state):
	if len(state.stacks['_exec']) > 0:
		if len(state.stacks['_boolean']) == 0:
			state.stacks['_exec'].pop_item()
		elif not state.stacks['_boolean'].stack_ref(0):
			state.stacks['_exec'].pop_item()
			state.stacks['_boolean'].pop_item()
		else:
			block = state.stacks['_exec'].stack_ref(0)
			state.stacks['_exec'].push_item('_exec_while')
			state.stacks['_exec'].push_item(block)
			state.stacks['_boolean'].pop_item()
	return state
exec_while_intruction = pysh_instruction.Pysh_Instruction('exec_while',
												  	      exec_while,
												  		  stack_types = ['_exec', '_boolean'],
												  		  parentheses = 1)
registered_instructions.register_instruction(exec_while_intruction)


def exec_do_while(state):
	if len(state.stacks['_exec']) > 0:
			block = state.stacks['_exec'].stack_ref(0)
			state.stacks['_exec'].push_item('_exec_while')
			state.stacks['_exec'].push_item(block)
	return state
exec_do_while_intruction = pysh_instruction.Pysh_Instruction('exec_do*while',
															 exec_do_while,
															 stack_types = ['_exec', '_boolean'],
															 parentheses = 1)
registered_instructions.register_instruction(exec_do_while_intruction)



# Code Map

