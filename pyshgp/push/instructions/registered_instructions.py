# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 18:24:31 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals


import warnings

from ... import exceptions as e

'''
List of all registered push instructions.
'''
registered_instructions = set()

def register_instruction(instruction):
    '''Registers an instruction, excluding duplicates.
    '''   
    if len([i for i in registered_instructions if i.name == instruction.name]) > 0:
        warnings.warn('Duplicate instructions registered: ' + instruction.name + '. Duplicate ignored.')
    else:
        registered_instructions.update([instruction])


def get_instruction(name):
    '''Gets a registered instruction by its name.
    '''
    l = [i for i in registered_instructions if name == i.name]
    if len(l) > 0:
        return l[0]
    else:
        raise e.UnknownInstructionName(name)


def get_instructions_by_pysh_type(pysh_type):
    '''Returns list of instructions that deal with the given pysh_type
    '''
    return [i for i in registered_instructions if pysh_type in i.stack_types]


class InstructionLookerUpper():
    '''A callable object that, when processed in by the push interpreter, returns a specific instruction.
    '''
    def __init__(self, instruction_name):
        self.instruction_name = instruction_name

    def __call__(self):
        return get_instruction(self.instruction_name)

    def __repr__(self):
        return self.instruction_name + "_LOOKUP"

    def __eq__(self, other):
        return self.instruction_name == other.instruction_name