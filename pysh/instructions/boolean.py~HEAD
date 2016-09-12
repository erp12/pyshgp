from __future__ import absolute_import, division, print_function, unicode_literals

from .. import pysh_state
from .. import instruction as instr

from . import registered_instructions

def boolean_and(state):
	if len(state.stacks['_boolean']) > 1:
		result = state.stacks['_boolean'].stack_ref(0) and state.stacks['_boolean'].stack_ref(1)
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].push_item(result)
	return state
boolean_and_intruction = instr.Pysh_Instruction('boolean_and',
												  			boolean_and,
												  			stack_types = ['_boolean'])
registered_instructions.register_instruction(boolean_and_intruction)
#<instr_open>
#<instr_name>boolean_and
#<instr_desc>Pushes the logical AND of the top two booleans.
#<instr_close>


def boolean_or(state):
	if len(state.stacks['_boolean']) > 1:
		result = state.stacks['_boolean'].stack_ref(0) or state.stacks['_boolean'].stack_ref(1)
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].push_item(result)
	return state
boolean_or_intruction = instr.Pysh_Instruction('boolean_or',
												  			boolean_or,
												  			stack_types = ['_boolean'])
registered_instructions.register_instruction(boolean_or_intruction)
#<instr_open>
#<instr_name>boolean_or
#<instr_desc>Pushes the logical OR of the top two booleans.
#<instr_close>


def boolean_not(state):
	if len(state.stacks['_boolean']) > 0:
		result = not state.stacks['_boolean'].stack_ref(0)
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].push_item(result)
	return state
boolean_not_intruction = instr.Pysh_Instruction('boolean_not',
												  			boolean_not,
												  			stack_types = ['_boolean'])
registered_instructions.register_instruction(boolean_not_intruction)
#<instr_open>
#<instr_name>boolean_not
#<instr_desc>Pushes the logical NOT of the top boolean.
#<instr_close>


def boolean_xor(state):
	if len(state.stacks['_boolean']) > 1:
		result = not (state.stacks['_boolean'].stack_ref(0) == state.stacks['_boolean'].stack_ref(1))
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].push_item(result)
	return state
boolean_xor_intruction = instr.Pysh_Instruction('boolean_xor',
												  			boolean_xor,
												  			stack_types = ['_boolean'])
registered_instructions.register_instruction(boolean_xor_intruction)
#<instr_open>
#<instr_name>boolean_xor
#<instr_desc>Pushes the logical XOR of the top two booleans.
#<instr_close>


def boolean_invert_first_then_and(state):
	if len(state.stacks['_boolean']) > 1:
		result = (not state.stacks['_boolean'].stack_ref(0)) and state.stacks['_boolean'].stack_ref(1)
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].push_item(result)
	return state
boolean_invert_first_then_and_intruction = instr.Pysh_Instruction('boolean_invert_first_then_and', 
																		     boolean_invert_first_then_and,
												  							 stack_types = ['_boolean'])
registered_instructions.register_instruction(boolean_invert_first_then_and_intruction)
#<instr_open>
#<instr_name>boolean_invert_first_then_and
#<instr_desc>Pushes the logical AND of the top two booleans, with the fist argument inverted.
#<instr_close>


def boolean_invert_second_then_and(state):
	if len(state.stacks['_boolean']) > 1:
		result = state.stacks['_boolean'].stack_ref(0) and (not state.stacks['_boolean'].stack_ref(1))
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].pop_item()
		state.stacks['_boolean'].push_item(result)
	return state
boolean_invert_second_then_and_intruction = instr.Pysh_Instruction('boolean_invert_second_then_and', 
																		     boolean_invert_second_then_and,
												  							 stack_types = ['_boolean'])
registered_instructions.register_instruction(boolean_invert_second_then_and_intruction)
#<instr_open>
#<instr_name>boolean_invert_second_then_and
#<instr_desc>Pushes the logical AND of the top two booleans, with the second argument inverted.
#<instr_close>