# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 13:39:36 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

INSTRUCTION_ATOM_TYPE = 0
INPUT_INSTRUCTION_ATOM_TYPE = 1
CLASS_LABEL_INSTRUCTION_ATOM_TYPE = 2

class Pysh_Instruction(object):
    '''
    Holds information about a push instruction. Can be found in a
    Push program.
    '''
    
    def __init__(self, name, func, stack_types = [], parentheses = 0):
        self.name = name
        self.func = func
        self.stack_types = stack_types
        self.parentheses = parentheses # Specifies parens group. (0, 1, 2, ... etc)
        self.atom_type = INSTRUCTION_ATOM_TYPE
        
    def __repr__(self):
        return str(self.name) + "_INSTR"

class Pysh_Input_Instruction(Pysh_Instruction):
    '''
    Subclass secific to storing information about input instructions
    which are generated based on initial state for the _input stack.
    '''

    def __init__(self, input_index):
        name = "_input" + str(input_index)
        print("NAME", name)
        Pysh_Instruction.__init__(self, name, None)
        self.input_index = input_index
        self.func = "_input" + str(input_index)
        self.stack_types = '_input'
        self.atom_type = INPUT_INSTRUCTION_ATOM_TYPE
        
    def __repr__(self):
        return str(self.name) + "_INPT_INSTR"

class Pysh_Class_Instruction(Pysh_Instruction):
    '''
    Subclass secific to classification problems. Pulls from a numerical
    stack to add "votes" to an elementof the output stack.
    '''

    def __init__(self, class_id, vote_stack):
        Pysh_Instruction.__init__(self, "vote"+str(class_id)+vote_stack, None)
        self.class_id = class_id
        self.vote_stack = vote_stack
        self.stack_types = '_class'
        self.atom_type = CLASS_LABEL_INSTRUCTION_ATOM_TYPE
        
    def __repr__(self):
        return str(self.name) + "_CLASS_INSTR"
