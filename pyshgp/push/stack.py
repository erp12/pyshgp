# -*- coding: utf-8 -*-

"""
The :mod:`stack` module defines the ``PyshStack`` class which is used to
hold values of a certain type in a ``PyshState`` object.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from .. import utils as u

class PyshStack(list):
    """Stack that holds elements of a sinlge push type. Extends Python list.
    """

    #: The push type that the stack holds.
    pysh_type = None
    
    def __init__(self, pysh_type_str):
        self.pysh_type = pysh_type_str

        # If the pysh_type is ``_output`` then push the empty string to
        # the outut stack.
        if pysh_type_str == '_output':
            self.push_item('')
        
    def push_item(self, value):
        '''Pushes a value to the top of the stack.

        :param value: Value to push onto stack.
        '''
        self.append(value)
        
    def pop_item(self):
        '''Pops the top value off the stack.
        '''
        self.pop();
    
    def top_item(self):
        '''Returns the top item on the stack, or a NoStackItem if empty.

        :returns: Returns the top element of the stack, or NoStackItem if empty.
        '''
        if len(self) > 0:        
            return self[-1]
        else:
            return u.NoStackItem()
    
    def ref(self, position):
        '''Returns the element at a given position.

        If stack is empty, returns NoStackItem. If ``position < 0`` or 
        ``position > len(self)`` returns StackOutOfBounds.

        :param int position: Position in stack to get item.
        :returns: Element at ``positon`` in stack.
        '''
        if len(self) <= position:
            return u.StackOutOfBounds()
        elif len(self) == 0:
            return u.NoStackItem()
        else:
            return self[(len(self) - 1) - position]
        
    def insert(self, position, value):
        """Inserts value at position in stack.'

        :param int position: Position in stack to insert value.
        :param value: Value to insert into stack.
        """
        super(PyshStack, self).insert(len(self) - position, value)

    def flush(self):
        """Empties the stack.
        """
        del self[:]

    def __repr__(self):
        self_r = list(self[::-1])
        return self_r.__repr__()