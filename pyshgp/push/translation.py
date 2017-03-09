# -*- coding: utf-8 -*-
"""
The :mod:`translation` module provides functions that translate Plush genomes 
into Push programs.

Todo:
	Consider breaking up some of the larger functions in this file.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from .. import utils as u

from . import instruction
from . import plush as pl
from .instructions import registered_instructions as ri
from .instructions import *


def get_matcing_close_index(sequence):
    open_count = 0
    for i in range(len(sequence)):
        if sequence[i] == '_open':
            open_count += 1
        elif sequence[i] == '_close':
            open_count -= 1
        if open_count == 0:
            return i
        i += 1

def open_close_sequence_to_list(sequence):
    if not type(sequence) == list:
        return sequence
    elif len(sequence) == 0:
        return []
    else:
        result = []
        rest = sequence
        while len(rest) > 0:
            if rest[0] == '_open':
                i = get_matcing_close_index(rest)
                sub_seq = rest[1:i]
                result.append( open_close_sequence_to_list(sub_seq) )
                rest = rest[i+1:]
            else:
                result.append(rest[0])
                rest.pop(0)
        return result
# print(open_close_sequence_to_list(["_open", 1, 2, "_open", 'a', 'b', "_open", 'c', "_close", "_open", "_open", 'd', "_close", "_close", 'e', "_close", "_close"]))
# print(open_close_sequence_to_list(["_open", 1, "_close", "_open", 2, "_close"]))
# print(open_close_sequence_to_list(["_open", "_open", 1, "_close", "_open", 2, "_close", "_close"]))


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
			reversed_prog.pop(0)
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
	return new_prog

def translate_plush_genome_to_push_program(genome, max_points, atom_generators = None):
	'''
	Takes as input of a Plush genome and translates it to the correct Push program with
	balanced parens. The linear Plush genome is made up of a list of instruction
	objects. As the linear Plush genome is traversed, each instruction that requires
	parens will push :close and/or :close-open onto the paren-stack, and will
	also put an open paren after it in the program. 
	If the end of the program is reached but parens are still needed (as indicated by
	the paren-stack), parens are added until the paren-stack is empty.
	'''

	translated_program = None # The program being built after being translated from open-close sequence.
	prog = [] # The open-close being built. 
	gn = genome # The linear Plush genome being translated. List of Plush_Gene objects.
	num_parens_here = 0 # The number of parens that still need to be added at this location.
	paren_stack = [] # Whenever an instruction requires parens grouping, it will push either _close or _close-open on this stack. This will indicate what to insert in the program the next time a paren is indicated by the _close key in the instruction.

	looping = True
	while looping:
		# Check if need to add close parens here
		if num_parens_here != None and 0 < num_parens_here:
			if len(paren_stack) > 0:
				if paren_stack[0] == '_close':
					prog += ['_close']
				elif paren_stack[0] == '_close_open':
					prog += ['_close', '_open']
				else:
					raise Exception('Something bad found on paren_stack!')
			num_parens_here -= 1
			paren_stack = paren_stack[1:]
		# Check if at end of program but still need to add parens
		elif len(gn) == 0 and len(paren_stack) != 0:
			num_parens_here = len(paren_stack)
		# Check if done
		elif len(gn) == 0:
			translated_program = u.open_close_sequence_to_list(prog)
			looping = False
		# Check for silenced instruction
		elif pl.plush_gene_is_silent(gn[0]):
			gn.pop(0)
		# If here, ready for next instruction
		else:
			instr = pl.plush_gene_get_instruction(gn[0])
			
			# if not pl.plush_gene_is_literal(gn[0]):
			# 	if not (atom_generators != None and instr in atom_generators):
			# 		instr = ri.get_instruction(instr.name)

			number_paren_groups = 0
			if isinstance(instr, instruction.PyshInstruction):
				number_paren_groups = instr.parentheses

			new_paren_stack = paren_stack
			if 0 < number_paren_groups:
				new_paren_stack = ['_close_open'] * (number_paren_groups - 1)
				new_paren_stack += ['_close']
				new_paren_stack += paren_stack
				
			if 0 >= number_paren_groups:
				prog.append(instr)
			else: 
				prog += [instr, '_open']
			num_parens_here = pl.plush_gene_get_closes(gn[0])
			gn = gn[1:]
			paren_stack = new_paren_stack

	if u.count_points(translated_program) > max_points:
		print("Too many points! Max is:", max_points)
		return [] # Translates to an empty programs if program exceeds max-points
	else:
		return translated_program

