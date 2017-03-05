# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 13:39:36 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type



class PyshInstruction(object):
    '''A instruction for the push language.

    Attributes:
        name: A string name for the instruction.
        fun: The python function that manipulates a push state in the desired way.
        stack_types: 
        parentheses:
        atom_type: 
    '''
    
    def __init__(self, name, func, stack_types = [], parentheses = 0):
        self.name = name
        self.func = func
        self.stack_types = stack_types
        self.parentheses = parentheses # Specifies parens group. (0, 1, 2, ... etc)
        
    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return self.name.__hash__()

    def __repr__(self):
        return str(self.name)

class PyshInputInstruction(PyshInstruction):
    '''A push instruction that will handle input values.

    Input instructions which are generated based on initial state of the _input stack.

    Attributes:
        input_index: The index in the input stack to get value from.
    '''

    def __init__(self, input_index):
        name = "_input" + str(input_index)
        PyshInstruction.__init__(self, name, None)
        self.input_index = input_index
        self.stack_types = '_input'
        
    def __repr__(self):
        return str(self.name)

class PyshClassVoteInstruction(PyshInstruction):
    '''A push instruction that will handle Class Voting.

    Pulls from a numerical stack to add "votes" to an element of the output stack.
    Intended to be used in classification problems.

    Attributes:
        class_id: The index in the output stack to place vote.
        vote_stack: The numerical stack from which to pull a vote.
    '''

    def __init__(self, class_id, vote_stack):
        PyshInstruction.__init__(self, "vote"+str(class_id)+vote_stack, None)
        self.class_id = class_id
        self.vote_stack = vote_stack
        self.stack_types = '_class'
        
    def __repr__(self):
        return str(self.name)
