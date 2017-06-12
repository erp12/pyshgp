# -*- coding: utf-8 -*-
"""
The :mod:`registered_instructions` module defines functions that handle adding
new Push instructions and retrieving previously registered Push instructions.
"""
from __future__ import absolute_import, division, print_function, unicode_literals


import warnings

from ... import exceptions as e


#: List of all registered push instructions.
registered_instructions = set()

def register_instruction(instruction):
    """Registers an instruction, excluding duplicates.

    :param PushInstruction instruction: The instruction object to register.
    """
    if len([i for i in registered_instructions if i.name == instruction.name]) > 0:
        warnings.warn('Duplicate instructions registered: ' + instruction.name + '. Duplicate ignored.')
    else:
        registered_instructions.update([instruction])


def get_instruction(name):
    """Gets a registered instruction by its name.

    :param str name: Name of instruction
    :returns: A PushInstruction with ``name``, or throws UnknownInstructionName.
    """
    l = [i for i in registered_instructions if name == i.name]
    if len(l) > 0:
        return l[0]
    else:
        raise e.UnknownInstructionName(name)


def get_instructions_by_pysh_type(pysh_type):
    """Returns list of instructions that deal with the given pysh_type

    :param str pysh_type: Pysh type string (ie ``'_integer'``) to filter by.
    :returns: List if PushInstruction objects that are associated with ``pysh_type``.
    """
    return [i for i in registered_instructions if pysh_type in i.stack_types]
