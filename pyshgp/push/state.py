# -*- coding: utf-8 -*-

"""
The :mod:`state` module defines the ``PyshState`` class which is used to hold
all values during the execution of a PushProgram.

.. todo::
    Consider merging this file with ``interpreter.py`` to simplify the 
    manipuation of Push states. 
"""

from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type


from . import stack 
from .. import constants as c


class PyshState:
    """Object containing the entire push state. 

    .. todo::
        This should could extend from dict.
    """
    
    def __init__(self):
        '''Initializes empty stacks
        '''
        self.stacks = {}
        for t in c.pysh_types:
            self.stacks[t] = stack.PyshStack(t)

    def size(self):
        '''Returns the number of items on the stack, not including output str.

        :returns: Int of size.
        '''
        i = 0
        for stk in self.stacks.values():
            i += len(stk)
        # if output stack exists, subtract 1 from total because the
        # first element of the output stack is the printing string.
        if '_output' in self.stacks.keys():
            i -= 1
        return i

    def as_dict(self):
        '''Returns the state as a python dictionary

        :returns: Dict of all values in state.
        '''
        dct = {}
        for k in self.stacks.keys():
            dct[k] = self.stacks[k][:]
        return dct
    
    def pretty_print(self):
        '''Prints state of all stacks in the pysh_state
        '''
        for t in c.pysh_types:
            print(self.stacks[t].pysh_type, ":", self.stacks[t])
            