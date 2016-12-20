# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 13:27:39 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type


from . import stack 
from .. import constants as c

'''
Object containing the entire push state. 
'''
class PyshState:
    
    def __init__(self):
        '''Initializes empty stacks
        '''
        self.stacks = {}
        for t in c.pysh_types:
            self.stacks[t] = stack.PyshStack(t)

    def size(self):
        '''Returns the number of items on the stack
        '''
        i = 0
        for stk in self.stacks.values():
            i += len(stk)
        # if output stack exists, subtract 1 from total because the
        # first element of the output stack is the printing string.
        if '_output' in self.stacks.keys():
            i -= 1
        return i
    
    def pretty_print(self):
        '''Prints state of all stacks in the pysh_state
        '''
        for t in c.pysh_types:
            print(self.stacks[t].pysh_type, ":", self.stacks[t])
            