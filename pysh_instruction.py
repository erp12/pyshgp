# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 13:39:36 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

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
        
    def __repr__(self):
        return self.name + "_INSTR"

class Pysh_Input_Instruction(Pysh_Instruction):
    '''
    Subclass secific to storing information about input instructions
    which are generated based on initial state for the _input stack.
    '''

    def __init__(self, name):
        Pysh_Instruction.__init__(self, name, None)
        self.name = name
        self.func = name
        self.stack_types = '_input'

    def __repr__(self):
        return self.name + "_INPT_INSTR"
