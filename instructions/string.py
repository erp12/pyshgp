from .. import pysh_state
from .. import pysh_instruction
from .. import pysh_utils

import registered_instructions


def string_from_integer(state):
	if len(state.stacks['_integer']) > 0:
		top_int = state.stacks['_integer'].stack_ref(0)
		state.stacks['_integer'].pop_item()
		state.stacks['_string'].push_item(str(top_int))
	return state
string_from_integer_intruction = pysh_instruction.Pysh_Instruction('string_from_integer',
												  					string_from_integer,
												  					stack_types = ['_string', '_integer'])
registered_instructions.register_instruction(string_from_integer_intruction)


def string_from_float(state):
	if len(state.stacks['_float']) > 0:
		top_float = state.stacks['_float'].stack_ref(0)
		state.stacks['_float'].pop_item()
		state.stacks['_string'].push_item(str(top_float))
	return state
string_from_float_intruction = pysh_instruction.Pysh_Instruction('string_from_float',
												  					string_from_float,
												  					stack_types = ['_string', '_float'])
registered_instructions.register_instruction(string_from_float_intruction)


def string_from_boolean(state):
	if len(state.stacks['_boolean']) > 0:
		top_float = state.stacks['_boolean'].stack_ref(0)
		state.stacks['_boolean'].pop_item()
		state.stacks['_string'].push_item(str(top_float))
	return state
string_from_boolean_intruction = pysh_instruction.Pysh_Instruction('string_from_boolean',
												  					string_from_boolean,
												  					stack_types = ['_string', '_boolean'])
registered_instructions.register_instruction(string_from_boolean_intruction)


def string_concat(state):
	if len(state.stacks['_string']) > 1:
		s1 = state.stacks['_string'].stack_ref(0)
		s2 = state.stacks['_string'].stack_ref(0)
		state.stacks['_string'].pop_item()
		state.stacks['_string'].pop_item()
		state.stacks['_string'].push_item(s1 + s2)
	return state
string_concat_instruction = pysh_instruction.Pysh_Instruction('string_concat',
															   string_concat,
															   stack_types = ['_string'])
registered_instructions.register_instruction(string_concat_instruction)


def string_head(state):
	if len(state.stacks['_string']) > 0 and len(state.stacks['_integer']) > 0:
		s = state.stacks['_string'].stack_ref(0)
		i = state.stacks['_integer'].stack_ref(0)
		state.stacks['_string'].pop_item()
		state.stacks['_integer'].pop_item()
		state.stacks['_string'].push_item(s[:i])
	return state
string_head_instruction = pysh_instruction.Pysh_Instruction('string_head',
															 string_head,
															 stack_types = ['_string', '_integer'])
registered_instructions.register_instruction(string_head_instructions)


def string_tail(state):
	if len(state.stacks['_string']) > 0 and len(state.stacks['_integer']) > 0:
		s = state.stacks['_string'].stack_ref(0)
		i = state.stacks['_integer'].stack_ref(0)
		state.stacks['_string'].pop_item()
		state.stacks['_integer'].pop_item()
		state.stacks['_string'].push_item(s[-i:])
	return state
string_tail_instruction = pysh_instruction.Pysh_Instruction('string_tail',
															 string_tail,
															 stack_types = ['_string', '_integer'])
registered_instructions.register_instruction(string_head_instructions)

def string_substring(state):
	if len(state.stacks['_string']) > 1 and len(state.stacks['_integer']) > 0:
		s = state.stacks['_string'].stack_ref(0)
		start_index = state.stacks['_integer'].stack_ref(0)
		end_index = 
		state.stacks['_string'].pop_item()
		state.stacks['_integer'].pop_item()
		state.stacks['_string'].push_item(s[-i:])
	return state
string_tail_instruction = pysh_instruction.Pysh_Instruction('string_tail',
															 string_tail,
															 stack_types = ['_string', '_integer'])
registered_instructions.register_instruction(string_head_instructions)

# def string_split_at_index(state):
#	pass

# def string_split_at_str(state):
#	pass

# def string_split_at_space(state):
#	pass

# def string_length(state):
#	pass

# def string_reverse(state):
# 	pass



# string_emptystring
# string_contains # True if top string is a substring of second string; false otherwise
# string_replace # In third string on stack, replaces all occurences of second string with first string



