# -*- coding: utf-8 -*-
"""
The :mod:`translation` module provides functions that translate Plush genomes
into Push programs.
"""
from copy import copy

from ..utils import is_str_type
from .instruction import Instruction


def get_matcing_close_index(sequence):
    """Returns the index of the the matching ``"_close"``
    to the first ``"_open"``.

    Parameters
    ----------
    sequence : list
        List with some ``"_open"`` and ``"_close"`` elements.

    Returns
    --------
    Int of index to match ``"_close"``.
    """
    open_count = 0
    for i in range(len(sequence)):
        if is_str_type(sequence[i]) and sequence[i] == '_open':
            open_count += 1
        elif is_str_type(sequence[i]) and sequence[i] == '_close':
            open_count -= 1
        if open_count == 0:
            return i
        i += 1


def open_close_sequence_to_list(sequence):
    """Converts flat list with ``"_open"`` and ``"_close"`` elements to
    nested lists.

    Parameters
    ----------
    sequence : list
        List with some ``"_open"`` and ``"_close"`` elements.

    Examples
    --------
    >>> open_close_sequence_to_list(["_open", 1, "_close", 2]))
    [[1], 2]
    """
    if not isinstance(sequence, list):
        return sequence
    elif len(sequence) == 0:
        return []
    else:
        result = []
        rest = sequence
        while len(rest) > 0:
            if is_str_type(rest[0]) and rest[0] == '_open':
                i = get_matcing_close_index(rest)
                sub_seq = rest[1:i]
                result.append(open_close_sequence_to_list(sub_seq))
                rest = rest[i + 1:]
            else:
                result.append(rest[0])
                rest.pop(0)
        return result


def genome_to_program(genome):
    """Given a Plush genomes, returns the equivalent Push program.

    Takes as input of a Plush genome and translates it to the correct Push
    program with balanced parens. The linear Plush genome is made up of a list
    of instruction objects. As the linear Plush genome is traversed, each
    instruction that requires parens will push ``"_close"`` and/or
    ``"_close_open"`` onto the paren stack, and will also put an open paren
    after it in the program.  If the end of the program is reached but parens
    are still needed (as indicated by the paren-stack), parens are added until
    the paren stack is empty.

    Parameters
    ----------
    genome : list
        List of Plush genes to be translated.

    Returns
    --------
    A Push program.
    """

    # The program being built after being translated from open-close sequence.
    translated_program = None

    # The open-close being built.
    prog = []

    # The linear Plush genome being translated. List of Plush_Gene objects.
    gn = copy(genome)

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
        if num_parens_here is not None and 0 < num_parens_here:
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
        elif gn[0].is_silent:
            gn.pop(0)
        # If here, ready for next instruction
        else:
            atom = gn[0].atom
            number_paren_groups = 0
            if isinstance(atom, Instruction):
                number_paren_groups = atom.parentheses

            new_paren_stack = paren_stack
            if 0 < number_paren_groups:
                new_paren_stack = ['_close_open'] * (number_paren_groups - 1)
                new_paren_stack += ['_close']
                new_paren_stack += paren_stack

            if 0 >= number_paren_groups:
                prog.append(atom)
            else:
                prog += [atom, '_open']
            num_parens_here = gn[0].closes
            gn = gn[1:]
            paren_stack = new_paren_stack

    return translated_program
