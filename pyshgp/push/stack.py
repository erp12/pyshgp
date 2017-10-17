# -*- coding: utf-8 -*-
"""
The :mod:`stack` module defines the ``PyshStack`` class which is used to hold
values of a certain type in a ``PyshState`` object.
"""


class PyshStack(list):
    """Stack that holds elements of a sinlge push type. Extends Python list.
    """

    #: The push type that the stack holds.
    pysh_type = None

    def __init__(self, pysh_type_str):
        self.pysh_type = pysh_type_str

    def push(self, value):
        """Pushes a value to the top of the stack. An alias for `append` which
        makes the definition of push instructions more clear.

        Parameters
        ----------
        value :
            Value to push onto stack.
        """
        self.append(value)

    def top_item(self):
        """Returns the top item on the stack, or a NoStackItem if empty.

        Returns
        --------
        Returns the top element of the stack, or NoStackItem if empty.
        """
        if len(self) > 0:
            return self[-1]
        else:
            return None

    def ref(self, position):
        """Returns the element at a given position.

        If stack is empty, returns NoStackItem. If ``position < 0`` or
        ``position > len(self)`` returns StackOutOfBounds.

        Parameters
        ----------
        position : int
            Position in stack to get item.

        Returns
        --------
        Element at ``positon`` in stack.
        """
        if len(self) <= position:
            return None
        elif len(self) == 0:
            return None
        else:
            return self[(len(self) - 1) - position]

    def insert(self, position, value):
        """Inserts value at position in stack.'

        Parameters
        ----------
        position : int
            Position in stack to get item.
        value :
            Value to insert into stack.
        """
        super(PyshStack, self).insert(len(self) - position, value)

    def flush(self):
        """Empties the stack.
        """
        del self[:]

    def __repr__(self):
        self_r = list(self[::-1])
        return self_r.__repr__()
