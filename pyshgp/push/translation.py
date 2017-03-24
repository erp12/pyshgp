# -*- coding: utf-8 -*-
"""
The :mod:`translation` module provides functions that translate Plush genomes 
into Push programs.

.. todo::
    Consider breaking up some of the larger functions in this file.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from .. import utils as u

from . import instruction
from . import plush as pl
from .instructions import registered_instructions as ri
from .instructions import *


def get_matcing_close_index(sequence):
    """Returns the index of the the matching ``"_close"`` to the first ``"_open"``.

    :param sequence: List with some ``"_open"`` and ``"_close"`` elements.
    :returns: Int of index to match ``"_close"``.
    """
    open_count = 0
    for i in range(len(sequence)):
        if u.is_str_type(sequence[i]) and sequence[i] == '_open':
            open_count += 1
        elif u.is_str_type(sequence[i]) and sequence[i] == '_close':
            open_count -= 1
        if open_count == 0:
            return i
        i += 1

def open_close_sequence_to_list(sequence):
    """Converts flat list with ``"_open"`` and ``"_close"`` elements to nested lists.

    :param sequence: List with some ``"_open"`` and ``"_close"`` elements.

    :example: 
        >>> open_close_sequence_to_list(["_open", 1, "_close", "_open", 2, "_close"]))
        [[1], [2]]
    """
    if not type(sequence) == list:
        return sequence
    elif len(sequence) == 0:
        return []
    else:
        result = []
        rest = sequence
        while len(rest) > 0:
            if u.is_str_type(rest[0]) and rest[0] == '_open':
                i = get_matcing_close_index(rest)
                sub_seq = rest[1:i]
                result.append( open_close_sequence_to_list(sub_seq) )
                rest = rest[i+1:]
            else:
                result.append(rest[0])
                rest.pop(0)
        return result

def translate_plush_genome_to_push_program(genome, max_points):
    """Given a Plush genomes, returns the equivalent Push program.

    Takes as input of a Plush genome and translates it to the correct Push 
    program with balanced parens. The linear Plush genome is made up of a list
    of instruction objects. As the linear Plush genome is traversed, each 
    instruction that requires parens will push ``"_close"`` and/or 
    ``"_close_open"`` onto the paren stack, and will also put an open paren
    after it in the program.  If the end of the program is reached but parens
    are still needed (as indicated by the paren-stack), parens are added until
    the paren stack is empty.

    :param list genome: List of Plush genes to be translated.
    :param int max_points: Max size of translated program.
    :returns: A Push program.
    """

    # The program being built after being translated from open-close sequence.
    translated_program = None

    # The open-close being built. 
    prog = []

    # The linear Plush genome being translated. List of Plush_Gene objects.
    gn = genome 

     # The number of parens that still need to be added at this location.
    num_parens_here = 0

    # Whenever an instruction requires parens grouping, it will push either 
    # _close or _close_open on this stack. This will indicate what to insert in
    # the program the next time a paren is indicated by the _close key in the 
    # instruction.
    paren_stack = [] 

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
            translated_program = open_close_sequence_to_list(prog)
            looping = False
        # Check for silenced instruction
        elif pl.plush_gene_is_silent(gn[0]):
            gn.pop(0)
        # If here, ready for next instruction
        else:
            instr = pl.plush_gene_get_instruction(gn[0])
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

