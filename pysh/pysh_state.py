# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 13:27:39 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type


from . import pysh_stack 
from . import pysh_globals as g

'''
Object containing the entire push state. 
'''
class Pysh_State:
    
    def __init__(self):
        '''
        Constructor of pysh state.
        '''
        # Initializes empty stacks
        self.stacks = {}
        for t in g.pysh_types:
            self.stacks[t] = pysh_stack.Pysh_Stack(t)

    def total_state_size(self):
        i = 0
        for s in self.stacks:
            i += len(s)
        return i
    
    def pretty_print(self):
        '''
        Prints state of all stacks in the pysh_state
        '''
        for t in g.pysh_types:
            print(self.stacks[t].pysh_type, ":", self.stacks[t])
            