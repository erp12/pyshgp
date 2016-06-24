import pysh_state
import pysh_instruction
import pysh_utils

import registered_instructions

def boolean_and(state):
	if len(state.stacks['_boolean']) > 1:
		result = state.stacks['_bool'].stack_ref(0) and state.stacks['_bool'].stack_ref(1)
		state.stacks['_bool'].pop_item()
		state.stacks['_bool'].pop_item()
		state.stacks['_bool'].push_item(result)
	return state
boolean_and_intruction = pysh_instruction.Pysh_Instruction('_bool_and',
												  			boolean_and,
												  			stack_types = ['_bool'])
registered_instructions.register_instruction(boolean_and_intruction)



def boolean_or(state):
	if len(state.stacks['_boolean']) > 1:
		result = state.stacks['_bool'].stack_ref(0) or state.stacks['_bool'].stack_ref(1)
		state.stacks['_bool'].pop_item()
		state.stacks['_bool'].pop_item()
		state.stacks['_bool'].push_item(result)
	return state
boolean_or_intruction = pysh_instruction.Pysh_Instruction('_bool_or',
												  			boolean_or,
												  			stack_types = ['_bool'])
registered_instructions.register_instruction(boolean_or_intruction)



def boolean_not(state):
	if len(state.stacks['_boolean']) > 1:
		result = not state.stacks['_bool'].stack_ref(0)
		state.stacks['_bool'].pop_item()
		state.stacks['_bool'].push_item(result)
	return state
boolean_not_intruction = pysh_instruction.Pysh_Instruction('_bool_not',
												  			boolean_not,
												  			stack_types = ['_bool'])
registered_instructions.register_instruction(boolean_not_intruction)



def boolean_xor(state):
	if len(state.stacks['_boolean']) > 1:
		result = not (state.stacks['_bool'].stack_ref(0) == state.stacks['_bool'].stack_ref(1))
		state.stacks['_bool'].pop_item()
		state.stacks['_bool'].pop_item()
		state.stacks['_bool'].push_item(result)
	return state
boolean_xor_intruction = pysh_instruction.Pysh_Instruction('_bool_xor',
												  			boolean_xor,
												  			stack_types = ['_bool'])
registered_instructions.register_instruction(boolean_xor_intruction)



def boolean_invert_first_then_and(state):
	if len(state.stacks['_boolean']) > 1:
		result = (not state.stacks['_bool'].stack_ref(0)) and state.stacks['_bool'].stack_ref(1)
		state.stacks['_bool'].pop_item()
		state.stacks['_bool'].pop_item()
		state.stacks['_bool'].push_item(result)
	return state
boolean_invert_first_then_and_intruction = pysh_instruction.Pysh_Instruction('_boolean_invert_first_then_and', 
																		     boolean_invert_first_then_and,
												  							 stack_types = ['_bool'])
registered_instructions.register_instruction(boolean_invert_first_then_and_intruction)



def boolean_invert_second_then_and(state):
	if len(state.stacks['_boolean']) > 1:
		result = state.stacks['_bool'].stack_ref(0) and (not state.stacks['_bool'].stack_ref(1))
		state.stacks['_bool'].pop_item()
		state.stacks['_bool'].pop_item()
		state.stacks['_bool'].push_item(result)
	return state
boolean_invert_second_then_and_intruction = pysh_instruction.Pysh_Instruction('_boolean_invert_second_then_and', 
																		     boolean_invert_second_then_and,
												  							 stack_types = ['_bool'])
registered_instructions.register_instruction(boolean_invert_second_then_and_intruction)