from __future__ import absolute_import, division, print_function, unicode_literals

from .. import pysh_state
from .. import pysh_instruction

from . import registered_instructions

def boolean_and(state):
	if len(state.stacks['_boolean']) > 1:
		result = state.stacks['_boolean'].stack_ref(0) and state.stacks['_boolean'].stack_ref(1)
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].push_item(result)
	return state
boolean_and_intruction = pysh_instruction.Pysh_Instruction('boolean_and',
												  			boolean_and,
												  			stack_types = ['_boolean'])
registered_instructions.register_instruction(boolean_and_intruction)


def boolean_or(state):
	if len(state.stacks['_boolean']) > 1:
		result = state.stacks['_boolean'].stack_ref(0) or state.stacks['_boolean'].stack_ref(1)
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].push_item(result)
	return state
boolean_or_intruction = pysh_instruction.Pysh_Instruction('boolean_or',
												  			boolean_or,
												  			stack_types = ['_boolean'])
registered_instructions.register_instruction(boolean_or_intruction)



def boolean_not(state):
	if len(state.stacks['_boolean']) > 1:
		result = not state.stacks['_boolean'].stack_ref(0)
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].push_item(result)
	return state
boolean_not_intruction = pysh_instruction.Pysh_Instruction('boolean_not',
												  			boolean_not,
												  			stack_types = ['_boolean'])
registered_instructions.register_instruction(boolean_not_intruction)



def boolean_xor(state):
	if len(state.stacks['_boolean']) > 1:
		result = not (state.stacks['_boolean'].stack_ref(0) == state.stacks['_boolean'].stack_ref(1))
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].push_item(result)
	return state
boolean_xor_intruction = pysh_instruction.Pysh_Instruction('boolean_xor',
												  			boolean_xor,
												  			stack_types = ['_boolean'])
registered_instructions.register_instruction(boolean_xor_intruction)



def boolean_invert_first_then_and(state):
	if len(state.stacks['_boolean']) > 1:
		result = (not state.stacks['_boolean'].stack_ref(0)) and state.stacks['_boolean'].stack_ref(1)
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].push_item(result)
	return state
boolean_invert_first_then_and_intruction = pysh_instruction.Pysh_Instruction('boolean_invert_first_then_and', 
																		     boolean_invert_first_then_and,
												  							 stack_types = ['_boolean'])
registered_instructions.register_instruction(boolean_invert_first_then_and_intruction)



def boolean_invert_second_then_and(state):
	if len(state.stacks['_boolean']) > 1:
		result = state.stacks['_boolean'].stack_ref(0) and (not state.stacks['_boolean'].stack_ref(1))
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].push_item(result)
	return state
boolean_invert_second_then_and_intruction = pysh_instruction.Pysh_Instruction('boolean_invert_second_then_and', 
																		     boolean_invert_second_then_and,
												  							 stack_types = ['_boolean'])
registered_instructions.register_instruction(boolean_invert_second_then_and_intruction)