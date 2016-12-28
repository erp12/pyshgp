# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 13:18:57 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from .. import utils as u

class PyshStack(list):
    '''Stack that holds elements of a sinlge push type.

    Attributes:
        pysh_type: The push type that the stack holds.
    '''
    
    def __init__(self, pysh_type_str):
        '''
        
        '''
        self.pysh_type = pysh_type_str

        # If the pysh_type is ``_output`` then push the empty string to
        # the outut stack.
        if pysh_type_str == '_output':
            self.push_item('')
        
    def push_item(self, value):
        '''Pushes ``value`` to the top of the stack.
        '''
        self.append(value)
        
    def pop_item(self):
        '''Pops the top value off the stack.
        '''
        self.pop();
    
    def top_item(self):
        '''Returns the top item on the stack, or a NoStackItem if empty.
        '''
        if len(self) > 0:        
            return self[-1]
        else:
            return u.NoStackItem()
    
    def stack_ref(self, position):
        '''Returns the element at a given position.
        '''
        if len(self) <= position:
            return u.StackOutOfBounds()
        elif len(self) == 0:
            return u.NoStackItem()
        else:
            return self[(len(self) - 1) - position]
        
    def stack_insert(self, position, value):
        self.insert(len(self) - position, value)

    def stack_flush(self):
        del self[:]

    def __repr__(self):
        '''Prints the stack as a reversed list.
        '''
        self_r = list(self[::-1])
        return self_r.__repr__()