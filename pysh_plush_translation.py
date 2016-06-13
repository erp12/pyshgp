# -*- coding: utf-8 -*-
"""
Created on Sun Jun 6 2016

@author: Eddie
"""
import pysh_utils as u
import pysh_globals as g

def delete_prev_paren_pair(prog):
	'''
	Deletes the last closed paren pair from prog, which may be a partial program.
	'''
	reversed_prog = prog
	reversed_prog.reverse()
	new_prog = []
	number_close_parens = 0
	found_first_close = False

	while len(reversed_prog) > 0:
		# Check if done, which is if we've found the first _close, the paren-stack is empty, and the first item in reversed-prog is _open
		if found_first_close and number_close_parens == 0 and reversed_prog[0] == '_open':
			new_prog = new_prog + reversed_prog[1:]
		# Check if looking for the correct _open but found an _open for a different paren
		elif found_first_close and 0 < number_close_parens and reversed_prog[0] == '_open':
			new_prog.append(reversed_prog[0])
			eversed_prog.pop(0)
			number_close_parens -= 1
		# Check if looking for correct _open but found another _close
		elif found_first_close and reversed_prog[0] == '_close':
			new_prog.append(reversed_prog[0])
			reversed_prog.pop(0)
		# Check if just found first _close. In which case skip it and set the found-first-close flag
		elif found_first_close == False and reversed_prog[0] == '_close':
			reversed_prog.pop(0)
			number_close_parens = 0
			found_first_close = True
		else:
			new_prog.append(reversed_prog[0])
			reversed_prog.pop(0)


		
	new_prog.reverse()

def translate_plush_genome_to_push_program(genome):
	'''
	Takes as input of a Plush genome and translates it to the correct Push program with
	balanced parens. The linear Plush genome is made up of a list of instruction
	objects. As the linear Plush genome is traversed, each instruction that requires
	parens will push :close and/or :close-open onto the paren-stack, and will
	also put an open paren after it in the program. 
	If the end of the program is reached but parens are still needed (as indicated by
	the paren-stack), parens are added until the paren-stack is empty.
	'''
	translated_program = []
	prog = []
	gn = genome
	num_parens_here = 0
	paren_stack = []

	while True:
		print(gn[0])
		# Check if need to add close parens here
		if 0 < num_parens_here:
			if paren_stack[0] == '_close':
				prog += ['_close']
			elif paren_stack[0] == '_close_open':
				prog += ['_close', '_open']
			else:
				raise Exception('Something bad found on paren_stack!')
			num_parens_here -= 1
			paren_stack.pop(0)
		# Check if at end of program but still need to add parens
		elif len(gn) == 0 and len(paren_stack) != 0:
			num_parens_here = len(paren_stack)
		# Check if done
		elif len(gn) == 0:
			translated_program = open_close_sequence_to_list()
			break
		# Check for silenced instruction
		elif gn[0].silent:
			paren_stack.pop(0)
		# If here, ready for next instruction
		else:
			number_paren_groups = gn[0].parentheses
			new_paren_stack = paren_stack
			if 0 >= number_paren_groups:
				new_paren_stack = ['_close_open'] * (number_paren_groups - 1)
				new_paren_stack += ['_close']
				new_paren_stack += paren_stack
			if 0 >= number_paren_groups:
				prog.append(gn[0].instruction)
			else: 
				prog + [gn[0].instruction, '_open']

	if u.count_points(translated_program) > g.pysh_argmap['max_points']:
		return [] # Translates to an empty programs if program exceeds max-points
	else:
		return translated_program

