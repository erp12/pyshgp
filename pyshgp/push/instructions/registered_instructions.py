# -*- coding: utf-8 -*-
"""
The :mod:`registered_instructions` module defines functions that handle adding
new Push instructions and retrieving previously registered Push instructions.
"""
from __future__ import absolute_import, division, print_function, unicode_literals


import warnings

from ... import exceptions as e

'''
List of all registered push instructions.
'''
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


class InstructionLookerUpper():
    """A callable object that, when processed in by the push interpreter, returns a specific instruction.

    Use of these instructions is only needed when defining new Push
    instructions that must call themselves, or other situations where a Push
    instruction must be defined in a way that creates an instance of another
    Push instruction that is not yet registered.

    .. todo::
        Consider renaming this class. Perhaps ``JustInTimeInstruction``?
    """

    #: Name of the instruction to look up and use in place of this instruction
    #: during program execution.
    instruction_name = None

    def __init__(self, instruction_name):
        self.instruction_name = instruction_name

    def __call__(self):
        return get_instruction(self.instruction_name)

    def __repr__(self):
        return self.instruction_name + "_LOOKUP"

    def __eq__(self, other):
        return self.instruction_name == other.instruction_name